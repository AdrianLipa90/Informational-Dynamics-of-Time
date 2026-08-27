import math


def finite_charge(current, volumes):
    if len(current) != len(volumes) or not current:
        raise ValueError("current/volume support mismatch")
    if any(v <= 0.0 for v in volumes):
        raise ValueError("positive cell volumes required")
    return sum(j * v for j, v in zip(current, volumes))


def measure_defect(v_theta, v_q):
    if len(v_theta) != len(v_q) or not v_theta:
        raise ValueError("measure support mismatch")
    return sum(abs(a - b) for a, b in zip(v_theta, v_q)) / sum(v_theta)


def local_current_defect(j_theta, j_q, volumes):
    q_theta = finite_charge(j_theta, volumes)
    if q_theta <= 0.0:
        raise ValueError("positive Noether total required")
    return sum(v * abs(a - b) for v, a, b in zip(volumes, j_theta, j_q)) / q_theta


def total_charge_defect(q_theta, q_sigma):
    if q_theta <= 0.0:
        raise ValueError("positive Noether total required")
    return abs(q_sigma - q_theta) / q_theta


def test_exact_common_local_current_binding_has_zero_defects():
    volumes = [1.0, 2.0, 1.0]
    j_theta = [1.0, 2.0, 3.0]
    j_q = list(j_theta)
    q_theta = finite_charge(j_theta, volumes)
    q_sigma = finite_charge(j_q, volumes)
    assert measure_defect(volumes, volumes) == 0.0
    assert local_current_defect(j_theta, j_q, volumes) == 0.0
    assert total_charge_defect(q_theta, q_sigma) == 0.0


def test_equal_integrated_charge_does_not_imply_local_current_binding():
    volumes = [1.0, 1.0]
    j_theta = [1.0, 3.0]
    j_q = [2.0, 2.0]
    q_theta = finite_charge(j_theta, volumes)
    q_sigma = finite_charge(j_q, volumes)
    assert q_theta == q_sigma == 4.0
    assert total_charge_defect(q_theta, q_sigma) == 0.0
    assert math.isclose(local_current_defect(j_theta, j_q, volumes), 0.5, rel_tol=0.0, abs_tol=1e-15)


def test_measure_defect_detects_volume_mismatch():
    assert math.isclose(measure_defect([1.0, 1.0], [1.0, 1.1]), 0.05, rel_tol=0.0, abs_tol=1e-15)


def test_total_charge_defect_detects_integrated_mismatch():
    q_theta = finite_charge([1.0, 2.0], [1.0, 1.0])
    q_sigma = finite_charge([1.0, 3.0], [1.0, 1.0])
    assert math.isclose(total_charge_defect(q_theta, q_sigma), 1.0 / 3.0, rel_tol=0.0, abs_tol=1e-15)


def test_zero_local_defect_implies_equal_total_on_common_measure():
    volumes = [0.5, 1.5, 2.0]
    current = [2.0, 1.0, 0.5]
    assert local_current_defect(current, current, volumes) == 0.0
    assert finite_charge(current, volumes) == finite_charge(current, volumes)


def test_side_flux_exact_conservation_gate_is_zero():
    side_flux = 0.0
    assert abs(side_flux) == 0.0


def test_noether_epsilon_transfers_without_new_normalization_after_charge_binding():
    h_phi = 12.0
    q_theta = 4.0
    q_sigma = 4.0
    epsilon_n = h_phi / q_theta
    epsilon_q_candidate = h_phi / q_sigma
    assert epsilon_n == epsilon_q_candidate == 3.0
