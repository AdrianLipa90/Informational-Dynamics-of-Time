import numpy as np
import pytest

from src.idt.relational_tensor_scalar_forcing import (
    RelationalTemporalForcingError,
    audit_response_geometry,
    canonical_complex_structure,
    contextual_temporal_pace,
    internal_elapsed_increment,
    reparameterized_activity,
    response_flow,
    transformed_response_geometry,
)


def test_context_changes_elapsed_for_same_order_increment():
    dl=1.0
    slow=internal_elapsed_increment(0.5,1.0,dl)
    fast=internal_elapsed_increment(3.0,1.0,dl)
    assert slow == 0.5
    assert fast == 3.0
    assert slow != fast


def test_elapsed_is_invariant_under_increasing_reparameterization():
    a=2.7; ref=1.3; dl=0.4
    scale=0.25
    a_prime=reparameterized_activity(a,scale)
    dl_prime=dl/scale
    assert internal_elapsed_increment(a,ref,dl) == pytest.approx(internal_elapsed_increment(a_prime,ref,dl_prime))


def test_covector_to_vector_response_is_coordinate_covariant_with_rank2_tensor():
    G=np.diag([1.2,0.9,1.2,0.9])
    J=canonical_complex_structure(4)
    p=np.array([0.3,-0.7,1.1,0.4])
    h=np.array([-0.2,0.8,0.5,-1.0])
    A=np.array([[1.0,0.2,0.0,0.0],[0.1,1.1,0.0,0.0],[0.0,0.0,0.9,-0.15],[0.0,0.0,0.25,1.05]])
    v=response_flow(p,h,G,J)
    Gp,Jp=transformed_response_geometry(G,J,A)
    pp=np.linalg.solve(A.T,p); hp=np.linalg.solve(A.T,h)
    assert np.linalg.norm(response_flow(pp,hp,Gp,Jp)-A@v) < 1e-12


def test_symmetric_positive_response_dissipates_information_for_arbitrary_covector():
    rng=np.random.default_rng(20260827)
    J=canonical_complex_structure(4)
    for _ in range(500):
        B=rng.normal(size=(4,4))
        G=B@B.T + 0.2*np.eye(4)
        p=rng.normal(size=4)
        audit=audit_response_geometry(1.0,1.0,p,np.zeros(4),G,J,np.eye(4))
        assert audit.dissipation_rate < 0.0


def test_kahler_compatible_phase_sector_is_reversible_and_antisymmetric():
    G=np.diag([1.7,1.7,0.6,0.6])
    J=canonical_complex_structure(4)
    audit=audit_response_geometry(2.0,1.0,[1,2,3,4],[-2,1,0.5,3],G,J,np.eye(4))
    assert abs(audit.reversible_rate) < 1e-12
    assert audit.complex_structure_defect < 1e-12
    assert audit.antisymmetry_defect < 1e-12


def test_incompatible_mobility_exposes_missing_kahler_compatibility():
    G=np.diag([1.7,0.8,0.6,0.3])
    J=canonical_complex_structure(4)
    audit=audit_response_geometry(1.0,1.0,[1,0,0,0],[1,2,3,4],G,J,np.eye(4))
    assert audit.antisymmetry_defect > 0.1


def test_invalid_inputs_fail_closed():
    with pytest.raises(RelationalTemporalForcingError):
        contextual_temporal_pace(0.0,1.0)
    with pytest.raises(RelationalTemporalForcingError):
        canonical_complex_structure(3)
