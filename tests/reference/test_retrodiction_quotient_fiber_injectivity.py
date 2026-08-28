from __future__ import annotations

import numpy as np
import pytest

from src.idt.retrodiction_quotient_fiber_injectivity import (
    QuotientFiberInjectivityError,
    audit_finite_quotient_fiber_injectivity,
)


def test_sheet_bit_separates_exact_quotient_collision() -> None:
    audit = audit_finite_quotient_fiber_injectivity(
        [[4.0], [4.0]],
        [[2.0], [-2.0]],
        {"sheet": [[1.0], [-1.0]]},
    )
    assert audit.status == "FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER"
    assert audit.base_collision_count == 1
    assert audit.collisions[0].separating_channels == ("sheet",)


def test_scale_fiber_separates_normalized_shape_collision() -> None:
    audit = audit_finite_quotient_fiber_injectivity(
        [[0.6, 0.8], [0.6, 0.8]],
        [[3.0, 4.0], [6.0, 8.0]],
        {"scale": [[5.0], [10.0]]},
    )
    assert audit.status == "FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER"
    assert audit.collisions[0].augmented_distance == pytest.approx(5.0)


def test_identical_declared_fiber_preserves_collision() -> None:
    audit = audit_finite_quotient_fiber_injectivity(
        [[1.0], [1.0]],
        [[0.0], [2.0]],
        {"residence_label": [[0.0], [0.0]]},
    )
    assert audit.status == "FINITE_DOMAIN_COLLISIONS_PERSIST"
    assert audit.unresolved_collision_count == 1


def test_all_base_collisions_must_be_separated() -> None:
    audit = audit_finite_quotient_fiber_injectivity(
        [[0.0], [0.0], [0.0]],
        [[0.0], [1.0], [2.0]],
        {"fiber": [[0.0], [1.0], [1.0]]},
    )
    assert audit.base_collision_count == 3
    assert audit.separated_collision_count == 2
    assert audit.unresolved_collision_count == 1
    assert audit.status == "FINITE_DOMAIN_COLLISIONS_PERSIST"


def test_noncolliding_projection_needs_no_fiber_separation() -> None:
    audit = audit_finite_quotient_fiber_injectivity(
        [[0.0], [1.0]],
        [[0.0], [2.0]],
        {"fiber": [[0.0], [0.0]]},
    )
    assert audit.status == "NO_BASE_COLLISIONS_IN_FINITE_DOMAIN"
    assert audit.base_collision_count == 0


def test_channel_names_are_deterministic_and_sorted() -> None:
    audit = audit_finite_quotient_fiber_injectivity(
        [[0.0], [0.0]],
        [[0.0], [1.0]],
        {"zeta": [[0.0], [2.0]], "alpha": [[0.0], [3.0]]},
    )
    assert audit.collisions[0].separating_channels == ("alpha", "zeta")


def test_invalid_shapes_and_tolerances_fail_closed() -> None:
    with pytest.raises(QuotientFiberInjectivityError):
        audit_finite_quotient_fiber_injectivity(
            [[0.0]], [[0.0]], {"f": [[0.0]]}
        )
    with pytest.raises(QuotientFiberInjectivityError):
        audit_finite_quotient_fiber_injectivity(
            [[0.0], [0.0]],
            [[0.0], [1.0]],
            {"f": [[0.0], [1.0]]},
            base_tolerance=0.0,
        )
    with pytest.raises(QuotientFiberInjectivityError):
        audit_finite_quotient_fiber_injectivity(
            [[0.0], [0.0]],
            [[0.0], [1.0]],
            {"f": [[np.nan], [1.0]]},
        )


def test_current_07h_reflection_null_is_separated_by_wA1_fiber() -> None:
    reference_latent = [0.034, -0.023, -0.008, 0.028]
    alternate_latent = [
        0.03399999999998063,
        0.34071654937113033,
        -0.00802729491823317,
        -0.8206629500579328,
    ]
    base = [
        np.zeros(6),
        np.array([5.594315114139762e-17, 0, 0, 0, 0, 0]),
    ]
    audit = audit_finite_quotient_fiber_injectivity(
        base,
        [reference_latent, alternate_latent],
        {"w_A_1": [[0.5838364569736161], [0.6030256253846112]]},
        base_tolerance=1e-10,
        latent_tolerance=1e-8,
        fiber_tolerance=1e-10,
    )
    assert audit.status == "FINITE_DOMAIN_INJECTIVE_WITH_DECLARED_FIBER"
    assert audit.collisions[0].latent_distance == pytest.approx(
        0.9233193011263697
    )
    assert audit.collisions[0].separating_channels == ("w_A_1",)


def test_current_07h_rx1_negative_control_does_not_separate_fiber() -> None:
    reference_latent = [0.034, -0.023, -0.008, 0.028]
    alternate_latent = [
        0.03399999999998063,
        0.34071654937113033,
        -0.00802729491823317,
        -0.8206629500579328,
    ]
    base = [
        np.zeros(6),
        np.array([5.594315114139762e-17, 0, 0, 0, 0, 0]),
    ]
    audit = audit_finite_quotient_fiber_injectivity(
        base,
        [reference_latent, alternate_latent],
        {"r_x_1": [[0.0], [1.1102230246251565e-16]]},
        fiber_tolerance=1e-10,
    )
    assert audit.status == "FINITE_DOMAIN_COLLISIONS_PERSIST"
    assert audit.collisions[0].separating_channels == ()
