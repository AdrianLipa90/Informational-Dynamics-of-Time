import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PAIR = ROOT / "validation" / "IDT_RFC_PNCS_SOURCE_HOLONOMY_PAIR_V0_1.json"
LOCK = ROOT / "validation" / "01X_RFC_CROSS_REFERENCE_LOCK_V0_1.json"
EXPECTED_PNCS = "26fb4714a7d7e71f16024f2120f93099a9c62c01"
EXPECTED_LOOPS = [
    "SOURCE.CARRIER.NORMALIZATION.ROUNDTRIP",
    "SOURCE.CARRIER.Q0_OCCUPATION.ROUNDTRIP",
    "SOURCE.CARRIER.EPSILON_MASS_DENSITY.ROUNDTRIP",
    "SOURCE.PHASE_INTENTION.EULER_CHARGE_ENERGY.ROUNDTRIP",
    "SOURCE.PHASE_NOETHER.COLLECTIVE_CARRIER.ROUNDTRIP",
    "SOURCE.PHASE_NOETHER.RFC_CONSERVED_CURRENT.ROUNDTRIP",
    "SOURCE.PHASE_NOETHER.ROTOR_INERTIA.REDUCTION.ROUNDTRIP",
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
        lock["interface_contract"]["pncs_scalar_field_rotor_loop"],
    ] == EXPECTED_LOOPS


def test_pair_receipt_records_executed_peer_reference_gates():
    pair = _load(PAIR)
    assert pair["idt"]["status"] == "PASS"
    assert pair["idt"]["passed"] >= 373
    assert pair["idt"]["failed"] == 0
    assert pair["rfc"]["status"] == "PASS"
    assert pair["rfc"]["passed"] >= 65
    assert pair["rfc"]["failed"] == 0
    assert pair["pncs"]["native_ci"]["classification"] == "CI_EXECUTION_UNRESOLVED_PRE_TEST"
    assert pair["pncs"]["native_ci"]["code_test_failure_observed"] is False


def test_scalar_field_rotor_reduction_is_typed_separately_from_01z_defect():
    interface = _load(PAIR)["interface"]
    assert interface["legacy_inertia_binding_defect"] == "Delta_I_01Z=abs(I_A/I_phi-1)"
    assert interface["scalar_field_phase_coefficient"] == "C_A=sum_a A_a^2 V_a"
    assert interface["scalar_field_collective_inertia"] == "I_A=2*C_A"
    assert interface["scalar_field_rotor_reduction_defect"] == "Delta_I_reduction=abs(I_phi-I_A)/I_A"
    assert interface["exact_reduction_identity"] == (
        "common positive D_tau_chi => Delta_I_reduction=Delta_coefficient=Delta_Q_reduction=Delta_epsilon_reduction"
    )
    assert interface["exact_inertia_binding_reduction"] == (
        "I_A=I_phi => Q_theta=P_Phi^EB and epsilon_N^EB=P_Phi^EB/(2 I_phi)=(1/2)D_tau_chi"
    )


def test_exact_current_measure_bound_and_anti_false_positive_witness_are_explicit():
    pair = _load(PAIR)
    interface = pair["interface"]
    assert interface["common_slice_gate"] == "same slice_id, normal orientation, measure_id and ordered cell_ids"
    assert interface["local_current_binding_defect"] == "Delta_J=sum_a V_Q,a*abs(j_Q,a-j_theta,a)/Q_theta"
    assert interface["measure_binding_defect"] == "Delta_V=sum_a abs(V_Q,a-V_theta,a)*abs(j_theta,a)/Q_theta"
    assert interface["total_charge_binding_defect"] == "Delta_Sigma=abs(Q_Sigma-Q_theta)/Q_theta"
    assert interface["exact_defect_bound"] == "Delta_Sigma <= Delta_J + Delta_V"
    witness = pair["anti_false_positive_witness"]
    assert witness["Q_theta"] == witness["Q_Sigma"] == 4.0
    assert witness["Delta_Sigma"] == 0.0
    assert witness["Delta_J"] == 0.5
    assert witness["Delta_V"] == 0.0
    assert witness["binding_verdict"] == "FAIL_LOCAL_CURRENT"


def test_physical_promotion_remains_explicit_after_reduction_theorem():
    pair = _load(PAIR)
    assert pair["interface"]["collective_reduction_gate"] == (
        "same field/rotor phase mode, covariant-rate ID, measure ID and ordered collective support"
    )
    assert pair["interface"]["physical_cross_binding"] == "OPEN_COMMON_PHASE_RATE_MEASURE_CURRENT_PROMOTION"
