import math

import pytest

from idt.orchorbital_600cell_candidate_v01 import (
    IDTOrchorbital600CellCandidateError,
    bind_orchorbital_sector,
    supported_dimension,
    working_orchorbital_table,
)


def test_candidate_is_active_working_without_mutating_temporal_core():
    rows = working_orchorbital_table()
    assert len(rows) == 6
    assert all(row.status == "CANDIDATE" for row in rows)
    assert all(row.active_working_version for row in rows)
    assert all(not row.canonical for row in rows)
    assert all(not row.temporal_core_mutated for row in rows)
    assert all(row.physical_time_binding == "OPEN" for row in rows)


def test_candidate_keeps_explicit_pncs_source_provenance():
    assert {
        row.source_carrier for row in working_orchorbital_table()
    } == {"PNCS_600CELL_S3_ANGULAR_CANDIDATE_V0_1"}


def test_s3_multiplicity_and_angular_spectrum():
    rows = working_orchorbital_table()
    assert [row.multiplicity for row in rows] == [1, 4, 9, 16, 25, 36]
    assert [row.angular_eigenvalue for row in rows] == [0, 3, 8, 15, 24, 35]
    assert supported_dimension() == 91


def test_adjacency_sector_eigenvalues():
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    expected = [12.0, 6.0 * phi, 4.0 * phi, 3.0, 0.0, -2.0]
    observed = [row.adjacency_eigenvalue for row in working_orchorbital_table()]
    assert all(
        math.isclose(got, want, rel_tol=0.0, abs_tol=1e-15)
        for got, want in zip(observed, expected)
    )


@pytest.mark.parametrize("bad", [-1, 6, 7, True])
def test_outside_verified_orchorbital_sector_fails_closed(bad):
    with pytest.raises(IDTOrchorbital600CellCandidateError):
        bind_orchorbital_sector(bad)
