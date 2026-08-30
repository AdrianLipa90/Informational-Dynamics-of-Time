from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .bifurcation import BifurcationError
from .now_bifurcation_bridge import GatedBifurcation, wave_active_bifurcation_operator
from .now_material_quantile_binding import BoundNowMarker


class BoundNowBifurcationError(ValueError):
    pass


@dataclass(frozen=True)
class BoundNowBifurcation:
    occurrence_prefix: tuple[str, ...]
    terminal_edge_id: str
    theta: float
    material_position: float
    material_velocity: float
    realization_weight: float
    mobility: float
    phase_increment_rad: float
    operator: np.ndarray


def _finite(value: float, name: str) -> float:
    out = float(value)
    if not math.isfinite(out):
        raise BoundNowBifurcationError(f"{name} must be finite")
    return out


def bind_now_bifurcation(
    bound_now: BoundNowMarker,
    *,
    material_theta: float,
    structural_signature: float,
    wave_activation: float,
    activity: float,
    current: float,
    generator: Sequence[Sequence[complex]],
    atol: float = 1e-12,
) -> BoundNowBifurcation:
    occ = bound_now.occurrence
    if occ.terminal_edge_id is None or occ.terminal_event_weight is None:
        raise BoundNowBifurcationError("bound NOW occurrence must terminate on a realized event")
    if occ.terminal_event_weight <= 0.0:
        raise BoundNowBifurcationError("bound NOW occurrence must have positive terminal event weight")

    theta_material = _finite(material_theta, "material_theta")
    tol = _finite(atol, "atol")
    if tol < 0.0:
        raise BoundNowBifurcationError("atol must be non-negative")
    if not math.isclose(theta_material, float(occ.theta), rel_tol=0.0, abs_tol=tol):
        raise BoundNowBifurcationError("material Theta must match the realized occurrence Theta")

    signature = _finite(structural_signature, "structural_signature")
    activation = _finite(wave_activation, "wave_activation")
    if signature < 0.0 or activation < 0.0:
        raise BoundNowBifurcationError("realization factors must be non-negative")
    expected_weight = signature * activation
    if not math.isclose(expected_weight, float(occ.terminal_event_weight), rel_tol=0.0, abs_tol=tol):
        raise BoundNowBifurcationError(
            "realization product must match the terminal occurrence event weight"
        )

    try:
        gated: GatedBifurcation = wave_active_bifurcation_operator(
            signature,
            activation,
            activity,
            current,
            generator,
        )
    except BifurcationError as exc:
        raise BoundNowBifurcationError(str(exc)) from exc

    if not gated.realized or gated.realization_weight <= 0.0:
        raise BoundNowBifurcationError("selected NOW occurrence must produce a realized bifurcation")

    front = bound_now.material_front
    if not all(
        math.isfinite(float(value))
        for value in (front.position, front.theta_velocity, front.local_density, front.local_current)
    ):
        raise BoundNowBifurcationError("bound material front must be finite")
    if front.local_density <= 0.0:
        raise BoundNowBifurcationError("bound material front density must be positive")

    return BoundNowBifurcation(
        occurrence_prefix=tuple(occ.prefix),
        terminal_edge_id=str(occ.terminal_edge_id),
        theta=float(occ.theta),
        material_position=float(front.position),
        material_velocity=float(front.theta_velocity),
        realization_weight=float(gated.realization_weight),
        mobility=float(gated.coordinates.mobility),
        phase_increment_rad=float(gated.coordinates.phase_increment_rad),
        operator=np.asarray(gated.operator, dtype=complex).copy(),
    )


def apply_bound_bifurcation(
    state_before: Sequence[complex],
    bound: BoundNowBifurcation,
) -> np.ndarray:
    state = np.asarray(state_before, dtype=complex)
    op = np.asarray(bound.operator, dtype=complex)
    if state.ndim != 1 or state.size == 0:
        raise BoundNowBifurcationError("state_before must be a non-empty vector")
    if op.ndim != 2 or op.shape != (state.size, state.size):
        raise BoundNowBifurcationError("operator dimension must match the state vector")
    if not np.all(np.isfinite(state.real)) or not np.all(np.isfinite(state.imag)):
        raise BoundNowBifurcationError("state_before must be finite")
    return op @ state
