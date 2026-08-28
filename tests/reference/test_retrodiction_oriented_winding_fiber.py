from __future__ import annotations

import math

import numpy as np
import pytest

from src.idt.kepler_memory import MemoryPhaseState
from src.idt.orchorbital import AttractorSpec
from src.idt.retrodiction_global_null_gate import (
    ScalarCheckpointObservation,
    sparse_orchorbital_observation,
)
from src.idt.retrodiction_oriented_winding_fiber import (
    OrientedWindingFiberError,
    audit_known_null_oriented_winding,
    oriented_winding_fiber_for_kicks,
    winding_fiber_distance,
)
from src.idt.retrodiction_quotient_fiber_injectivity import (
    audit_finite_quotient_fiber_injectivity,
)


def _initial() -> MemoryPhaseState:
    return MemoryPhaseState(
        position=np.array([-0.7, 0.4], dtype=float),
        velocity=np.array([0.05, 0.25], dtype=float),
        tau_internal=0.0,
        swept_area=0.0,
    )


def _attractors():
    return [
        AttractorSpec("A", np.array([-1.5, 0.0]), 3.2),
        AttractorSpec("B", np.array([1.5, 0.0]), 2.7),
        AttractorSpec("C", np.array([0.0, 2.0]), 2.4),
    ]


def _truth():
    return [0.034 - 0.023j, -0.008 + 0.028j]


def _alternate():
    return [
        complex(0.03399999999998063, 0.34071654937113033),
        complex(-0.00802729491823317, -0.8206629500579328),
    ]


def _base_specs():
    return [
        ScalarCheckpointObservation(2, "rx"),
        ScalarCheckpointObservation(2, "ry"),
        ScalarCheckpointObservation(2, "vx"),
        ScalarCheckpointObservation(2, "weight", "A"),
        ScalarCheckpointObservation(2, "weight", "B"),
        ScalarCheckpointObservation(2, "weight", "C"),
    ]


def _latent(kicks):
    return np.asarray(
        [value for kick in kicks for value in (complex(kick).real, complex(kick).imag)],
        dtype=float,
    )


def test_known_reflection_null_is_separated_by_ordered_oriented_winding() -> None:
    audit = audit_known_null_oriented_winding(
        _initial(),
        _attractors(),
        (0.004, 0.003),
        _truth(),
        _alternate(),
        _base_specs(),
        base_tolerance=1e-10,
        fiber_tolerance=1e-12,
    )
    assert audit.base_residual < 1e-12
    assert audit.latent_separation > 0.9
    assert audit.active_sequence_equal
    assert audit.winding_fiber_distance > 1e-12
    assert audit.status == "BASE_NULL_SEPARATED_BY_ORIENTED_WINDING"


def test_winding_fiber_uses_exact_binary64_hex_receipt_values() -> None:
    fiber = oriented_winding_fiber_for_kicks(
        _initial(), _attractors(), (0.004, 0.003), _truth()
    )
    assert fiber.status == "ORDERED_ORIENTED_WINDING_FIBER"
    assert len(fiber.winding_increment_hex) == 2
    assert tuple(float.fromhex(raw) for raw in fiber.winding_increment_hex) == fiber.winding_increments
    assert math.isclose(
        fiber.cumulative_winding,
        math.fsum(fiber.winding_increments),
        rel_tol=0.0,
        abs_tol=0.0,
    )


def test_winding_fiber_is_deterministic_for_identical_history() -> None:
    left = oriented_winding_fiber_for_kicks(
        _initial(), _attractors(), (0.004, 0.003), _truth()
    )
    right = oriented_winding_fiber_for_kicks(
        _initial(), _attractors(), (0.004, 0.003), _truth()
    )
    assert left.winding_increment_hex == right.winding_increment_hex
    assert winding_fiber_distance(left, right) == 0.0


def test_oriented_winding_plugs_into_07p_finite_domain_gate() -> None:
    ref = _truth()
    alt = _alternate()
    base_ref = sparse_orchorbital_observation(
        _initial(), _attractors(), (0.004, 0.003), ref, _base_specs()
    )
    base_alt = sparse_orchorbital_observation(
        _initial(), _attractors(), (0.004, 0.003), alt, _base_specs()
    )
    fiber_ref = oriented_winding_fiber_for_kicks(
        _initial(), _attractors(), (0.004, 0.003), ref
    )
    fiber_alt = oriented_winding_fiber_for_kicks(
        _initial(), _attractors(), (0.004, 0.003), alt
    )
    audit = audit_finite_quotient_fiber_injectivity(
        (base_ref, base_alt),
        (_latent(ref), _latent(alt)),
        {
            "oriented_winding": (
                fiber_ref.winding_increments,
                fiber_alt.winding_increments,
            )
        },
        base_tolerance=1e-10,
        latent_tolerance=1e-8,
        fiber_tolerance=1e-12,
    )
    assert audit.base_collision_count == 1
    assert audit.separated_collision_count == 1
    assert audit.unresolved_collision_count == 0
    assert audit.collisions[0].separating_channels == ("oriented_winding",)
    assert audit.status == "FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER"


def test_non_null_pair_is_reported_before_winding_separation_claim() -> None:
    perturbed = [0.05 - 0.02j, -0.01 + 0.03j]
    audit = audit_known_null_oriented_winding(
        _initial(),
        _attractors(),
        (0.004, 0.003),
        _truth(),
        perturbed,
        _base_specs(),
        base_tolerance=1e-14,
    )
    assert audit.base_residual > 1e-14
    assert audit.status == "NOT_A_BASE_NULL"


def test_mismatched_event_count_fails_closed() -> None:
    with pytest.raises(OrientedWindingFiberError, match="equal event count"):
        audit_known_null_oriented_winding(
            _initial(),
            _attractors(),
            (0.004, 0.003),
            _truth(),
            [_alternate()[0]],
            _base_specs(),
        )


def test_nonpositive_delta_tau_fails_closed() -> None:
    with pytest.raises(OrientedWindingFiberError, match="strictly positive"):
        oriented_winding_fiber_for_kicks(
            _initial(), _attractors(), (0.004, 0.0), _truth()
        )
