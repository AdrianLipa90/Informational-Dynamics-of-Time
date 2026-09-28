from idt.pretemporal_alternating_stella_inference import (
    A4,
    AlternatingStellaState,
    cross_overlap_signature,
    full_successor,
    half_step,
    matmul,
    validate,
)


def test_decorated_half_step_squares_to_successor():
    for sector in (0, 1):
        x = AlternatingStellaState(3, sector)
        assert half_step(half_step(x)) == full_successor(x)


def test_label_reassignment_does_not_change_inference_signature():
    x = half_step(AlternatingStellaState(0, 0))
    target = cross_overlap_signature(x.plus, x.minus)
    for a in A4:
        for b in A4:
            assert cross_overlap_signature(
                matmul(x.plus, a),
                matmul(x.minus, b),
            ) == target


def test_reference_validator_passes():
    result = validate()
    assert result["status"] == "PASS"
    assert result["tetrahedral_rotation_group_order"] == 12
    assert result["physical_time_assumed"] is False
    assert result["physical_space_assumed"] is False
