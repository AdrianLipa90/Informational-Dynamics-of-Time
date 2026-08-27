import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / "validation" / "IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1.json"
LOCK = ROOT / "validation" / "01X_RFC_CROSS_REFERENCE_LOCK_V0_1.json"
EXPECTED_PNCS = "e6d5e217aeed2906372fdd0aa41845f0df32bbae"
EXPECTED_LOOPS = [
    "SOURCE.CARRIER.NORMALIZATION.ROUNDTRIP",
    "SOURCE.CARRIER.Q0_OCCUPATION.ROUNDTRIP",
    "SOURCE.CARRIER.EPSILON_MASS_DENSITY.ROUNDTRIP",
    "SOURCE.PHASE_INTENTION.EULER_CHARGE_ENERGY.ROUNDTRIP",
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
        lock["interface_contract"]["pncs_euler_energy_loop"],
    ] == EXPECTED_LOOPS


def test_pair_receipt_records_executed_peer_reference_gates():
    pair = _load(PAIR)
    assert pair["idt"]["status"] == "PASS"
    assert pair["idt"]["passed"] >= 347
    assert pair["idt"]["failed"] == 0
    assert pair["rfc"]["status"] == "PASS"
    assert pair["rfc"]["passed"] >= 39
    assert pair["rfc"]["failed"] == 0
    assert pair["pncs"]["native_ci"]["classification"] == "CI_EXECUTION_UNRESOLVED_PRE_TEST"
    assert pair["pncs"]["native_ci"]["code_test_failure_observed"] is False


def test_epsilon_derivation_is_ordered_after_euler_closure():
    pair = _load(PAIR)
    assert pair["interface"]["euler_closed_action_charge"] == "J_I^EB=hbar*theta_I^EB"
    assert pair["interface"]["rotor_energy"] == "H_Phi^EB=(J-J_I^EB)^2/(2 I_phi)"
    assert pair["interface"]["energy_per_action_charge"] == "epsilon_I^EB=H_Phi^EB/J_I^EB"


def test_physical_cross_binding_gate_remains_explicit():
    pair = _load(PAIR)
    assert pair["interface"]["physical_cross_binding"] == "OPEN"
