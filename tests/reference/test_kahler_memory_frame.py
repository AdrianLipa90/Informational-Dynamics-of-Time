import math

import numpy as np
import pytest

from src.idt.kahler_memory_frame import (
    KahlerMemoryFrameError,
    fs_distance_cp1,
    fs_log_map_cp1,
    initial_cp1_memory_frame,
    parallel_transport_cp1_frame,
    project_cp1_event,
    qubit_bloch,
)


def test_qubit_bloch_is_unit_and_global_phase_invariant():
    psi = np.array([1.0, 0.4 + 0.3j], dtype=complex)
    n0 = qubit_bloch(psi)
    n1 = qubit_bloch(psi * np.exp(1.234j))
    assert np.linalg.norm(n0) == pytest.approx(1.0, abs=1e-14)
    assert np.allclose(n0, n1, atol=1e-14, rtol=0.0)


def test_fs_log_norm_matches_qubit_overlap_distance():
    a = np.array([1.0, 0.0], dtype=complex)
    b = np.array([math.cos(0.31), math.sin(0.31)], dtype=complex)
    na = qubit_bloch(a)
    nb = qubit_bloch(b)
    xi = fs_log_map_cp1(na, nb)
    overlap_distance = math.acos(abs(np.vdot(a, b)))
    assert np.linalg.norm(xi) == pytest.approx(overlap_distance, abs=1e-14)
    assert fs_distance_cp1(na, nb) == pytest.approx(overlap_distance, abs=1e-14)


def test_initial_frame_is_tangent_orthonormal_and_kahler_oriented():
    a = qubit_bloch([1.0, 0.0])
    b = qubit_bloch([math.cos(0.2), 1j * math.sin(0.2)])
    frame = initial_cp1_memory_frame(a, b)
    assert np.dot(frame.anchor_bloch, frame.e_q) == pytest.approx(0.0, abs=1e-14)
    assert np.dot(frame.anchor_bloch, frame.e_p) == pytest.approx(0.0, abs=1e-14)
    assert np.dot(frame.e_q, frame.e_p) == pytest.approx(0.0, abs=1e-14)
    assert np.linalg.norm(frame.e_q) == pytest.approx(1.0, abs=1e-14)
    assert np.linalg.norm(frame.e_p) == pytest.approx(1.0, abs=1e-14)
    assert np.allclose(frame.e_p, np.cross(frame.anchor_bloch, frame.e_q), atol=1e-14, rtol=0.0)


def test_event_projection_norm_equals_fs_distance():
    a = qubit_bloch([1.0, 0.0])
    b = qubit_bloch([math.cos(0.23), math.sin(0.23)])
    frame = initial_cp1_memory_frame(a, b)
    delta_m = project_cp1_event(frame, b)
    assert abs(delta_m) == pytest.approx(fs_distance_cp1(a, b), abs=1e-14)
    assert abs(delta_m.imag) < 1e-14


def test_parallel_transport_preserves_tangent_dyad_and_orientation():
    a = qubit_bloch([1.0, 0.0])
    b = qubit_bloch([math.cos(0.2), math.sin(0.2)])
    c = qubit_bloch([math.cos(0.35), math.sin(0.35) * np.exp(0.4j)])
    frame_a = initial_cp1_memory_frame(a, b)
    frame_c = parallel_transport_cp1_frame(frame_a, c)
    assert np.dot(frame_c.anchor_bloch, frame_c.e_q) == pytest.approx(0.0, abs=1e-12)
    assert np.dot(frame_c.anchor_bloch, frame_c.e_p) == pytest.approx(0.0, abs=1e-12)
    assert np.dot(frame_c.e_q, frame_c.e_p) == pytest.approx(0.0, abs=1e-12)
    assert np.allclose(frame_c.e_p, np.cross(frame_c.anchor_bloch, frame_c.e_q), atol=1e-12, rtol=0.0)


def test_parallel_transport_round_trip_recovers_frame_on_same_geodesic():
    a = qubit_bloch([1.0, 0.0])
    b = qubit_bloch([math.cos(0.27), math.sin(0.27)])
    frame_a = initial_cp1_memory_frame(a, b)
    frame_b = parallel_transport_cp1_frame(frame_a, b)
    frame_back = parallel_transport_cp1_frame(frame_b, a)
    assert np.allclose(frame_back.e_q, frame_a.e_q, atol=1e-12, rtol=0.0)
    assert np.allclose(frame_back.e_p, frame_a.e_p, atol=1e-12, rtol=0.0)


def test_antipodal_geodesic_ambiguity_fails_closed():
    north = np.array([0.0, 0.0, 1.0])
    south = np.array([0.0, 0.0, -1.0])
    with pytest.raises(KahlerMemoryFrameError):
        fs_log_map_cp1(north, south)
