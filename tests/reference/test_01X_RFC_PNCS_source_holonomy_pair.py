import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / "validation" / "IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1.json"
LOCK = ROOT / "validation" / "01X_RFC_CROSS_REFERENCE_LOCK_V0_1.json"
EXPECTED_PNCS = "5276133cf2ab6e47b6a4737d9671a1a8f0386a11"
EXPECTED_LOOPS = [
    "SOURCE.CARRIER.NORMALIZATION.ROUNDTRIP",
    "SOURCE.CARRIER.Q0_OCCUPATION.ROUNDTRIP",
    "SOURCE.CARRIER.EPSILON_MASS_DENSITY.ROUNDTRIP",
    "SOURCE.PHASE_INTENTION.EULER_CHARGE_ENERGY.ROUNDTRIP",
    "SOURCE.PHASE_NOETHER.COLLECTIVE_CARRIER.ROUNDTRIP",
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
        lock["interface_contract"]["pncs_noether_carrier_loop"],
    ] == EXPECTED_LOOPS


def test_pair_receipt_records_executed_peer_reference_gates():
    pair = _load(PAIR)
    assert pair["idt"]["status"] == "PASS"
    assert pair["idt"]["passed"] >= 355
    assert pair["idt"]["failed"] == 0
    assert pair["rfc"]["status"] == "PASS"
    assert pair["rfc"]["passed"] >= 47
    assert pair["rfc"]["failed"] == 0
    assert pair["pncs"]["native_ci"]["classification"] == "CI_EXECUTION_UNRESOLVED_PRE_TEST"
    assert pair["pncs"]["native_ci"]["code_test_failure_observed"] is False


def test_noether_carrier_is_distinct_from_intention_charge():
    pair = _load(PAIR)
    assert pair["interface"]["euler_closed_intention_charge"] == "J_I^EB=hbar*theta_I^EB"
    assert pair["interface"]["preferred_rotor_carrier"] == "P_Phi^EB=J-J_I^EB"
    assert pair["interface"]["noether_collective_charge"] == "Q_theta=I_A*(P_Phi^EB/I_phi)"
    assert pair["interface"]["preferred_energy_per_carrier"] == "epsilon_N^EB=H_Phi^EB/P_Phi^EB=P_Phi^EB/(2 I_phi)"


def test_inertia_binding_defect_remains_explicit():
    pair = _load(PAIR)
    assert pair["interface"]["inertia_binding_defect"] == "Delta_I=abs(I_A/I_phi-1)"
    assert pair["interface"]["physical_cross_binding"] == "OPEN"
