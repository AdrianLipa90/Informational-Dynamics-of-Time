from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREREG = ROOT / "experiments" / "E004_retrocausal_preregistration" / "preregistration_v0_1.json"
GRAPH = ROOT / "validation" / "dependency_graph.json"


def _prereg():
    return json.loads(PREREG.read_text())


def _nodes():
    return {item["id"]: item for item in json.loads(GRAPH.read_text())["nodes"]}


def test_preregistration_keeps_execution_and_claim_gates_closed() -> None:
    doc = _prereg()
    assert doc["status"] == "PREREGISTRATION_READY_EXECUTION_GATED_BY_RETRODICTION_ADMISSION"
    assert doc["dependency"]["required_node"] == "RETRODICTION"
    assert doc["dependency"]["execution_gate"] == "GATED"
    assert doc["dependency"]["physical_claim_gate"] == "GATED"
    assert doc["dependency"]["active_blocker"] == "AUGMENTED_GLOBAL_DOMAIN_COVERAGE_ACTIVE_NEXT_GATE"
    assert "EXECUTION_AND_PHYSICAL_CLAIM_GATE_GATED" in _nodes()["RETROCAUSAL_TESTS"]["status"]


def test_evidence_chain_is_frozen_in_required_order() -> None:
    assert _prereg()["evidence_chain"] == [
        "RAW_OBSERVATION",
        "STATISTICAL_EFFECT",
        "CLASSICAL_CHANNEL_AUDIT",
        "PHYSICAL_CLAIM_STATUS",
    ]


def test_future_condition_is_generated_after_sealed_observation() -> None:
    doc = _prereg()
    assert doc["ordered_events"] == ["t0", "tS", "tF", "tR"]
    assert doc["required_temporal_inequality"] == "t0 < tS < tF < tR"
    assert doc["future_condition"]["generation_after_seal"] is True
    assert doc["future_condition"]["independent_rng_required"] is True
    assert doc["future_condition"]["raw_rng_record_required"] is True


def test_confirmatory_statistical_contract_is_fixed() -> None:
    statistic = _prereg()["primary_statistic"]
    assert statistic["alternative"] == "two-sided"
    assert statistic["alpha"] == 0.005
    assert statistic["permutations"] == 100000
    sample = _prereg()["sample_rule"]
    assert sample["valid_trials_target"] == 4096
    assert sample["attempted_trials_ceiling"] == 4608
    assert sample["outcome_dependent_stopping"] is False


def test_claim_transition_requires_audit_retrodiction_and_replication() -> None:
    transition = _prereg()["claim_transition"]
    assert transition == {
        "statistical_significance_required": True,
        "classical_channel_audit_pass_required": True,
        "retrodiction_admission_required": True,
        "independent_replication_required": True,
    }
