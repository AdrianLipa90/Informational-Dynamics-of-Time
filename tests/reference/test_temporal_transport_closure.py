import numpy as np
from src.idt.bifurcation import polar_bifurcation_operator
from src.idt.temporal_transport import interrupted_temporal_propagator, interrupted_norm_bound, cut_interrupted_temporal_propagator, transport_condition_number

I=np.eye(2,dtype=complex)
X=np.array([[0,1],[1,0]],complex)
Y=np.array([[0,-1j],[1j,0]],complex)
D=np.diag([0.1,0.7]).astype(complex)


def test_transport_contraction_bound():
    seg=[I, np.diag([1,1j]), X]
    ev=[polar_bifurcation_operator(.3,.2,D,X).operator, polar_bifurcation_operator(.4,-.1,D,Y).operator]
    measured,bound=interrupted_norm_bound(seg,ev)
    assert measured <= bound+1e-12
    assert bound <= 1.0+1e-12


def test_finite_exponential_transport_can_be_invertible_but_ill_conditioned():
    D2=np.diag([0.0,2.0]).astype(complex)
    b=polar_bifurcation_operator(10.0,.3,D2,X).operator
    u=interrupted_temporal_propagator([I,I],[b])
    assert abs(np.linalg.det(u))>0.0
    assert transport_condition_number(u)>1e7


def test_exact_transport_cut_factorization():
    seg=[I,np.diag([1,1j]),X,np.diag([1j,1])]
    ev=[polar_bifurcation_operator(.2,.1,D,X).operator, polar_bifurcation_operator(.3,-.15,D,Y).operator, polar_bifurcation_operator(.1,.05,D,X).operator]
    total=interrupted_temporal_propagator(seg,ev)
    for c in range(4):
        early,late=cut_interrupted_temporal_propagator(seg,ev,c)
        assert np.allclose(total,late@early,atol=1e-13,rtol=0)
