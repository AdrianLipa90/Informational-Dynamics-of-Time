from src.idt.harmonic_scheduler import (
    admission_band,
    band,
    eligible_tick,
    jitter_adjusted_band,
    next_eligible_tick,
)


def test_dyadic_workload_bands_are_disjoint():
    for tick in range(1, 1025):
        matches = [k for k in range(1, 8) if eligible_tick(tick, k)]
        assert len(matches) <= 1


def test_expected_phase_slots():
    assert [n for n in range(1, 9) if eligible_tick(n, 1)] == [1, 3, 5, 7]
    assert [n for n in range(1, 9) if eligible_tick(n, 2)] == [2, 6]
    assert [n for n in range(1, 17) if eligible_tick(n, 3)] == [4, 12]


def test_deep_boundary_is_quiet_slot():
    assert admission_band(128, max_band=7) is None
    assert admission_band(64, max_band=7) == 7


def test_next_slot_and_jitter_demotion():
    assert next_eligible_tick(6, 3) == 12
    assert jitter_adjusted_band(4, observed_jitter_s=0.09, jitter_limit_s=0.05) == 5
    assert jitter_adjusted_band(4, observed_jitter_s=0.01, jitter_limit_s=0.05) == 4


def test_base_period():
    b0 = band(0)
    assert abs(b0.frequency_hz - 7.83) < 1e-12
    assert abs(b0.period_s - (1.0 / 7.83)) < 1e-12
