import math

import numpy as np
import pytest

from src.idt.kahler_memory_frame import fs_distance_cp1, initial_cp1_memory_frame, project_cp1_event, qubit_bloch
from src.idt.kahler_memory_frame_cpn import (
    CPNMemoryFrameError,
    fs_distance_cpn,
    fs_log_map_cpn,
    initial_cpn_memory_frame,
    parallel_transport_cpn_frame,
    project_cpn_event,
)


def _norm(x):
    x = np.asarray(x, dtype=complex)
    return x / np.linalg.norm(x)


def test_cpn_log_map_is_horizontal_and_has_fs_norm():
    a = _norm([1.0, 0.0, 0.0])
    b = _norm([math.cos(0.4), math.sin(0.4), 0.0])
    xi = fs_log_map_cpn(a, b)
    assert abs(np.vdot(a, xi)) < 1e-13
    assert np.linalg.norm(xi) == pytest.approx(fs_distance_cpn(a, b), abs=1e-13)
    assert fs_distance_cpn(a, b) == pytest.approx(0.4, abs=1e-13)


def test_initial_cpn_frame_is_kahler_conjugate_horizontal_dyad():
    a = _norm([1.0, 0.0, 0.0])
    b = _norm([math.cos(0.4), math.sin(0.4), 0.0])
    frame = initial_cpn_memory_frame(a, b)
    assert abs(np.vdot(frame.anchor_state, frame.e_q)) < 1e-13
    assert abs(np.vdot(frame.anchor_state, frame.e_p)) < 1e-13
    assert np.linalg.norm(frame.e_q) == pytest.approx(1.0, abs=1e-13)
    assert np.linalg.norm(frame.e_p) == pytest.approx(1.0, abs=1e-13)
    assert abs(np.vdot(frame.e_q, frame.e_p).real) < 1e-13
    assert np.allclose(frame.e_p, 1j * frame.e_q, atol=1e-13, rtol=0.0)


def test_reference_event_projects_to_real_distance_with_zero_residual():
    a = _norm([1.0, 0.0, 0.0])
    b = _norm([math.cos(0.4), math.sin(0.4), 0.0])
    frame = initial_cpn_memory_frame(a, b)
    projection = project_cpn_event(frame, b)
    assert projection.delta_m == pytest.approx(0.4 + 0.0j, abs=1e-13)
    assert projection.fs_distance == pytest.approx(0.4, abs=1e-13)
    assert projection.residual_norm == pytest.approx(0.0, abs=1e-13)


def test_higher_dimensional_projection_resolves_memory_plane_and_residual():
    a = _norm([1.0, 0.0, 0.0])
    b = _norm([math.cos(0.4), math.sin(0.4), 0.0])
    c = _norm([0.9, 0.2 * np.exp(0.3j), 0.35 * np.exp(-0.7j)])
    frame = initial_cpn_memory_frame(a, b)
    projection = project_cpn_event(frame, c)
    assert projection.residual_norm > 0.1
    assert projection.fs_distance**2 == pytest.approx(
        abs(projection.delta_m) ** 2 + projection.residual_norm**2,
        abs=2e-13,
    )
    assert abs(projection.delta_m) < projection.fs_distance


def test_independent_global_phases_leave_cpn_projection_invariant():
    a = _norm([1.0, 0.0, 0.0])
    b = _norm([math.cos(0.4), math.sin(0.4), 0.0])
    c = _norm([0.9, 0.2 * np.exp(0.3j), 0.35 * np.exp(-0.7j)])
    frame = initial_cpn_memory_frame(a, b)
    projection = project_cpn_event(frame, c)

    a2 = a * np.exp(0.7j)
    b2 = b * np.exp(-1.1j)
    c2 = c * np.exp(2.2j)
    frame2 = initial_cpn_memory_frame(a2, b2)
    projection2 = project_cpn_event(frame2, c2)

    assert projection2.delta_m == pytest.approx(projection.delta_m, abs=1e-13)
    assert projection2.fs_distance == pytest.approx(projection.fs_distance, abs=1e-13)
    assert projection2.residual_norm == pytest.approx(projection.residual_norm, abs=1e-13)


def test_cpn_geodesic_transport_preserves_kahler_frame_and_round_trip():
    a = _norm([1.0, 0.0, 0.0])
    b = _norm([math.cos(0.4), math.sin(0.4), 0.0])
    frame_a = initial_cpn_memory_frame(a, b)
    frame_b = parallel_transport_cpn_frame(frame_a, b)
    assert abs(np.vdot(frame_b.anchor_state, frame_b.e_q)) < 1e-13
    assert np.allclose(frame_b.e_p, 1j * frame_b.e_q, atol=1e-13, rtol=0.0)

    frame_a2 = parallel_transport_cpn_frame(frame_b, a)
    overlap = np.vdot(a, frame_a2.anchor_state)
    phase = overlap / abs(overlap)
    assert np.allclose(frame_a2.e_q / phase, frame_a.e_q, atol=2e-13, rtol=0.0)
    assert np.allclose(frame_a2.e_p / phase, frame_a.e_p, atol=2e-13, rtol=0.0)


def test_cpn_reduces_to_cp1_distance_and_memory_displacement_magnitude():
    psi_a = _norm([1.0, 0.0])
    psi_b = _norm([math.cos(0.2), math.sin(0.2)])

    frame_n = initial_cpn_memory_frame(psi_a, psi_b)
    projection_n = project_cpn_event(frame_n, psi_b)

    bloch_a = qubit_bloch(psi_a)
    bloch_b = qubit_bloch(psi_b)
    frame_1 = initial_cp1_memory_frame(bloch_a, bloch_b)
    delta_1 = project_cp1_event(frame_1, bloch_b)

    assert fs_distance_cpn(psi_a, psi_b) == pytest.approx(fs_distance_cp1(bloch_a, bloch_b), abs=1e-13)
    assert abs(projection_n.delta_m) == pytest.approx(abs(delta_1), abs=1e-13)
    assert projection_n.residual_norm == pytest.approx(0.0, abs=1e-13)


def test_orthogonal_cut_locus_fails_closed():
    with pytest.raises(CPNMemoryFrameError):
        fs_log_map_cpn([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
    with pytest.raises(CPNMemoryFrameError):
        initial_cpn_memory_frame([1.0, 0.0, 0.0], [0.0, 1.0, 0.0])
