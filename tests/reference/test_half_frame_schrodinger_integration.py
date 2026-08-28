import math
import numpy as np

from idt.half_frame_temporal_gluing import (
    audit_half_frame_state,
    glued_temporal_measures,
    interface_occupancy,
)
from idt.zeta_collatz_temporal_fuzziness import (
    build_prime_frames,
    propagate_frame_amplitudes,
    zeta_collatz_hamiltonian,
)


def test_schrodinger_frame_flow_closes_on_half_frame_overlap_and_defect_sectors():
    frames = build_prime_frames([3, 5, 7, 11])
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.6, collatz_coupling=0.8)
    psi0 = np.asarray([1.0, 0.0, 0.0, 0.0], dtype=complex)
    psi = propagate_frame_amplitudes(psi0, h, 0.73)

    audit = audit_half_frame_state(psi)
    assert audit.support_labels == ("1", "12", "23", "34", "4")
    assert audit.norm_residual < 5e-14
    assert math.isclose(
        audit.glued_weight + audit.seam_defect_weight,
        1.0,
        rel_tol=0.0,
        abs_tol=5e-14,
    )
    assert interface_occupancy(psi) > 0.0


def test_schrodinger_readout_and_elapsed_support_share_same_N_plus_1_topology():
    frames = build_prime_frames([3, 5, 7, 11, 13])
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.35, collatz_coupling=1.1)
    psi0 = np.ones(5, dtype=complex) / math.sqrt(5.0)
    psi = propagate_frame_amplitudes(psi0, h, 0.41)
    audit = audit_half_frame_state(psi)

    frame_measures = np.asarray([0.2, 0.4, 0.7, 0.3, 0.9])
    elapsed_supports = glued_temporal_measures(frame_measures)

    assert audit.glued_amplitudes.size == elapsed_supports.size == 6
    assert len(audit.support_labels) == 6
    assert math.isclose(float(np.sum(elapsed_supports)), float(np.sum(frame_measures)), abs_tol=2e-15)


def test_reference_schrodinger_flow_can_increase_neighbor_overlap_occupancy():
    frames = build_prime_frames([3, 5, 7, 11, 13])
    h = zeta_collatz_hamiltonian(frames, zeta_scale=0.6, collatz_coupling=1.0)
    psi0 = np.asarray([1.0, 0.0, 0.0, 0.0, 0.0], dtype=complex)
    initial = interface_occupancy(psi0)
    psi = propagate_frame_amplitudes(psi0, h, 1.0)
    evolved = interface_occupancy(psi)

    assert math.isclose(initial, 0.25, rel_tol=0.0, abs_tol=2e-15)
    assert evolved > 0.5
    assert evolved > initial + 0.25
