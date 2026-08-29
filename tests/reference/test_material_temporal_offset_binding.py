import math
import pytest

from idt.material_temporal_offset_binding import (
    fractional_material_offset,
    material_offset_state,
    reference_change_factor,
    transform_material_offset,
)


def make_state(curvature=0.75, omega_ref=3.0, dtheta_ref=2.0, activity_ref=4.0, activity_local=10.0, calibration=0.5):
    lapse = activity_local / activity_ref
    return material_offset_state(
        curvature=curvature,
        omega_ref=omega_ref,
        dtheta_ref=dtheta_ref,
        lapse=lapse,
        calibration=calibration,
        activity_ref=activity_ref,
        activity_local=activity_local,
    )


def test_exact_material_composition():
    state = make_state()
    eta = 0.75 / 3.0
    assert state.seam_ratio == pytest.approx(eta)
    assert state.dtheta_offset == pytest.approx(eta * state.dtheta)
    assert state.dt_offset == pytest.approx(0.5 * state.dtheta_offset)
    assert state.dtau_offset == pytest.approx((10.0 / 4.0) * state.dt_offset)
    assert state.dtau_offset == pytest.approx(eta * state.dtau)


def test_fractional_offset_is_seam_ratio():
    state = make_state(curvature=-1.2, omega_ref=6.0)
    assert fractional_material_offset(state) == pytest.approx(-1.2 / 6.0)


def test_local_rate_collapses_to_calibration_times_local_activity():
    state = make_state(activity_ref=3.0, activity_local=7.5, calibration=2.0)
    assert state.gamma_t == pytest.approx(6.0)
    assert state.gamma_tau == pytest.approx(15.0)
    assert state.gamma_tau == pytest.approx((7.5 / 3.0) * state.gamma_t)
    assert state.gamma_tau_offset == pytest.approx(state.gamma_tau * state.seam_ratio)


def test_reference_cocycle_preserved_on_material_offset():
    state = make_state(omega_ref=4.0)
    omega_s = 10.0
    factor = reference_change_factor(4.0, omega_s)
    transformed = transform_material_offset(state.dtau_offset, 4.0, omega_s)
    assert factor == pytest.approx(0.4)
    assert transformed == pytest.approx(factor * state.dtau_offset)


def test_zero_curvature_gives_zero_material_offset():
    state = make_state(curvature=0.0)
    assert state.dtheta_offset == 0.0
    assert state.dt_offset == 0.0
    assert state.dtau_offset == 0.0
    assert state.gamma_tau_offset == 0.0


def test_positive_calibration_preserves_offset_sign():
    pos = make_state(curvature=0.3, dtheta_ref=1.0)
    neg = make_state(curvature=-0.3, dtheta_ref=1.0)
    assert pos.dtau_offset > 0.0
    assert neg.dtau_offset < 0.0


def test_two_material_clocks_share_fractional_offset_but_not_absolute_offset():
    x = make_state(activity_local=5.0)
    y = make_state(activity_local=12.0)
    assert fractional_material_offset(x) == pytest.approx(fractional_material_offset(y))
    assert x.dtau_offset != pytest.approx(y.dtau_offset)


def test_fail_closed_on_lapse_activity_mismatch():
    with pytest.raises(ValueError, match="lapse must equal"):
        material_offset_state(
            curvature=1.0,
            omega_ref=2.0,
            dtheta_ref=1.0,
            lapse=3.0,
            calibration=1.0,
            activity_ref=2.0,
            activity_local=4.0,
        )


@pytest.mark.parametrize("field,value", [
    ("omega_ref", 0.0),
    ("omega_ref", -1.0),
    ("lapse", 0.0),
    ("calibration", 0.0),
    ("activity_ref", 0.0),
    ("activity_local", -1.0),
])
def test_positive_carriers_fail_closed(field, value):
    kwargs = dict(
        curvature=1.0,
        omega_ref=2.0,
        dtheta_ref=1.0,
        lapse=2.0,
        calibration=1.0,
        activity_ref=2.0,
        activity_local=4.0,
    )
    kwargs[field] = value
    with pytest.raises(ValueError):
        material_offset_state(**kwargs)


def test_nonfinite_inputs_fail_closed():
    with pytest.raises(ValueError):
        make_state(curvature=math.nan)
