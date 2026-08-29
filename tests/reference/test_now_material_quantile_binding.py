import math

import numpy as np
import pytest

from idt.now_material_quantile_binding import (
    NowMaterialBindingError,
    bind_concurrent_now_to_quantiles,
    bind_serial_now_to_quantile,
    exchange_fixed_point_residual,
    mirror_quantile_residual,
    reflected_mass_fraction,
    symmetric_density_about,
    symmetric_mass_fraction,
)
from idt.relational_precedence import RelationalEdge, unfold_serial_history


def _gaussian(center: float = 0.0):
    x = np.linspace(-10.0, 10.0, 5001)
    rho = np.exp(-0.5 * (x - center) ** 2)
    return x, rho


def _serial(event_weights=(1.0, 1.0, 1.0)):
    edges = [
        RelationalEdge("e1", "A", "B", 0.2, event_weights[0]),
        RelationalEdge("e2", "B", "A", 0.3, event_weights[1]),
        RelationalEdge("e3", "A", "C", 0.4, event_weights[2]),
    ]
    return unfold_serial_history("A", edges)


def test_exchange_involution_has_unique_half_fixed_point():
    assert symmetric_mass_fraction() == 0.5
    assert exchange_fixed_point_residual(0.5) == 0.0
    for q in (0.1, 0.25, 0.4, 0.6, 0.75, 0.9):
        assert reflected_mass_fraction(reflected_mass_fraction(q)) == pytest.approx(q)
        assert exchange_fixed_point_residual(q) != 0.0


def test_mirror_symmetric_density_pairs_quantiles_about_center():
    center = 1.25
    x = np.linspace(center - 8.0, center + 8.0, 4001)
    rho = np.exp(-0.5 * (x - center) ** 2)
    assert symmetric_density_about(x, rho, center)
    for q in (0.1, 0.2, 0.35, 0.5):
        assert abs(mirror_quantile_residual(x, rho, center, q)) < 1e-12


def test_serial_binding_preserves_prefix_identity_through_state_recurrence():
    occurrences = _serial()
    x, rho = _gaussian(0.0)
    current = 0.75 * rho
    bound = bind_serial_now_to_quantile(occurrences, x, rho, current)
    assert bound.occurrence.prefix == ("e1", "e2", "e3")
    assert bound.occurrence.state == "C"
    assert bound.occurrence.theta == pytest.approx(0.9)
    assert abs(bound.material_front.position) < 1e-12
    assert bound.material_front.theta_velocity == pytest.approx(0.75, abs=2e-12)


def test_wave_translation_moves_material_coordinate_while_event_identity_is_retained():
    occurrences = _serial()
    x0, rho0 = _gaussian(-1.0)
    x1, rho1 = _gaussian(2.0)
    b0 = bind_serial_now_to_quantile(occurrences, x0, rho0, np.zeros_like(rho0))
    b1 = bind_serial_now_to_quantile(occurrences, x1, rho1, np.zeros_like(rho1))
    assert b0.occurrence.prefix == b1.occurrence.prefix
    assert b0.material_front.position == pytest.approx(-1.0, abs=2e-12)
    assert b1.material_front.position == pytest.approx(2.0, abs=2e-12)


def test_realization_change_moves_now_identity_while_material_family_is_retained():
    x, rho = _gaussian(0.5)
    current = np.zeros_like(rho)
    full = bind_serial_now_to_quantile(_serial((1.0, 1.0, 1.0)), x, rho, current)
    earlier = bind_serial_now_to_quantile(_serial((1.0, 1.0, 0.0)), x, rho, current)
    assert full.occurrence.prefix == ("e1", "e2", "e3")
    assert earlier.occurrence.prefix == ("e1", "e2")
    assert full.material_front.position == pytest.approx(earlier.material_front.position, abs=1e-14)


def test_concurrent_binding_retains_all_frontier_ids_branchwise():
    xa, rhoa = _gaussian(-2.0)
    xb, rhob = _gaussian(3.0)
    fields = {
        "left": (xa, rhoa, np.zeros_like(rhoa)),
        "right": (xb, rhob, np.zeros_like(rhob)),
    }
    bound = bind_concurrent_now_to_quantiles(("left", "right"), fields)
    assert set(bound) == {"left", "right"}
    assert bound["left"].position == pytest.approx(-2.0, abs=2e-12)
    assert bound["right"].position == pytest.approx(3.0, abs=2e-12)
    assert all(front.mass_fraction == 0.5 for front in bound.values())


@pytest.mark.parametrize(
    "call",
    [
        lambda: reflected_mass_fraction(0.0),
        lambda: exchange_fixed_point_residual(1.0),
        lambda: bind_serial_now_to_quantile(_serial((0.0, 0.0, 0.0)), [0.0, 1.0], [1.0, 1.0], [0.0, 0.0]),
        lambda: bind_concurrent_now_to_quantiles(("a", "b"), {"a": ([0.0, 1.0], [1.0, 1.0], [0.0, 0.0])}),
    ],
)
def test_binding_gate_fails_closed(call):
    with pytest.raises(NowMaterialBindingError):
        call()
