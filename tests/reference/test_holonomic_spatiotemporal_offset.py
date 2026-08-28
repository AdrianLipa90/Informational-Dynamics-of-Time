import math

import numpy as np
import pytest

from idt.holonomic_spatiotemporal_offset import (
    HolonomicOffsetError,
    audit_phase_closed_offset,
    calibrated_elapsed_time,
    phase_closure_residual,
    temporal_offset_divergence,
    temporal_offset_from_phase_closure,
    total_holonomic_phase,
)


def test_phase_closure_inversion_exact_dimensionless_reference():
    dt = temporal_offset_from_phase_closure(
        p_dot_dx=7.5,
        energy=2.5,
        geometric_phase=0.7,
        winding=1,
        hbar=1.0,
    )
    residual = phase_closure_residual(7.5, 2.5, dt, 0.7, 1, hbar=1.0)
    assert abs(residual) < 1e-14


def test_spatial_temporal_trade_at_fixed_energy_and_holonomy():
    dt0 = temporal_offset_from_phase_closure(1.0, 4.0, 0.3, 0, hbar=1.0)
    dt1 = temporal_offset_from_phase_closure(3.0, 4.0, 0.3, 0, hbar=1.0)
    assert math.isclose(dt1 - dt0, 0.5, rel_tol=0.0, abs_tol=1e-15)


def test_geometric_holonomy_shifts_temporal_offset():
    dt0 = temporal_offset_from_phase_closure(0.0, 5.0, 0.2, 0, hbar=1.0)
    dt1 = temporal_offset_from_phase_closure(0.0, 5.0, 1.2, 0, hbar=1.0)
    assert math.isclose(dt1 - dt0, 0.2, rel_tol=0.0, abs_tol=1e-15)


def test_same_spatial_endpoint_can_carry_temporal_holonomy_offset():
    audit = audit_phase_closed_offset(
        spatial_offset=[0.0, 0.0, 0.0],
        momentum=[1.0, 2.0, 3.0],
        energy=2.0,
        geometric_phase=1.0,
        winding=0,
        hbar=1.0,
    )
    assert math.isclose(audit.coordinate_time_offset, 0.5, abs_tol=1e-15)
    assert abs(audit.closure_residual) < 1e-14


def test_relational_lapse_integrates_calibrated_elapsed_time():
    elapsed = calibrated_elapsed_time([0.2, 0.3, 0.5], [1.0, 2.0, 0.5])
    assert math.isclose(elapsed, 1.05, rel_tol=0.0, abs_tol=1e-15)


def test_temporal_offset_divergence_is_lineage_difference_norm():
    delta, norm = temporal_offset_divergence([0.0, 1.0, 2.0], [0.0, 1.2, 1.7])
    np.testing.assert_allclose(delta, [0.0, 0.2, -0.3], atol=1e-15)
    assert math.isclose(norm, math.sqrt(0.13), rel_tol=0.0, abs_tol=1e-15)


def test_total_phase_matches_closed_audit():
    audit = audit_phase_closed_offset(
        spatial_offset=[2.0, -1.0],
        momentum=[3.0, 4.0],
        energy=5.0,
        geometric_phase=0.4,
        winding=2,
        hbar=1.0,
    )
    phase = total_holonomic_phase(
        p_dot_dx=2.0,
        energy=5.0,
        delta_t=audit.coordinate_time_offset,
        geometric_phase=0.4,
        hbar=1.0,
    )
    assert math.isclose(phase, 4.0 * math.pi, rel_tol=0.0, abs_tol=1e-14)


@pytest.mark.parametrize(
    "kwargs",
    [
        dict(p_dot_dx=1.0, energy=0.0, geometric_phase=0.0, winding=0, hbar=1.0),
        dict(p_dot_dx=1.0, energy=-1.0, geometric_phase=0.0, winding=0, hbar=1.0),
        dict(p_dot_dx=1.0, energy=1.0, geometric_phase=0.0, winding=0, hbar=0.0),
    ],
)
def test_phase_closure_inversion_fails_closed(kwargs):
    with pytest.raises(HolonomicOffsetError):
        temporal_offset_from_phase_closure(**kwargs)
