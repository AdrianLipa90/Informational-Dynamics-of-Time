import math
import numpy as np
import pytest
from src.idt.temporal_phase_connection import *

def tri_states():
    return [np.array([1,0],complex),np.array([1,1],complex)/math.sqrt(2),np.array([1,1j],complex)/math.sqrt(2)]

def links(states, dh=(0,0,0), sigma=(0,0,0)):
    return [temporal_edge_link(states[i],states[(i+1)%3],dh[i],sigma[i]) for i in range(3)]

def test_exact_scalar_cycle_telescopes():
    assert abs(exact_scalar_cycle_sum([0.2,-1.1,3.7,0.4])) < 1e-15

def test_berry_triangle_has_nonzero_global_holonomy():
    phi=cycle_phase(links(tri_states()))
    assert phi == pytest.approx(math.pi/4,abs=1e-12)
    assert connection_obstruction(phi)

def test_cycle_holonomy_is_gauge_invariant():
    s=tri_states(); base=cycle_phase(links(s))
    rng=np.random.default_rng(20260827)
    for _ in range(500):
        sg=gauge_transform(s,rng.uniform(-20,20,3))
        assert abs(wrap_phase(cycle_phase(links(sg))-base)) < 2e-12

def test_exact_shannon_term_drops_from_cycle():
    s=tri_states(); H=[0.2,1.4,-0.7]
    dh=[H[(i+1)%3]-H[i] for i in range(3)]
    assert cycle_phase(links(s,dh=dh)) == pytest.approx(cycle_phase(links(s)),abs=1e-12)

def test_nonexact_affinity_survives_cycle():
    s=tri_states(); sigma=[0.4,-0.1,0.8]
    observed=cycle_phase(links(s,sigma=sigma))
    expected=wrap_phase(math.pi/4 + KAPPA*sum(sigma))
    assert observed == pytest.approx(expected,abs=1e-12)

def test_exact_node_phase_edges_have_zero_cycle_holonomy():
    h=[0.3,-0.8,1.2,2.0]
    assert abs(exact_scalar_cycle_sum(h)) < 1e-15

def test_zero_overlap_fails_closed():
    with pytest.raises(TemporalPhaseConnectionError):
        pancharatnam_link([1,0],[0,1])
