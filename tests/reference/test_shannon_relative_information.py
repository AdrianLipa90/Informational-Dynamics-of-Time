import numpy as np
import pytest
from src.idt.shannon_relative_information import *

def test_uniform_reference_identity_is_exact():
    p=np.array([0.55,0.25,0.15,0.05])
    u=np.full(4,0.25)
    assert kl_bits(p,u) == pytest.approx(uniform_information_deficit_bits(p),abs=1e-14)

def test_uniform_mixing_increases_shannon_and_decreases_relative_information():
    p=np.array([0.7,0.1,0.1,0.1]); n=4; eps=0.35
    P=(1-eps)*np.eye(n)+eps*np.full((n,n),1/n)
    u=np.full(n,1/n)
    step=relative_information_step(p,u,P)
    assert step.delta_bits < 0
    assert shannon_bits(apply_kernel(p,P)) > shannon_bits(p)

def test_nonuniform_detailed_balance_reference_contracts_kl():
    pi=np.array([0.2,0.3,0.5])
    F=np.array([[0.13,0.03,0.04],[0.03,0.22,0.05],[0.04,0.05,0.41]])
    P=F/pi[:,None]
    assert np.linalg.norm(pi@P-pi,ord=1) < 1e-14
    p=np.array([0.72,0.18,0.10])
    step=relative_information_step(p,pi,P)
    assert step.delta_bits < 0

def test_stationary_reference_is_fixed():
    pi=np.array([0.2,0.3,0.5])
    F=np.array([[0.13,0.03,0.04],[0.03,0.22,0.05],[0.04,0.05,0.41]])
    P=F/pi[:,None]
    assert np.linalg.norm(apply_kernel(pi,P)-pi) < 1e-14
    assert kl_bits(pi,pi) == pytest.approx(0.0,abs=1e-15)

def test_random_uniform_contractions_have_no_positive_kl_step():
    rng=np.random.default_rng(20260827)
    for _ in range(1000):
        n=int(rng.integers(2,10)); p=rng.dirichlet(np.ones(n)); eps=float(rng.uniform(1e-4,0.95))
        P=(1-eps)*np.eye(n)+eps*np.full((n,n),1/n); u=np.full(n,1/n)
        assert relative_information_step(p,u,P).delta_bits <= 2e-13

def test_nonstationary_reference_fails_closed():
    p=[0.7,0.3]; r=[0.6,0.4]; P=[[0.9,0.1],[0.2,0.8]]
    with pytest.raises(ShannonRelativeInformationError): relative_information_step(p,r,P)

def test_invalid_probability_fails_closed():
    with pytest.raises(ShannonRelativeInformationError): kl_bits([0.7,0.4],[0.5,0.5])
