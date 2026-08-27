from __future__ import annotations

import numpy as np
import pytest

from src.idt.retrodiction_adaptive_sod_separator import (
    AdaptiveSODSeparator,
    AdaptiveSODSeparatorError,
    augment_sparse_record,
    select_max_sod_separator,
)

REFERENCE = np.array([
    [-0.699724, 0.400908],
    [-0.699512, 0.401732],
    [-0.699018, 0.403095],
    [-0.698743, 0.403795],
])
OFFSETS = np.array([
    [0.0, -5.551115123125783e-17],
    [2.897277293967271e-06, -5.308564348105449e-07],
    [1.7763568394002505e-15, 3.885780586188048e-16],
    [1.7763568394002505e-15, 3.3306690738754696e-16],
])
CANDIDATE = REFERENCE + OFFSETS


def test_known_07m_witness_selects_r2x() -> None:
    sep = select_max_sod_separator(REFERENCE, CANDIDATE, spatial_tolerance=1e-9)
    assert sep.status == "KNOWN_SOD_SEPARATOR_SELECTED"
    assert sep.label == "r2x"
    assert sep.checkpoint_index == 2
    assert sep.axis_index == 0
    assert sep.magnitude == pytest.approx(2.897277293967271e-06)


def test_selected_coordinate_separates_known_witness_record() -> None:
    sep = select_max_sod_separator(REFERENCE, CANDIDATE, spatial_tolerance=1e-9)
    base = np.array([0.1, 0.2, 0.3])
    y0 = augment_sparse_record(base, REFERENCE, sep)
    y1 = augment_sparse_record(base, CANDIDATE, sep)
    assert np.linalg.norm(y1 - y0) == pytest.approx(sep.magnitude)
    assert np.linalg.norm(y1 - y0) > 1e-9


def test_ties_are_deterministic_earliest_checkpoint_x_before_y() -> None:
    ref = np.zeros((2, 2))
    cand = np.array([[2.0, -2.0], [2.0, 0.0]])
    sep = select_max_sod_separator(ref, cand, spatial_tolerance=0.5)
    assert sep.label == "r1x"


def test_no_divergent_coordinate_fails_closed() -> None:
    ref = np.zeros((2, 2))
    cand = ref + 1e-12
    with pytest.raises(AdaptiveSODSeparatorError, match="no spatial component"):
        select_max_sod_separator(ref, cand, spatial_tolerance=1e-9)


def test_invalid_tolerance_fails_closed() -> None:
    with pytest.raises(AdaptiveSODSeparatorError):
        select_max_sod_separator(REFERENCE, CANDIDATE, spatial_tolerance=0.0)


def test_augment_rejects_separator_outside_lineage() -> None:
    sep = AdaptiveSODSeparator("r9x", 9, 0, 1.0, 1.0, "KNOWN_SOD_SEPARATOR_SELECTED")
    with pytest.raises(AdaptiveSODSeparatorError, match="outside"):
        augment_sparse_record([1.0], REFERENCE, sep)
