import math

import numpy as np
import pytest

from idt.half_frame_continuum import (
    HalfFrameContinuumError,
    continuum_defect_density,
    continuum_fuzzy_density,
    continuum_profiles,
    gauge_transform_samples,
    integrated_fuzzy_measure,
    weighted_defect_energy,
)


def _smooth_sample(n: int):
    x = np.linspace(0.0, 1.0, n)
    h = float(x[1] - x[0])

    def radius(z):
        return 1.0 + 0.2 * np.sin(2.0 * np.pi * z)

    def radius_prime(z):
        return 0.4 * np.pi * np.cos(2.0 * np.pi * z)

    def phase(z):
        return 0.3 * np.sin(2.0 * np.pi * z)

    def phase_prime(z):
        return 0.6 * np.pi * np.cos(2.0 * np.pi * z)

    def connection(z):
        return 0.1 * np.cos(2.0 * np.pi * z)

    amplitudes = np.sqrt(h) * radius(x) * np.exp(1j * phase(x))
    seams = 0.1 / (2.0 * np.pi) * (
        np.sin(2.0 * np.pi * x[1:]) - np.sin(2.0 * np.pi * x[:-1])
    )
    mids = 0.5 * (x[:-1] + x[1:])
    density_target = radius(mids) ** 2
    gradient_target = radius_prime(mids) ** 2 + (
        radius(mids) * (phase_prime(mids) - connection(mids))
    ) ** 2
    return x, h, amplitudes, seams, mids, density_target, gradient_target


def test_constant_covariantly_locked_field_is_exact():
    h = 0.125
    k = 0.7
    x0 = 0.25
    left = math.sqrt(h) * np.exp(1j * k * x0)
    right = math.sqrt(h) * np.exp(1j * k * (x0 + h))
    seam = k * h
    assert math.isclose(continuum_fuzzy_density(left, right, seam, h), 1.0, rel_tol=0.0, abs_tol=1e-14)
    assert continuum_defect_density(left, right, seam, h) < 1e-27


def test_fuzzy_density_converges_second_order_at_midpoints():
    errors = []
    for n in (33, 65, 129, 257):
        _, h, amplitudes, seams, _, target, _ = _smooth_sample(n)
        profile = continuum_profiles(amplitudes, seams, h)
        errors.append(float(np.max(np.abs(profile.fuzzy_density - target))))
    ratios = np.asarray(errors[:-1]) / np.asarray(errors[1:])
    assert np.all(ratios > 3.8)
    assert errors[-1] < 4e-5


def test_defect_density_converges_second_order_to_covariant_gradient():
    errors = []
    for n in (33, 65, 129, 257):
        _, h, amplitudes, seams, _, _, target = _smooth_sample(n)
        profile = continuum_profiles(amplitudes, seams, h)
        errors.append(float(np.max(np.abs(profile.defect_density - target))))
    ratios = np.asarray(errors[:-1]) / np.asarray(errors[1:])
    assert np.all(ratios > 3.8)
    assert errors[-1] < 3e-4


def test_fuzzy_quality_tends_to_one_in_smooth_occupied_bulk():
    deficits = []
    for n in (33, 65, 129, 257):
        _, h, amplitudes, seams, _, _, _ = _smooth_sample(n)
        profile = continuum_profiles(amplitudes, seams, h)
        deficits.append(float(np.max(1.0 - profile.fuzzy_quality)))
    ratios = np.asarray(deficits[:-1]) / np.asarray(deficits[1:])
    assert np.all(ratios > 3.7)
    assert deficits[-1] < 2e-4


def test_gauge_transform_preserves_discrete_continuum_profiles():
    x, h, amplitudes, seams, _, _, _ = _smooth_sample(65)
    chi = 0.23 * np.sin(4.0 * np.pi * x) + 0.11 * x
    transformed_state, transformed_seams = gauge_transform_samples(amplitudes, seams, chi)
    before = continuum_profiles(amplitudes, seams, h)
    after = continuum_profiles(transformed_state, transformed_seams, h)
    np.testing.assert_allclose(after.fuzzy_density, before.fuzzy_density, rtol=0.0, atol=2e-14)
    np.testing.assert_allclose(after.defect_density, before.defect_density, rtol=0.0, atol=2e-11)
    np.testing.assert_allclose(after.fuzzy_quality, before.fuzzy_quality, rtol=0.0, atol=2e-14)


def test_integrated_fuzzy_measure_converges_to_continuum_norm():
    target = 1.02
    errors = []
    for n in (33, 65, 129, 257):
        _, h, amplitudes, seams, _, _, _ = _smooth_sample(n)
        profile = continuum_profiles(amplitudes, seams, h)
        value = integrated_fuzzy_measure(profile.fuzzy_density, h)
        errors.append(abs(value - target))
    ratios = np.asarray(errors[:-1]) / np.asarray(errors[1:])
    assert np.all(ratios > 3.8)
    assert errors[-1] < 1.3e-5


def test_weighted_defect_energy_converges_to_heterogeneous_continuum_form():
    target_grid = np.linspace(0.0, 1.0, 200001)
    radius = 1.0 + 0.2 * np.sin(2.0 * np.pi * target_grid)
    radius_prime = 0.4 * np.pi * np.cos(2.0 * np.pi * target_grid)
    phase_prime = 0.6 * np.pi * np.cos(2.0 * np.pi * target_grid)
    connection = 0.1 * np.cos(2.0 * np.pi * target_grid)
    mobility = 1.2 + 0.3 * np.cos(2.0 * np.pi * target_grid)
    energy_density = mobility * (
        radius_prime**2 + (radius * (phase_prime - connection)) ** 2
    )
    target = float(np.trapezoid(energy_density, target_grid))

    errors = []
    for n in (33, 65, 129, 257):
        _, h, amplitudes, seams, mids, _, _ = _smooth_sample(n)
        edge_mobility = 1.2 + 0.3 * np.cos(2.0 * np.pi * mids)
        profile = continuum_profiles(amplitudes, seams, h)
        value = weighted_defect_energy(profile.defect_density, edge_mobility, h)
        errors.append(abs(value - target))
    ratios = np.asarray(errors[:-1]) / np.asarray(errors[1:])
    assert np.all(ratios > 3.8)
    assert errors[-1] < 2e-4


@pytest.mark.parametrize(
    "call",
    [
        lambda: continuum_fuzzy_density(1.0, 1.0, 0.0, 0.0),
        lambda: continuum_defect_density(1.0, 1.0, 0.0, -1.0),
        lambda: continuum_profiles([1.0, 0.0], [], 0.1),
        lambda: weighted_defect_energy([1.0], [0.0], 0.1),
    ],
)
def test_half_frame_continuum_fails_closed(call):
    with pytest.raises(HalfFrameContinuumError):
        call()
