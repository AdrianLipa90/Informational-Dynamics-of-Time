import numpy as np

from idt.relative_coframe_dynamics import (
    audit_relative_dynamics,
    exterior_square4,
    frame_generator,
    lie_exterior_square,
    relative_bivector,
    relative_bivector_velocity,
    relative_bivector_velocity_generator_form,
    relative_coframe,
    relative_coframe_velocity,
    relative_coframe_velocity_generator_form,
)


def fixtures():
    source = np.array([
        [2.0, 1.0, 0.0, 0.0],
        [0.0, 2.0, 1.0, 0.0],
        [0.0, 0.0, 3.0, 1.0],
        [1.0, 0.0, 0.0, 2.0],
    ])
    target = np.array([
        [3.0, 0.0, 1.0, 0.0],
        [1.0, 2.0, 0.0, 1.0],
        [0.0, 1.0, 2.0, 0.0],
        [0.0, 0.0, 1.0, 2.0],
    ])
    source_v = np.array([
        [1.0, 0.0, 1.0, 0.0],
        [0.0, -1.0, 0.0, 1.0],
        [1.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 1.0],
    ])
    target_v = np.array([
        [0.0, 1.0, 0.0, 1.0],
        [1.0, 0.0, -1.0, 0.0],
        [0.0, 1.0, 1.0, 0.0],
        [1.0, 0.0, 0.0, -1.0],
    ])
    return source, target, source_v, target_v


def test_relative_coframe_generator_identity():
    source, target, source_v, target_v = fixtures()
    direct = relative_coframe_velocity(source, target, source_v, target_v)
    generated = relative_coframe_velocity_generator_form(source, target, source_v, target_v)
    assert np.allclose(direct, generated, rtol=0.0, atol=1e-12)


def test_relative_bivector_generator_identity():
    source, target, source_v, target_v = fixtures()
    direct = relative_bivector_velocity(source, target, source_v, target_v)
    generated = relative_bivector_velocity_generator_form(source, target, source_v, target_v)
    assert np.allclose(direct, generated, rtol=0.0, atol=1e-12)


def test_exterior_square_multiplicativity():
    source, target, _, _ = fixtures()
    relative = relative_coframe(source, target)
    lhs = exterior_square4(relative)
    rhs = exterior_square4(target) @ np.linalg.inv(exterior_square4(source))
    assert np.allclose(lhs, rhs, rtol=0.0, atol=1e-11)


def test_common_left_flow_is_conjugation():
    source, target, _, _ = fixtures()
    L = np.array([
        [0.0, 1.0, 0.0, 0.0],
        [-1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0],
        [0.0, 0.0, -1.0, 0.0],
    ])
    source_v = L @ source
    target_v = L @ target
    relative = relative_coframe(source, target)
    velocity = relative_coframe_velocity(source, target, source_v, target_v)
    assert np.allclose(velocity, L @ relative - relative @ L, rtol=0.0, atol=1e-12)


def test_audit_residuals_are_zero_to_precision():
    source, target, source_v, target_v = fixtures()
    audit = audit_relative_dynamics(source, target, source_v, target_v)
    assert audit.coframe_residual < 1e-12
    assert audit.bivector_residual < 1e-11
