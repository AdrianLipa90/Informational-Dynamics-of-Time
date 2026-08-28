import cmath
import itertools
import math


def omega():
    return cmath.exp(2j * math.pi / 3.0)


def z_nu(state):
    w = omega()
    se, sm, st = state
    return se + w * sm + (w ** 2) * st


def test_three_bipolar_flavours_give_eight_basis_sectors():
    sectors = list(itertools.product((1, -1), repeat=3))
    assert len(sectors) == 8
    assert len(set(sectors)) == 8


def test_root_of_unity_closure():
    w = omega()
    assert abs(1.0 + w + w ** 2) < 1e-12


def test_two_aligned_sectors_have_zero_coherent_projection():
    assert abs(z_nu((1, 1, 1))) < 1e-12
    assert abs(z_nu((-1, -1, -1))) < 1e-12


def test_other_six_sectors_have_equal_projection_magnitude_two():
    sectors = list(itertools.product((1, -1), repeat=3))
    nonzero = [s for s in sectors if s not in ((1, 1, 1), (-1, -1, -1))]
    assert len(nonzero) == 6
    for state in nonzero:
        assert math.isclose(abs(z_nu(state)), 2.0, rel_tol=1e-12, abs_tol=1e-12)


def matmul(A, B):
    rows, inner, cols = len(A), len(B), len(B[0])
    return [[sum(A[i][k] * B[k][j] for k in range(inner)) for j in range(cols)] for i in range(rows)]


def dagger(A):
    return [[A[j][i].conjugate() for j in range(len(A))] for i in range(len(A[0]))]


def test_generic_unitary_flavour_rotation_preserves_norm():
    # Simple exact 1-2 rotation embedded in U(3).
    c = math.cos(0.37)
    s = math.sin(0.37)
    U = [[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]]
    a = [0.3 + 0.4j, -0.2 + 0.1j, 0.5 - 0.3j]
    ap = [sum(U[i][j] * a[j] for j in range(3)) for i in range(3)]
    n0 = sum(abs(x) ** 2 for x in a)
    n1 = sum(abs(x) ** 2 for x in ap)
    assert math.isclose(n0, n1, rel_tol=1e-12, abs_tol=1e-12)


def test_neutrino_charge_operator_is_invariant_under_any_flavour_rotation():
    c = math.cos(0.61)
    s = math.sin(0.61)
    U = [[c, 0.0, s], [0.0, 1.0, 0.0], [-s, 0.0, c]]
    Q = [[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]]
    transformed = matmul(matmul(dagger(U), Q), U)
    assert transformed == Q


def test_charge_degenerate_flavours_can_mix_without_changing_charge_operator():
    c = math.cos(0.29)
    s = math.sin(0.29)
    U = [[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]]
    q = -1.0
    Q = [[q, 0.0, 0.0], [0.0, q, 0.0], [0.0, 0.0, q]]
    transformed = matmul(matmul(dagger(U), Q), U)
    for i in range(3):
        for j in range(3):
            assert abs(transformed[i][j] - Q[i][j]) < 1e-12


def test_nondegenerate_charge_rotation_fails_charge_preservation_gate():
    c = math.cos(0.41)
    s = math.sin(0.41)
    U = [[c, s, 0.0], [-s, c, 0.0], [0.0, 0.0, 1.0]]
    Q = [[0.0, 0.0, 0.0], [0.0, -1.0, 0.0], [0.0, 0.0, -1.0]]
    transformed = matmul(matmul(dagger(U), Q), U)
    defect = max(abs(transformed[i][j] - Q[i][j]) for i in range(3) for j in range(3))
    assert defect > 1e-6
