from fractions import Fraction


def normalize(values):
    total = sum(values)
    assert total > 0
    return tuple(Fraction(v, total) for v in values)


def lift(profile, scale):
    return tuple(scale * p for p in profile)


def relative_l1_defect(original, reconstructed):
    numerator = sum(abs(Fraction(a) - Fraction(b)) for a, b in zip(original, reconstructed))
    denominator = sum(abs(Fraction(a)) for a in original)
    return numerator / denominator


def test_positive_ray_projects_to_one_simplex_point():
    q = (2, 3, 5)
    assert normalize(q) == normalize(tuple(7 * x for x in q))


def test_analytic_holonomy_formula_is_exact():
    q = (2, 3, 5)
    total = sum(q)
    p = normalize(q)
    for scale in (1, 4, 10, 17):
        measured = relative_l1_defect(q, lift(p, scale))
        analytic = abs(Fraction(1) - Fraction(scale, total))
        assert measured == analytic


def test_exact_inverse_transport_uses_extensive_coordinate():
    q = (2, 3, 5)
    assert lift(normalize(q), sum(q)) == tuple(Fraction(v) for v in q)


def test_constructive_two_scale_probe_matches_rfc_receipt_values():
    q1 = (2, 3, 5)
    q2 = (4, 6, 10)
    assert normalize(q1) == normalize(q2)
    assert relative_l1_defect(q1, lift(normalize(q1), 1)) == Fraction(9, 10)
    assert relative_l1_defect(q2, lift(normalize(q2), 1)) == Fraction(19, 20)


def test_source_mass_factorization_shape_times_scale():
    q = (2, 3, 5)
    epsilon_over_c2 = Fraction(7, 11)
    q_total = sum(q)
    p = normalize(q)
    m_total = epsilon_over_c2 * q_total

    direct = tuple(epsilon_over_c2 * Fraction(v) for v in q)
    factorized = tuple(m_total * x for x in p)
    assert direct == factorized
