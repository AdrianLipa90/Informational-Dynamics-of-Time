import pytest

from idt.global_temporal_foliation import (
    TemporalFoliationError,
    certify_clock_domain,
    d_temporal_coframe,
    frobenius_residual,
    temporal_coframe,
)


def test_constant_lapse_temporal_coframe_has_zero_frobenius_residual():
    residual = frobenius_residual(
        1.25,
        [0.0, 0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0, 0.0],
    )
    assert residual == 0.0


def test_spatially_varying_lapse_still_satisfies_frobenius():
    residual = frobenius_residual(
        0.8,
        [0.2, -0.7, 1.1, 0.4],
        [1.0, 0.3, -0.2, 0.5],
        c=3.0,
    )
    assert residual == pytest.approx(0.0, abs=1e-12)


def test_generic_clock_covector_and_lapse_gradient_cancel_in_four_dimensions():
    residual = frobenius_residual(
        2.0,
        [1.3, -0.4, 0.9, -1.2],
        [0.7, -1.1, 0.6, 1.5],
    )
    assert residual == pytest.approx(0.0, abs=1e-12)


def test_temporal_coframe_is_positive_scalar_multiple_of_dt():
    dt = [1.0, -2.0, 0.5, 0.25]
    theta = temporal_coframe(1.5, dt, c=2.0)
    assert theta == pytest.approx(tuple(3.0 * value for value in dt))


def test_dtheta_matches_c_dN_wedge_dt_and_is_antisymmetric():
    dtheta = d_temporal_coframe(
        [0.0, 2.0, -1.0, 0.5],
        [1.0, 0.0, 0.0, 0.0],
        c=2.0,
    )
    for i in range(4):
        assert dtheta[i][i] == 0.0
        for j in range(4):
            assert dtheta[i][j] == pytest.approx(-dtheta[j][i])


def test_local_certificate_passes_without_promoting_global_clock():
    cert = certify_clock_domain(
        [0.7, 1.0, 1.9],
        [1.0, 0.8, 1.2],
        global_clock_scalar_supplied=False,
    )
    assert cert.positive_lapse
    assert cert.regular_clock
    assert cert.local_frobenius
    assert cert.kernel_preserved
    assert not cert.global_clock_scalar_supplied
    assert not cert.global_regular_foliation
    assert cert.cauchy_global_hyperbolicity == "OPEN"


def test_global_regular_foliation_promotes_only_when_global_clock_input_is_supplied():
    cert = certify_clock_domain(
        [0.7, 1.0, 1.9],
        [1.0, 0.8, 1.2],
        global_clock_scalar_supplied=True,
    )
    assert cert.global_clock_scalar_supplied
    assert cert.global_regular_foliation
    assert cert.cauchy_global_hyperbolicity == "OPEN"


@pytest.mark.parametrize("bad_lapse", [0.0, -1.0, float("inf"), float("nan")])
def test_nonpositive_or_nonfinite_lapse_fails_closed(bad_lapse):
    with pytest.raises(TemporalFoliationError):
        temporal_coframe(bad_lapse, [1.0, 0.0, 0.0, 0.0])


def test_zero_clock_differential_fails_closed():
    with pytest.raises(TemporalFoliationError):
        temporal_coframe(1.0, [0.0, 0.0, 0.0, 0.0])


def test_mismatched_gradient_dimension_fails_closed():
    with pytest.raises(TemporalFoliationError):
        d_temporal_coframe([1.0, 2.0, 3.0], [1.0, 0.0, 0.0, 0.0])


def test_sampled_domain_with_zero_dt_norm_fails_closed():
    with pytest.raises(TemporalFoliationError):
        certify_clock_domain([1.0, 1.2], [1.0, 0.0])
