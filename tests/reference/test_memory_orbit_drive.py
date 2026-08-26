from __future__ import annotations

import math

from src.idt.memory_orbit import (
    cycle_memory_affinity_bits,
    cycle_memory_drive,
    memory_edge_drive,
    signed_polygon_area,
)


def test_memory_edge_drive_is_antisymmetric() -> None:
    a = 1.2 + 0.3j
    b = -0.4 + 1.1j
    assert math.isclose(memory_edge_drive(a, b), -memory_edge_drive(b, a), abs_tol=1e-14)


def test_memory_cycle_drive_equals_twice_signed_area_times_coupling() -> None:
    orbit = [0.0 + 0.0j, 2.0 + 0.0j, 2.0 + 1.0j, 0.0 + 1.0j]
    coupling = 0.7
    measured = cycle_memory_drive(orbit, coupling=coupling)
    expected = 2.0 * coupling * signed_polygon_area(orbit)
    assert math.isclose(measured, expected, rel_tol=0.0, abs_tol=1e-14)


def test_reversing_memory_orbit_flips_circulation() -> None:
    orbit = [1.0 + 0.0j, 0.0 + 1.0j, -1.0 + 0.0j]
    fwd = cycle_memory_drive(orbit)
    rev = cycle_memory_drive(list(reversed(orbit)))
    assert math.isclose(fwd, -rev, rel_tol=0.0, abs_tol=1e-14)


def test_collinear_ray_memory_has_zero_drive() -> None:
    orbit = [1.0 + 0.0j, 2.0 + 0.0j, 4.0 + 0.0j]
    assert math.isclose(cycle_memory_drive(orbit), 0.0, abs_tol=1e-14)


def test_cycle_memory_affinity_is_drive_over_ln2() -> None:
    orbit = [1.0 + 0.0j, 0.0 + 1.0j, -1.0 + 0.0j]
    drive = cycle_memory_drive(orbit, coupling=0.25)
    affinity = cycle_memory_affinity_bits(orbit, coupling=0.25)
    assert math.isclose(affinity, drive / math.log(2.0), rel_tol=0.0, abs_tol=1e-14)
