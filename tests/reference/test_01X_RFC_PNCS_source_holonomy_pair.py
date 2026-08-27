import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / "validation" / "IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1.json"
LOCK = ROOT / "validation" / "01X_RFC_CROSS_REFERENCE_LOCK_V0_1.json"
EXPECTED_PNCS = "5f3bf90998b8c3547d51e7c47bddaf0d6be25d60"
EXPECTED_LOOPS = [
    "SOURCE.CARRIER.NORMALIZATION.ROUNDTRIP",
    "SOURCE.CARRIER.Q0_OCCUPATION.ROUNDTRIP",
    "SOURCE.CARRIER.EPSILON_MASS_DENSITY.ROUNDTRIP",
]


def _load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_pair_receipt_matches_idt_cross_reference_lock():
    pair = _load(PAIR)
    lock = _load(LOCK)
    assert pair["schema"] == "IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1"
    assert pair["local_repository"] == "AdrianLipa90/Informational-Dynamics-of-Time"
    assert pair["pncs"]["code_commit"] == EXPECTED_PNCS
    assert lock["pncs"]["commit"] == EXPECTED_PNCS
    assert pair["pncs"]["loops"] == EXPECTED_LOOPS
    assert [
        lock["interface_contract"]["pncs_reference_loop"],
        lock["interface_contract"]["pncs_q0_loop"],
        lock["interface_contract"]["pncs_epsilon_loop"],
    ] == EXPECTED_LOOPS


def test_pair_receipt_records_executed_peer_reference_gates():
    pair = _load(PAIR)
    assert pair["idt"]["status"] == "PASS"
    assert pair["idt"]["passed"] == 337
    assert pair["idt"]["failed"] == 0
    assert pair["rfc"]["status"] == "PASS"
    assert pair["rfc"]["passed"] == 29
    assert pair["rfc"]["failed"] == 0
    assert pair["pncs"]["native_ci"]["classification"] == "CI_EXECUTION_UNRESOLVED_PRE_TEST"
    assert pair["pncs"]["native_ci"]["code_test_failure_observed"] is False


def test_physical_cross_binding_gate_remains_explicit():
    pair = _load(PAIR)
    assert pair["interface"]["physical_cross_binding"] == "OPEN"
