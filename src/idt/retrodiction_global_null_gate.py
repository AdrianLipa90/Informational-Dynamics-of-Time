from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Sequence

import numpy as np

from .kepler_memory import MemoryPhaseState
from .memory_orchorbital_bridge import replay_memory_orchorbital_lineage
from .memory_recall import MemoryEventReceipt
from .orchorbital import AttractorSpec, evaluate_attractor_field


class RetrodictionGlobalNullError(ValueError):
    pass


@dataclass(frozen=True)
class ScalarCheckpointObservation:
    checkpoint_index: int
    kind: str
    attractor_name: str | None = None


@dataclass(frozen=True)
class KnownNullSeparationAudit:
    base_residual: float
    augmented_residual: float
    latent_separation: float
    base_equivalent: bool
    augmented_equivalent: bool
    status: str


_STATE_COMPONENTS = {
    "rx": ("position", 0),
    "ry": ("position", 1),
    "vx": ("velocity", 0),
    "vy": ("velocity", 1),
}


def _finite_kicks(kicks: Sequence[complex]) -> tuple[complex, ...]:
    if not kicks:
        raise RetrodictionGlobalNullError("kicks must be non-empty")
    out: list[complex] = []
    for raw in kicks:
        z = complex(raw)
        if not (math.isfinite(z.real) and math.isfinite(z.imag)):
            raise RetrodictionGlobalNullError("kicks must be finite")
        out.append(z)
    return tuple(out)


def _validated_observations(
    observations: Sequence[ScalarCheckpointObservation],
    event_count: int,
) -> tuple[ScalarCheckpointObservation, ...]:
    if not observations:
        raise RetrodictionGlobalNullError("observations must be non-empty")
    out: list[ScalarCheckpointObservation] = []
    for raw in observations:
        if not isinstance(raw, ScalarCheckpointObservation):
            raise RetrodictionGlobalNullError(
                "observations must contain ScalarCheckpointObservation values"
            )
        idx = int(raw.checkpoint_index)
        kind = str(raw.kind)
        if idx <= 0 or idx > event_count:
            raise RetrodictionGlobalNullError(
                "checkpoint_index must select a post-event state in [1,N]"
            )
        if kind in _STATE_COMPONENTS:
            if raw.attractor_name is not None:
                raise RetrodictionGlobalNullError(
                    "state-component observations do not accept attractor_name"
                )
        elif kind == "weight":
            name = "" if raw.attractor_name is None else str(raw.attractor_name).strip()
            if not name:
                raise RetrodictionGlobalNullError(
                    "weight observations require a non-empty attractor_name"
                )
        else:
            raise RetrodictionGlobalNullError(
                "kind must be one of rx, ry, vx, vy, weight"
            )
        out.append(ScalarCheckpointObservation(idx, kind, raw.attractor_name))
    return tuple(out)


def sparse_orchorbital_observation(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    kicks: Sequence[complex],
    observations: Sequence[ScalarCheckpointObservation],
) -> np.ndarray:
    """Evaluate an explicitly declared sparse checkpoint observation vector."""
    kick_values = _finite_kicks(kicks)
    dts = [float(value) for value in delta_taus]
    if len(dts) != len(kick_values) or not dts:
        raise RetrodictionGlobalNullError(
            "delta_taus must be non-empty and match the kick count"
        )
    if any((not math.isfinite(value) or value <= 0.0) for value in dts):
        raise RetrodictionGlobalNullError(
            "delta_taus must be finite and strictly positive"
        )
    specs = _validated_observations(observations, len(kick_values))
    receipts = [
        MemoryEventReceipt(dt, 1.0, kick)
        for dt, kick in zip(dts, kick_values)
    ]
    try:
        states, _ = replay_memory_orchorbital_lineage(
            initial_state,
            attractors,
            receipts,
        )
    except ValueError as exc:
        raise RetrodictionGlobalNullError(str(exc)) from exc

    field_cache: dict[int, object] = {}
    values: list[float] = []
    for spec in specs:
        state = states[spec.checkpoint_index]
        if spec.kind in _STATE_COMPONENTS:
            field_name, axis = _STATE_COMPONENTS[spec.kind]
            values.append(float(getattr(state, field_name)[axis]))
            continue

        idx = spec.checkpoint_index
        if idx not in field_cache:
            field = evaluate_attractor_field(state, attractors)
            if field.leak_mode:
                raise RetrodictionGlobalNullError(
                    "observed checkpoint entered LEAK_MODE"
                )
            field_cache[idx] = field
        field = field_cache[idx]
        target = str(spec.attractor_name)
        matches = [ev for ev in field.evaluations if ev.name == target]
        if len(matches) != 1:
            raise RetrodictionGlobalNullError(
                "weight observation attractor is absent or non-unique"
            )
        values.append(float(matches[0].weight))

    result = np.asarray(values, dtype=float)
    if not np.all(np.isfinite(result)):
        raise RetrodictionGlobalNullError("observation became non-finite")
    return result


