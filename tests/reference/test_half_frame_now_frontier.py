import math

import numpy as np

from idt.half_frame_temporal_gluing import glued_support_labels, glued_temporal_measures


def test_serial_frontier_is_last_pure_support():
    for n in range(1, 9):
        labels = glued_support_labels(n)
        assert labels[-1] == str(n)
        assert len(labels) == n + 1


def test_one_frame_extension_converts_old_frontier_to_new_interface():
    for n in range(1, 7):
        before = glued_support_labels(n)
        after = glued_support_labels(n + 1)
        assert after[:-2] == before[:-1]
        assert after[-2] == f"{n}{n + 1}"
        assert after[-1] == str(n + 1)


def test_elapsed_measure_extension_adds_exactly_new_frame_measure():
    old_theta = np.asarray([0.3, 0.8, 0.4, 1.1])
    new_theta = 0.65

    old_support = glued_temporal_measures(old_theta)
    new_support = glued_temporal_measures(np.append(old_theta, new_theta))

    assert math.isclose(
        float(np.sum(new_support) - np.sum(old_support)),
        new_theta,
        rel_tol=0.0,
        abs_tol=2e-15,
    )
    assert math.isclose(old_support[-1], old_theta[-1] / 2.0, abs_tol=2e-15)
    assert math.isclose(new_support[-2], (old_theta[-1] + new_theta) / 2.0, abs_tol=2e-15)
    assert math.isclose(new_support[-1], new_theta / 2.0, abs_tol=2e-15)
