from fractions import Fraction

import pytest

from idt.pretemporal_halfstep_successor import (
    PretemporalState,
    half_step,
    hilbert_shift,
    normalized_grade,
    post_transition_click_label,
    relational_edge,
    shifted_edge,
    successor,
)


@pytest.mark.parametrize("n", range(16))
@pytest.mark.parametrize("sector", (0, 1))
def test_half_step_squares_to_successor(n, sector):
    x = PretemporalState(n, sector)
    assert half_step(half_step(x)) == successor(x)


@pytest.mark.parametrize("n", range(16))
@pytest.mark.parametrize("sector", (0, 1))
def test_exact_half_grade(n, sector):
    x = PretemporalState(n, sector)
    assert normalized_grade(half_step(x)) - normalized_grade(x) == Fraction(1, 2)
    assert normalized_grade(successor(x)) - normalized_grade(x) == 1


@pytest.mark.parametrize("n", range(1, 32))
def test_relational_gluing_and_shift(n):
    assert relational_edge(n) & relational_edge(n + 1) == frozenset((n + 1,))
    assert shifted_edge(n) == relational_edge(n + 1)


def test_hilbert_shift_is_not_surjective_on_positive_rooms():
    image = {hilbert_shift(n) for n in range(1, 64)}
    assert len(image) == 63
    assert 1 not in image


def test_click_sequence():
    assert [post_transition_click_label(k) for k in range(1, 5)] == [
        (Fraction(1, 2), "-"),
        (Fraction(1, 1), "+"),
        (Fraction(3, 2), "-"),
        (Fraction(2, 1), "+"),
    ]


def test_fail_closed_domains():
    with pytest.raises(ValueError):
        PretemporalState(-1, 0)
    with pytest.raises(ValueError):
        PretemporalState(0, 2)
    with pytest.raises(ValueError):
        relational_edge(0)
    with pytest.raises(ValueError):
        hilbert_shift(0)
