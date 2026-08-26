import math
import numpy as np
import pytest
from src.idt.memory_dynamics import *

X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
Z=np.diag([1,-1]).astype(complex)


def test_raw_and_projective_imprints_are_global_phase_invariant():
    a=np.array([1,1j],complex)/math.sqrt(2)
    b=np.array([1,.3+0.4j],complex); b=b/np.linalg.norm(b)
    d0=raw_event_imprint(a,b); p0=projective_event_imprint(a,b)
    assert np.allclose(d0,raw_event_imprint(a*np.exp(1.2j),b*np.exp(-.7j)),atol=1e-14)
    assert np.allclose(p0,projective_event_imprint(a*np.exp(1.2j),b*np.exp(-.7j)),atol=1e-14)


def test_projective_imprint_is_hermitian_and_traceless():
    a=np.array([1,0],complex); b=np.array([1,1],complex)/math.sqrt(2)
    d=projective_event_imprint(a,b)
    assert np.allclose(d,d.conj().T,atol=1e-14)
    assert abs(np.trace(d))<1e-14


def test_scalar_contraction_separates_weight_from_projective_geometry():
    a=np.array([1,1j],complex)/math.sqrt(2); b=.4*a
    assert event_weight_change(a,b)<0
    assert np.allclose(projective_event_imprint(a,b),0,atol=1e-14)


def test_unitary_rotation_can_change_projective_imprint_without_weight_change():
    a=np.array([1,0],complex); b=np.array([1,1],complex)/math.sqrt(2)
    assert abs(event_weight_change(a,b))<1e-14
    assert np.linalg.norm(projective_event_imprint(a,b))>0.1


def test_memory_projection_increment_equals_projected_imprint():
    a=np.array([1,0],complex); b=np.array([1,1j],complex)/math.sqrt(2)
    ma=memory_plane_projection(a,X,Y); mb=memory_plane_projection(b,X,Y)
    d=projected_imprint(projective_event_imprint(a,b),X,Y)
    assert abs((mb-ma)-d)<1e-14


def test_central_force_has_zero_torque_and_areal_law():
    m=1.2+0.7j; v=-0.3+0.9j; acc=central_memory_acceleration(m,2.3)
    assert abs((m.conjugate()*acc).imag)<1e-14
    assert memory_areal_rate(m,v)==pytest.approx(memory_angular_momentum(m,v)/2)


def test_energy_derivative_cancels_algebraically():
    m=1.2+0.7j; v=-0.3+0.9j; mu=2.3; a=central_memory_acceleration(m,mu); r=abs(m)
    kinetic_rate=(v.conjugate()*a).real
    potential_rate=mu*(m.conjugate()*v).real/(r**3)
    assert kinetic_rate+potential_rate==pytest.approx(0,abs=1e-14)


def test_memory_circulation_rate_constant_and_variable_coupling():
    h=1.7; A=2.2; lam=.3
    assert memory_circulation_rate(h,A,lam)==pytest.approx(lam*h)
    assert memory_circulation_rate(h,A,lam,.04)==pytest.approx(lam*h+2*.04*A)


def test_action_area_normal_form_for_polygon():
    pts=np.array([1+0j,.2+1.1j,-.8+.3j,-.4-.7j,.6-.8j])
    lam=.37
    circ=sum(lam*(np.conj(pts[i])*pts[(i+1)%len(pts)]).imag for i in range(len(pts)))
    area=.5*sum((np.conj(pts[i])*pts[(i+1)%len(pts)]).imag for i in range(len(pts)))
    assert circ==pytest.approx(2*lam*area)


def test_exact_positive_berry_pullback_connection():
    m=.7+.4j; lam=.31; zb=memory_to_berry_patch(m,lam)
    assert berry_darboux_momentum(abs(zb))==pytest.approx(lam*abs(m)**2,abs=1e-14)
    assert berry_pullback_connection_coefficient(m,lam)==pytest.approx(lam*abs(m)**2,abs=1e-14)


def test_exact_negative_berry_pullback_uses_orientation_reversal():
    m=.5+.2j; lam=-.4
    assert berry_pullback_connection_coefficient(m,lam)==pytest.approx(lam*abs(m)**2,abs=1e-14)


def test_berry_pullback_curvature_matches_memory_curvature_in_polar_form():
    for r in [.1,.5,1.0]:
        lam=.2
        assert berry_pullback_curvature_polar(r,lam)==pytest.approx(2*lam*r,abs=1e-14)


def test_berry_pullback_fails_closed_at_patch_boundary():
    with pytest.raises(MemoryDynamicsError):
        memory_to_berry_patch(2+0j,.25)


def test_event_impulse_energy_and_angular_momentum_changes_match_direct_formula():
    m=1.1+.3j; v=-.2+.5j; dm=.08-.04j; g=.7; mu=1.3
    E0=memory_energy(m,v,mu); h0=memory_angular_momentum(m,v)
    _,v1=apply_memory_event_impulse(m,v,dm,g)
    dv=g*dm
    assert memory_energy(m,v1,mu)-E0==pytest.approx((v.conjugate()*dv).real+.5*abs(dv)**2,abs=1e-14)
    assert memory_angular_momentum(m,v1)-h0==pytest.approx((m.conjugate()*dv).imag,abs=1e-14)
