from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import KeplerMemoryError, MemoryPhaseState, kepler_memory_step


class RetrodictionObservabilityError(ValueError):
    pass


@dataclass(frozen=True)
class RetrodictionObservabilityAudit:
    jacobian: np.ndarray
    singular_values: np.ndarray
    rank: int
    unknown_dimension: int
    observation_dimension: int
    condition_number: float
    locally_identifiable: bool
    status: str


def _state_copy(state: MemoryPhaseState) -> MemoryPhaseState:
    r = np.asarray(state.position, dtype=float)
    v = np.asarray(state.velocity, dtype=float)
    if r.shape != (2,) or v.shape != (2,):
        raise RetrodictionObservabilityError("memory state position and velocity must be two-component vectors")
    if not np.all(np.isfinite(r)) or not np.all(np.isfinite(v)):
        raise RetrodictionObservabilityError("memory state must be finite")
    tau = float(state.tau_internal)
    area = float(state.swept_area)
    if not (math.isfinite(tau) and math.isfinite(area)):
        raise RetrodictionObservabilityError("memory state tau_internal and swept_area must be finite")
    return MemoryPhaseState(r.copy(), v.copy(), tau, area)


def _positive_sequence(values: Sequence[float], name: str) -> list[float]:
    out = [float(x) for x in values]
    if not out:
        raise RetrodictionObservabilityError(f"{name} must be non-empty")
    if any((not math.isfinite(x) or x <= 0.0) for x in out):
        raise RetrodictionObservabilityError(f"{name} entries must be finite and strictly positive")
    return out


def _kick_array(kicks: Sequence[complex]) -> np.ndarray:
    if not kicks:
        raise RetrodictionObservabilityError("nominal_kicks must be non-empty")
    out = np.empty((len(kicks), 2), dtype=float)
    for idx, raw in enumerate(kicks):
        z = complex(raw)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise RetrodictionObservabilityError("nominal_kicks must be finite")
        out[idx] = (z.real, z.imag)
    return out


def forward_kick_lineage(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    kicks: Sequence[complex],
) -> list[MemoryPhaseState]:
    """Propagate a memory lineage using direct two-component event kicks followed by Kepler steps."""
    state = _state_copy(initial_state)
    dts = _positive_sequence(delta_taus, "delta_taus")
    kick_array = _kick_array(kicks)
    if len(dts) != len(kick_array):
        raise RetrodictionObservabilityError("delta_taus and kicks must have one common length")

    states = [state]
    current = state
    for dt, kick in zip(dts, kick_array):
        kicked = MemoryPhaseState(
            current.position.copy(),
            current.velocity + kick,
            current.tau_internal,
            current.swept_area,
        )
        try:
            current = kepler_memory_step(kicked, mu_memory, dt)
        except KeplerMemoryError as exc:
            raise RetrodictionObservabilityError(str(exc)) from exc
        states.append(current)
    return states


def checkpoint_phase_vector(states: Sequence[MemoryPhaseState], checkpoint_indices: Sequence[int]) -> np.ndarray:
    if not checkpoint_indices:
        raise RetrodictionObservabilityError("checkpoint_indices must be non-empty")
    indices = [int(i) for i in checkpoint_indices]
    if len(indices) != len(set(indices)):
        raise RetrodictionObservabilityError("checkpoint_indices must be unique")
    if any(i <= 0 or i >= len(states) for i in indices):
        raise RetrodictionObservabilityError("checkpoint_indices must select post-event states in [1, N]")

    values: list[float] = []
    for idx in indices:
        state = _state_copy(states[idx])
        values.extend(float(x) for x in state.position)
        values.extend(float(x) for x in state.velocity)
    return np.asarray(values, dtype=float)


def kick_sensitivity_matrix(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    nominal_kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    *,
    finite_difference_step: float = 1e-7,
) -> np.ndarray:
    """Central finite-difference Jacobian dY/dz for latent two-component event kicks."""
    dts = _positive_sequence(delta_taus, "delta_taus")
    kicks = _kick_array(nominal_kicks)
    if len(dts) != len(kicks):
        raise RetrodictionObservabilityError("delta_taus and nominal_kicks must have one common length")
    eps = float(finite_difference_step)
    if not math.isfinite(eps) or eps <= 0.0:
        raise RetrodictionObservabilityError("finite_difference_step must be finite and strictly positive")

    def observe(kick_matrix: np.ndarray) -> np.ndarray:
        complex_kicks = [complex(float(k[0]), float(k[1])) for k in kick_matrix]
        states = forward_kick_lineage(initial_state, mu_memory, dts, complex_kicks)
        return checkpoint_phase_vector(states, checkpoint_indices)

    y0 = observe(kicks)
    jac = np.empty((y0.size, kicks.size), dtype=float)
    for column in range(kicks.size):
        plus = kicks.copy()
        minus = kicks.copy()
        plus.flat[column] += eps
        minus.flat[column] -= eps
        jac[:, column] = (observe(plus) - observe(minus)) / (2.0 * eps)
    if not np.all(np.isfinite(jac)):
        raise RetrodictionObservabilityError("non-finite sensitivity matrix")
    return jac


def audit_kick_observability(
    initial_state: MemoryPhaseState,
    mu_memory: float,
    delta_taus: Sequence[float],
    nominal_kicks: Sequence[complex],
    checkpoint_indices: Sequence[int],
    *,
    finite_difference_step: float = 1e-7,
    relative_rank_tolerance: float = 1e-8,
) -> RetrodictionObservabilityAudit:
    """Audit first-order local identifiability of latent event kicks from retained checkpoints."""
    tol = float(relative_rank_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise RetrodictionObservabilityError("relative_rank_tolerance must be finite and strictly positive")

    jac = kick_sensitivity_matrix(
        initial_state,
        mu_memory,
        delta_taus,
        nominal_kicks,
        checkpoint_indices,
        finite_difference_step=finite_difference_step,
    )
    singular = np.linalg.svd(jac, compute_uv=False)
    unknown_dim = int(jac.shape[1])
    observation_dim = int(jac.shape[0])
    if singular.size == 0:
        raise RetrodictionObservabilityError("empty singular spectrum")
    threshold = tol * max(1.0, float(singular[0]))
    rank = int(np.sum(singular > threshold))

    if observation_dim < unknown_dim:
        status = "UNDERDETERMINED_DIMENSION"
        identifiable = False
    elif rank < unknown_dim:
        status = "RANK_DEFICIENT"
        identifiable = False
    else:
        status = "LOCALLY_IDENTIFIABLE_REFERENCE"
        identifiable = True

    if identifiable:
        smallest = float(singular[unknown_dim - 1])
        condition = float(singular[0] / smallest)
    else:
        condition = math.inf

    return RetrodictionObservabilityAudit(
        jacobian=jac,
        singular_values=singular,
        rank=rank,
        unknown_dimension=unknown_dim,
        observation_dimension=observation_dim,
        condition_number=condition,
        locally_identifiable=identifiable,
        status=status,
    )


def final_checkpoint_dimension_bound(number_of_unknown_kicks: int) -> tuple[int, int, bool]:
    """Return (unknown dimension, final phase-state dimension, dimensionally possible)."""
    n = int(number_of_unknown_kicks)
    if n <= 0:
        raise RetrodictionObservabilityError("number_of_unknown_kicks must be a positive integer")
    unknown = 2 * n
    observed = 4
    return unknown, observed, observed >= unknown
