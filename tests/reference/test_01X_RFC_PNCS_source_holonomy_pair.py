import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / "validation" / "IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1.json"
LOCK = ROOT / "validation" / "01X_RFC_CROSS_REFERENCE_LOCK_V0_1.json"
EXPECTED_PNCS = "f7b428f4dc30ddeb1280c9213c5788f576a54db4"
EXPECTED_LOOPS = [
    "SOURCE.CARRIER.NORMALIZATION.ROUNDTRIP",
    "SOURCE.CARRIER.Q0_OCCUPATION.ROUNDTRIP",
    "SOURCE.CARRIER.EPSILON_MASS_DENSITY.ROUNDTRIP",
    "SOURCE.PHASE_INTENTION.EULER_CHARGE_ENERGY.ROUNDTRIP",
    "SOURCE.PHASE_NOETHER.COLLECTIVE_CARRIER.ROUNDTRIP",
    "SOURCE.PHASE_NOETHER.RFC_CONSERVED_CURRENT.ROUNDTRIP",
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
        lock["interface_contract"]["pncs_noether_rfc_current_loop"],
    ] == EXPECTED_LOOPS


def test_pair_receipt_records_executed_peer_reference_gates():
    pair = _load(PAIR)
    assert pair["idt"]["status"] == "PASS"
    assert pair["idt"]["passed"] >= 370
    assert pair["idt"]["failed"] == 0
    assert pair["rfc"]["status"] == "PASS"
    assert pair["rfc"]["passed"] >= 62
    assert pair["rfc"]["failed"] == 0
    assert pair["pncs"]["native_ci"]["classification"] == "CI_EXECUTION_UNRESOLVED_PRE_TEST"
    assert pair["pncs"]["native_ci"]["code_test_failure_observed"] is False


def test_noether_carrier_is_distinct_from_intention_charge_and_rotor_coordinate():
    pair = _load(PAIR)
    interface = pair["interface"]
    assert interface["euler_closed_intention_charge"] == "J_I^EB=hbar*theta_I^EB"
    assert interface["rotor_kinetic_carrier"] == "P_Phi^EB=J-J_I^EB"
    assert interface["noether_collective_charge"] == "Q_theta=I_A*(P_Phi^EB/I_phi)"
    assert interface["energy_per_finite_noether_carrier"] == "epsilon_N^EB=H_Phi^EB/Q_theta"
    assert interface["exact_inertia_binding_reduction"] == (
        "I_A=I_phi => Q_theta=P_Phi^EB and epsilon_N^EB=P_Phi^EB/(2 I_phi)=(1/2)D_tau_chi"
    )


def test_current_binding_defects_and_anti_false_positive_witness_are_explicit():
    pair = _load(PAIR)
    interface = pair["interface"]
    assert interface["local_current_binding_defect"] == "Delta_local=sum_a V_a*abs(j_Q,a-j_theta,a)/Q_theta"
    assert interface["total_charge_binding_defect"] == "Delta_Q=abs(Q_Sigma-Q_theta)/Q_theta"
    assert interface["side_flux_defect"] == "Delta_F=abs(F_side)"
    witness = pair["anti_false_positive_witness"]
    assert witness["Q_theta"] == witness["Q_Sigma"] == 4.0
    assert witness["Delta_Q"] == 0.0
    assert witness["Delta_local"] == 0.5
    assert witness["binding_verdict"] == "FAIL_LOCAL_CURRENT"


def test_physical_promotion_remains_explicit_after_zero_defect_candidate_gate():
    pair = _load(PAIR)
    assert pair["interface"]["inertia_binding_defect"] == "Delta_I=abs(I_A/I_phi-1)"
    assert pair["interface"]["physical_cross_binding"] == "OPEN_PROMOTION_AFTER_ZERO_DEFECT_CURRENT_GATE"
