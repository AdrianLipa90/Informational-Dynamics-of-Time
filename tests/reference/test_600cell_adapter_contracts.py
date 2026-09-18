from pathlib import Path

from idt.orchorbital_600cell_candidate_v01 import working_orchorbital_table

ROOT = Path(__file__).resolve().parents[2]


def test_600cell_candidate_contracts_preserve_noncanonical_boundary():
    rows = working_orchorbital_table()
    assert rows
    assert all(row.status == "CANDIDATE" for row in rows)
    assert all(not row.canonical for row in rows)
    assert all(not row.temporal_core_mutated for row in rows)
    assert all(row.physical_time_binding == "OPEN" for row in rows)


def test_phasenav_adapter_documents_preserve_candidate_boundary():
    carrier = (ROOT / "PHASENAV_CARRIER_HIERARCHY_ADAPTER_V0_2.md").read_text(encoding="utf-8")
    promotion = (ROOT / "PHASENAV_PROMOTION_GEOMETRY_ADAPTER_V0_1.md").read_text(encoding="utf-8")
    for text in (carrier, promotion):
        assert "CANDIDATE_ONLY" in text
        assert "TEMPORAL_CORE_MUTATED_FALSE" in text
        assert "CANON_WRITE_AUTHORITY_FALSE" in text
        assert "temporal_core_mutated=false" in text
