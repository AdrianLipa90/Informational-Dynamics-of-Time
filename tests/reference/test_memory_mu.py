import math

import pytest

from src.idt.memory_mu import (
    MemoryMuError,
    ellipse_from_apses,
    mu_from_angular_momentum_and_latus_rectum,
    mu_from_circulation_rate,
    mu_from_period_and_semimajor_axis,
)


def test_ellipse_apses_recover_a_e_and_p():
    el = ellipse_from_apses(1.8, 4.2)
    assert el.semi_major_axis == pytest.approx(3.0)
    assert el.eccentricity == pytest.approx(0.4)
    assert el.semi_latus_rectum == pytest.approx(3.0 * (1.0 - 0.4**2))


def test_mu_recovered_from_h_and_p():
    mu = 2.3
    a = 3.0
    e = 0.4
    p = a * (1.0 - e**2)
    h = math.sqrt(mu * p)
    assert mu_from_angular_momentum_and_latus_rectum(h, p) == pytest.approx(mu, rel=1e-14)


def test_mu_recovered_from_period_and_semimajor_axis():
    mu = 2.3
    a = 3.0
    period = 2.0 * math.pi * math.sqrt(a**3 / mu)
    assert mu_from_period_and_semimajor_axis(period, a) == pytest.approx(mu, rel=1e-14)


def test_mu_recovered_from_memory_circulation_rate():
    mu = 2.3
    a = 3.0
    e = 0.4
    p = a * (1.0 - e**2)
    h = math.sqrt(mu * p)
    coupling = -0.37
    rate = coupling * h
    assert mu_from_circulation_rate(rate, coupling, p) == pytest.approx(mu, rel=1e-14)


def test_orientation_reversal_preserves_identified_mu():
    p = 2.4
    h = 1.7
    mu0 = mu_from_angular_momentum_and_latus_rectum(h, p)
    mu1 = mu_from_angular_momentum_and_latus_rectum(-h, p)
    assert mu1 == pytest.approx(mu0)


def test_invalid_inputs_fail_closed():
    with pytest.raises(MemoryMuError):
        ellipse_from_apses(2.0, 1.0)
    with pytest.raises(MemoryMuError):
        mu_from_angular_momentum_and_latus_rectum(1.0, 0.0)
    with pytest.raises(MemoryMuError):
        mu_from_period_and_semimajor_axis(0.0, 1.0)
    with pytest.raises(MemoryMuError):
        mu_from_circulation_rate(1.0, 0.0, 1.0)
