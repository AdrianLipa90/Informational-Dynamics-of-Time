import math

LN2 = math.log(2.0)


def information_nats(information_bits: float) -> float:
    return LN2 * information_bits


def temporal_information_curvature(information_bits: float, relational_area: float) -> float:
    if relational_area <= 0.0:
        raise ValueError("relational_area must be positive")
    return information_nats(information_bits) / relational_area


def curvature_rate(
    information_bits: float,
    d_information_bits: float,
    relational_area: float,
    d_relational_area: float,
) -> float:
    if relational_area <= 0.0:
        raise ValueError("relational_area must be positive")
    j = information_nats(information_bits)
    dj = information_nats(d_information_bits)
    return dj / relational_area - j * d_relational_area / (relational_area**2)


def test_bit_to_nat_conversion():
    assert abs(information_nats(1.0) - LN2) < 1e-15


def test_inverse_square_scaling():
    base = temporal_information_curvature(3.0, 2.0)
    scaled = temporal_information_curvature(3.0, 18.0)
    assert abs(scaled - base / 9.0) < 1e-15


def test_exact_quotient_rate_against_symmetric_difference():
    information_bits = 2.3
    d_information_bits = -0.4
    area = 5.2
    d_area = 0.7
    analytic = curvature_rate(information_bits, d_information_bits, area, d_area)
    eps = 1e-7
    forward = temporal_information_curvature(
        information_bits + d_information_bits * eps,
        area + d_area * eps,
    )
    backward = temporal_information_curvature(
        information_bits - d_information_bits * eps,
        area - d_area * eps,
    )
    numeric = (forward - backward) / (2.0 * eps)
    assert abs(analytic - numeric) < 1e-8


def test_constant_area_inherits_information_descent():
    assert curvature_rate(2.0, -0.1, 4.0, 0.0) < 0.0


def test_zero_information_gives_zero_inverse_area_scalar():
    assert temporal_information_curvature(0.0, 3.0) == 0.0


def test_positive_area_is_required():
    try:
        temporal_information_curvature(1.0, 0.0)
    except ValueError:
        return
    raise AssertionError("zero relational area must fail closed")
