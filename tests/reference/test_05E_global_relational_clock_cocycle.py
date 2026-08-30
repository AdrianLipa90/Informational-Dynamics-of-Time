import math
from pathlib import Path

import pytest

from idt.global_relational_clock import (
    GlobalClockCocycleError,
    common_rate_rescaling,
    log_potential,
    ratio_from_certificate,
    reconstruct_global_clock_potential,
)


def sample_rates():
    return {"a": 1.2, "b": 0.8, "c": 2.0, "d": 1.5}


def sample_edges():
    a = sample_rates()
    return [
        ("a", "b", a["a"] / a["b"]),
        ("b", "c", a["b"] / a["c"]),
        ("c", "a", a["c"] / a["a"]),
        ("c", "d", a["c"] / a["d"]),
        ("a", "d", a["a"] / a["d"]),
    ]


def test_connected_consistent_graph_reconstructs_global_positive_clock_potential():
    cert = reconstruct_global_clock_potential(sample_edges(), reference="a")
    target = sample_rates()
    for node in target:
        assert cert.relative_rates[node] == pytest.approx(target[node] / target["a"])
        assert cert.relative_rates[node] > 0.0
    assert cert.max_relative_residual < 1e-12


def test_two_paths_give_same_ratio_and_triangle_cycle_product_is_one():
    cert = reconstruct_global_clock_potential(sample_edges(), reference="a")
    direct = ratio_from_certificate(cert, "c", "a")
    via_b = ratio_from_certificate(cert, "c", "b") * ratio_from_certificate(cert, "b", "a")
    assert direct == pytest.approx(via_b)
    cycle = (
        ratio_from_certificate(cert, "a", "b")
        * ratio_from_certificate(cert, "b", "c")
        * ratio_from_certificate(cert, "c", "a")
    )
    assert cycle == pytest.approx(1.0)


def test_log_cocycle_is_exact():
    cert = reconstruct_global_clock_potential(sample_edges(), reference="a")
    phi = log_potential(cert)
    for x, y, ratio in sample_edges():
        assert math.log(ratio) == pytest.approx(phi[x] - phi[y])
    loop_sum = (
        math.log(ratio_from_certificate(cert, "a", "b"))
        + math.log(ratio_from_certificate(cert, "b", "c"))
        + math.log(ratio_from_certificate(cert, "c", "a"))
    )
    assert loop_sum == pytest.approx(0.0, abs=1e-14)


def test_common_positive_rescaling_preserves_all_pairwise_lapse_ratios():
    cert = reconstruct_global_clock_potential(sample_edges(), reference="a")
    scaled = common_rate_rescaling(cert, 7.3)
    for x, y, ratio in sample_edges():
        assert scaled[x] / scaled[y] == pytest.approx(ratio)


def test_inconsistent_cycle_is_rejected():
    edges = sample_edges()
    x, y, ratio = edges[-1]
    edges[-1] = (x, y, ratio * 1.01)
    with pytest.raises(GlobalClockCocycleError, match="cycle|incompatible"):
        reconstruct_global_clock_potential(edges, reference="a")


def test_nonpositive_ratio_is_rejected():
    with pytest.raises(GlobalClockCocycleError, match="positive"):
        reconstruct_global_clock_potential([("a", "b", -1.0)], reference="a")


def test_disconnected_graph_is_rejected_for_one_global_reference_scale():
    edges = [("a", "b", 2.0), ("c", "d", 3.0)]
    with pytest.raises(GlobalClockCocycleError, match="disconnected"):
        reconstruct_global_clock_potential(edges, reference="a")


def test_tree_has_unique_reconstruction_relative_to_reference():
    edges = [("a", "b", 2.0), ("b", "c", 0.5), ("c", "d", 4.0)]
    cert = reconstruct_global_clock_potential(edges, reference="a")
    assert ratio_from_certificate(cert, "a", "d") == pytest.approx(2.0 * 0.5 * 4.0)


def test_05c_parent_and_05e_firewalls_are_source_bound():
    root = Path(__file__).resolve().parents[2]
    parent = (root / "formalism/05C_relational_lapse_interface.md").read_text(encoding="utf-8")
    doc = (root / "formalism/05E_global_relational_clock_cocycle.md").read_text(encoding="utf-8")
    assert "N_{x|s}=N_{x|r}N_{r|s}" in parent
    assert r"\prod_{e\in C}N_e=1" in doc
    assert "CAUSAL_TIME_FUNCTION_GATE_NEXT" in doc
    assert "global causal time/Cauchy foliation" in doc