def _latent_vector(kicks: Sequence[complex]) -> np.ndarray:
    values = _finite_kicks(kicks)
    out = np.empty(2 * len(values), dtype=float)
    for idx, kick in enumerate(values):
        out[2 * idx] = kick.real
        out[2 * idx + 1] = kick.imag
    return out


def audit_known_global_null_separation(
    initial_state: MemoryPhaseState,
    attractors: Sequence[AttractorSpec],
    delta_taus: Sequence[float],
    reference_kicks: Sequence[complex],
    alternate_kicks: Sequence[complex],
    base_observations: Sequence[ScalarCheckpointObservation],
    added_observations: Sequence[ScalarCheckpointObservation],
    *,
    equivalence_tolerance: float = 1e-10,
) -> KnownNullSeparationAudit:
    """Test whether declared added checkpoint scalars separate one known null pair.

    The gate is deliberately pair-scoped. A separated known pair receives
    KNOWN_NULL_SEPARATED; global injectivity remains a separate admission test.
    """
    tol = float(equivalence_tolerance)
    if not math.isfinite(tol) or tol <= 0.0:
        raise RetrodictionGlobalNullError(
            "equivalence_tolerance must be finite and strictly positive"
        )
    ref = _finite_kicks(reference_kicks)
    alt = _finite_kicks(alternate_kicks)
    if len(ref) != len(alt):
        raise RetrodictionGlobalNullError(
            "reference and alternate histories must have equal event count"
        )
    latent_separation = float(np.linalg.norm(_latent_vector(ref) - _latent_vector(alt)))
    if latent_separation <= tol:
        raise RetrodictionGlobalNullError(
            "known-null candidates must be distinct in latent coordinates"
        )

    base_specs = _validated_observations(base_observations, len(ref))
    added_specs = _validated_observations(added_observations, len(ref))
    base_ref = sparse_orchorbital_observation(
        initial_state, attractors, delta_taus, ref, base_specs
    )
    base_alt = sparse_orchorbital_observation(
        initial_state, attractors, delta_taus, alt, base_specs
    )
    augmented_specs = base_specs + added_specs
    aug_ref = sparse_orchorbital_observation(
        initial_state, attractors, delta_taus, ref, augmented_specs
    )
    aug_alt = sparse_orchorbital_observation(
        initial_state, attractors, delta_taus, alt, augmented_specs
    )

    base_residual = float(np.linalg.norm(base_ref - base_alt))
    augmented_residual = float(np.linalg.norm(aug_ref - aug_alt))
    base_equivalent = base_residual <= tol
    augmented_equivalent = augmented_residual <= tol
    if not base_equivalent:
        status = "NOT_A_BASE_NULL"
    elif augmented_equivalent:
        status = "KNOWN_NULL_PERSISTS"
    else:
        status = "KNOWN_NULL_SEPARATED"
    return KnownNullSeparationAudit(
        base_residual,
        augmented_residual,
        latent_separation,
        base_equivalent,
        augmented_equivalent,
        status,
    )
