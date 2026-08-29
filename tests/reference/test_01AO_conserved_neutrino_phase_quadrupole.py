import math

import numpy as np
import pytest

from idt.neutrino_conserved_quadrupole import (
    integrated_four_momentum_exchange_rate,
    phase_quadrupole_source,
)
from idt.qhtri_neutrino_gravity import project_tt


def polarization_coordinates(spatial):
    t = np.asarray(spatial, dtype=float)
    return 0.5 * (t[0, 0] - t[1, 1]), t[0, 1]


def test_phase_quadrupole_preserves_total_energy_and_zero_momentum():
    for phi in np.linspace(0.0, 2.0 * math.pi, 17):
        q = phase_quadrupole_source(20.0, 3.0, float(phi))
        assert math.isclose(q.source.total_energy_joule, 20.0, rel_tol=0.0, abs_tol=1e-12)
        assert np.linalg.norm(q.source.energy_flux_vector_joule) < 1e-12
        assert all(w >= 0.0 for w in q.pair_energies_joule)


def test_phase_maps_exactly_to_plus_cross_tt_coordinates():
    energy = 40.0
    amp = 4.0
    for phi in np.linspace(-1.2, 1.3, 21):
        q = phase_quadrupole_source(energy, amp, float(phi))
        tt = project_tt(q.source.spatial_stress_joule, (0.0, 0.0, 1.0))
        plus, cross = polarization_coordinates(tt)
        assert math.isclose(plus, amp * math.cos(2.0 * phi), rel_tol=1e-12, abs_tol=1e-12)
        assert math.isclose(cross, amp * math.sin(2.0 * phi), rel_tol=1e-12, abs_tol=1e-12)


def test_tt_norm_is_phase_invariant_for_fixed_modulation_amplitude():
    amp = 2.5
    norms = []
    for phi in np.linspace(0.0, math.pi, 13):
        q = phase_quadrupole_source(30.0, amp, float(phi))
        tt = np.asarray(project_tt(q.source.spatial_stress_joule, (0.0, 0.0, 1.0)))
        norms.append(float(np.linalg.norm(tt)))
    assert max(abs(n - math.sqrt(2.0) * amp) for n in norms) < 1e-12


def test_phase_update_needs_zero_external_integrated_four_force():
    a = phase_quadrupole_source(25.0, 2.0, 0.1).source
    b = phase_quadrupole_source(25.0, 2.0, 1.1).source
    rate = integrated_four_momentum_exchange_rate(a, b, 0.01)
    assert max(abs(x) for x in rate) < 1e-20


def test_energy_change_requires_nonzero_external_time_component():
    a = phase_quadrupole_source(20.0, 2.0, 0.2).source
    b = phase_quadrupole_source(22.0, 2.0, 0.2).source
    rate = integrated_four_momentum_exchange_rate(a, b, 0.5)
    assert rate[0] > 0.0


def test_phase_quadrupole_validation_fails_closed():
    with pytest.raises(ValueError):
        phase_quadrupole_source(0.0, 0.0, 0.0)
    with pytest.raises(ValueError):
        phase_quadrupole_source(10.0, -1.0, 0.0)
    with pytest.raises(ValueError):
        phase_quadrupole_source(10.0, 2.6, 0.0)
    q = phase_quadrupole_source(10.0, 1.0, 0.0).source
    with pytest.raises(ValueError):
        integrated_four_momentum_exchange_rate(q, q, 0.0)
