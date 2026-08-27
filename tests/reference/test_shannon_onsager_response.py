import math
import numpy as np
import pytest
from src.idt.shannon_onsager_response import *

def db_example():
    pi=np.array([0.2,0.3,0.5])
    C=np.array([[0,0.03,0.04],[0.03,0,0.05],[0.04,0.05,0]])
    Q=C/pi[:,None]; np.fill_diagonal(Q,0); np.fill_diagonal(Q,-Q.sum(axis=1))
    return pi,Q

def test_exact_factorization_detailed_balance():
    pi,Q=db_example(); p=np.array([0.62,0.28,0.10])
    a=audit_onsager_factorization(p,pi,Q)
    assert a.factorization_defect < 1e-12
    assert a.dissipation_rate_bits < 0

def test_tensor_is_symmetric_psd_and_mass_conserving():
    pi,Q=db_example(); p=np.array([0.62,0.28,0.10]); G=shannon_onsager_tensor_bits(p,pi,Q)
    assert np.linalg.norm(G-G.T) < 1e-13
    assert np.linalg.eigvalsh(G).min() > -1e-13
    assert np.linalg.norm(G@np.ones(3)) < 1e-13

def test_bit_factor_ln2_is_required():
    pi,Q=db_example(); p=np.array([0.62,0.28,0.10]); G=shannon_onsager_tensor_bits(p,pi,Q)
    grad=kl_gradient_bits(p,pi); v=master_velocity(p,Q)
    assert np.linalg.norm(v+G@grad) < 1e-12
    assert np.linalg.norm(v+(G/math.log(2))*grad) > 1e-3

def test_uniform_symmetric_equilibrium_reduces_to_mobility_laplacian():
    M=np.array([[0,1.2,0.4],[1.2,0,0.7],[0.4,0.7,0]])
    Q=symmetric_generator_from_mobility(M); n=3; u=np.full(n,1/n)
    G=shannon_onsager_tensor_bits(u,u,Q); K=graph_stiffness(M)
    assert np.linalg.norm(G-(math.log(2)/n)*K) < 1e-12

def test_random_exact_factorization():
    rng=np.random.default_rng(20260827)
    for _ in range(500):
        n=int(rng.integers(2,8)); pi=rng.dirichlet(np.ones(n)); B=rng.uniform(0.01,1.0,size=(n,n)); C=(B+B.T)/2; np.fill_diagonal(C,0)
        Q=C/pi[:,None]; np.fill_diagonal(Q,0); np.fill_diagonal(Q,-Q.sum(axis=1)); p=rng.dirichlet(np.ones(n))
        a=audit_onsager_factorization(p,pi,Q)
        assert a.factorization_defect < 2e-11
        assert a.dissipation_rate_bits < 1e-12
        assert a.mass_null_defect < 1e-11

def test_non_detailed_balance_fails_closed():
    pi=np.array([1/3]*3); Q=np.array([[-1,1,0],[0,-1,1],[1,0,-1]],dtype=float)
    with pytest.raises(ShannonOnsagerError): shannon_onsager_tensor_bits([0.5,0.3,0.2],pi,Q)

def test_invalid_inputs_fail_closed():
    with pytest.raises(ShannonOnsagerError): logarithmic_mean(0,1)
