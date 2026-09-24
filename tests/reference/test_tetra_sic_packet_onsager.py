import math

import numpy as np

from idt.tetra_sic_packet_onsager import (
    audit_tetra_sic_onsager,
    bloch_from_tetra_sic,
    elapsed_bloch_packet_velocity,
    tetra_bloch_velocity,
    tetra_sic_probabilities,
)


def test_tetra_sic_reconstruction():
    r=np.array((0.2,-0.3,0.4))
    p=tetra_sic_probabilities(r)
    assert np.allclose(bloch_from_tetra_sic(p),r,rtol=0.0,atol=1e-12)


def test_tetra_vertex_probabilities_are_positive():
    s=1.0/math.sqrt(3.0)
    p=tetra_sic_probabilities((s,s,s))
    assert np.allclose(
        np.sort(p),
        np.asarray((1.0/6.0,1.0/6.0,1.0/6.0,1.0/2.0)),
        rtol=0.0,
        atol=1e-12,
    )


def test_s4_symmetric_onsager_flow_is_radial():
    r=np.array((0.2,-0.3,0.4))
    rate=0.7
    assert np.allclose(
        tetra_bloch_velocity(r,rate),
        -4.0*rate*r,
        rtol=0.0,
        atol=1e-12,
    )


def test_onsager_audit():
    audit=audit_tetra_sic_onsager((0.2,-0.3,0.4),0.7)
    assert audit.reconstruction_defect < 1e-12
    assert audit.isotropic_velocity_defect < 1e-12
    assert audit.onsager_factorization_defect < 1e-12
    assert audit.onsager_dissipation_rate_bits <= 1e-12


def test_elapsed_packet_velocity_product_rule():
    r=np.array((0.2,-0.3,0.4))
    dr=np.array((-0.1,0.2,-0.3))
    ell=2.5
    dell=0.4
    v=elapsed_bloch_packet_velocity(ell,r,dell,dr)
    expected=np.concatenate(((0.5*dell,),0.5*(dell*r+ell*dr)))
    assert np.allclose(v,expected,rtol=0.0,atol=1e-12)


def test_uniform_relational_fields_recover_rate_rho_over_eta():
    from idt.tetra_sic_packet_onsager import tetra_relational_bloch_velocity
    r=np.array((0.2,-0.3,0.4))
    rho0=2.5
    eta0=5.0
    expected=-4.0*(rho0/eta0)*r
    actual=tetra_relational_bloch_velocity(
        r,
        (rho0,)*4,
        (eta0,)*4,
    )
    assert np.allclose(actual,expected,rtol=0.0,atol=1e-12)


def test_heterogeneous_relational_flow_conserves_probability():
    from idt.tetra_sic_packet_onsager import tetra_relational_probability_velocity
    dp=tetra_relational_probability_velocity(
        (0.2,-0.3,0.4),
        (1.0,2.0,3.0,4.0),
        (2.0,1.5,3.5,2.5),
    )
    assert abs(float(dp.sum())) < 1e-12
    assert np.all(np.isfinite(dp))
