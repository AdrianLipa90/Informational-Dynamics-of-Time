import math
import pytest


def _charge(j, v):
    if len(j) != len(v) or not j:
        raise ValueError("common non-empty cell partition required")
    if any(x <= 0.0 for x in v):
        raise ValueError("cell measures must be positive")
    return sum(float(ja) * float(va) for ja, va in zip(j, v))


def _defects(j_theta, v_theta, j_q, v_q):
    if not (len(j_theta) == len(v_theta) == len(j_q) == len(v_q)) or not j_theta:
        raise ValueError("common cell IDs required")
    q_theta = _charge(j_theta, v_theta)
    q_sigma = _charge(j_q, v_q)
    if q_theta <= 0.0:
        raise ValueError("positive Noether sector required")
    delta_j = sum(v * abs(jq - jt) for jt, jq, v in zip(j_theta, j_q, v_q)) / q_theta
    delta_v = sum(abs(vq - vt) * abs(jt) for jt, vt, vq in zip(j_theta, v_theta, v_q)) / q_theta
    delta_sigma = abs(q_sigma - q_theta) / q_theta
    return q_theta, q_sigma, delta_j, delta_v, delta_sigma


def _profile(j, v):
    q = _charge(j, v)
    if q <= 0.0:
        raise ValueError("positive carrier required")
    return [ja * va / q for ja, va in zip(j, v)]


def test_exact_current_and_measure_binding_closes_extensive_charge():
    j = [1.0, 2.0, 3.0]
    v = [0.5, 1.0, 1.5]
    q_theta, q_sigma, delta_j, delta_v, delta_sigma = _defects(j, v, j, v)
    assert q_sigma == q_theta
    assert delta_j == 0.0
    assert delta_v == 0.0
    assert delta_sigma == 0.0


def test_global_charge_defect_is_bounded_by_local_current_plus_measure_defects():
    rows = [
        ([1.0, 2.0], [1.0, 2.0], [1.2, 1.8], [1.0, 2.0]),
        ([0.5, 1.5, 2.0], [1.0, 1.0, 2.0], [0.6, 1.4, 2.2], [1.1, 0.9, 1.8]),
        ([3.0, 1.0], [0.4, 2.0], [2.5, 1.2], [0.5, 1.8]),
    ]
    for j_theta, v_theta, j_q, v_q in rows:
        _, _, delta_j, delta_v, delta_sigma = _defects(j_theta, v_theta, j_q, v_q)
        assert delta_sigma <= delta_j + delta_v + 1e-15


def test_current_mismatch_is_detected_even_when_measure_matches():
    _, _, delta_j, delta_v, delta_sigma = _defects(
        [1.0, 2.0], [1.0, 1.0], [1.5, 2.0], [1.0, 1.0]
    )
    assert delta_j > 0.0
    assert delta_v == 0.0
    assert delta_sigma > 0.0


def test_measure_mismatch_is_detected_even_when_current_matches():
    _, _, delta_j, delta_v, delta_sigma = _defects(
        [1.0, 2.0], [1.0, 1.0], [1.0, 2.0], [1.2, 0.8]
    )
    assert delta_j == 0.0
    assert delta_v > 0.0
    assert delta_sigma > 0.0


def test_equal_integrated_charge_does_not_imply_local_current_identity():
    # Equal totals by cancellation: the local current defect must remain visible.
    j_theta = [1.0, 1.0]
    j_q = [1.5, 0.5]
    v = [1.0, 1.0]
    q_theta, q_sigma, delta_j, delta_v, delta_sigma = _defects(j_theta, v, j_q, v)
    assert q_sigma == q_theta
    assert delta_sigma == 0.0
    assert delta_j > 0.0
    assert delta_v == 0.0


def test_exact_local_binding_preserves_normalized_profile():
    j = [1.0, 3.0, 2.0]
    v = [0.25, 0.5, 1.25]
    p_theta = _profile(j, v)
    p_q = _profile(j, v)
    assert p_q == p_theta
    assert math.isclose(sum(p_q), 1.0, rel_tol=0.0, abs_tol=1e-15)


def test_partition_and_positive_measure_gates_fail_closed():
    with pytest.raises(ValueError, match="common cell IDs"):
        _defects([1.0, 2.0], [1.0, 1.0], [1.0], [1.0])
    with pytest.raises(ValueError, match="cell measures must be positive"):
        _defects([1.0], [1.0], [1.0], [0.0])
    with pytest.raises(ValueError, match="positive Noether sector"):
        _defects([-1.0], [1.0], [-1.0], [1.0])
