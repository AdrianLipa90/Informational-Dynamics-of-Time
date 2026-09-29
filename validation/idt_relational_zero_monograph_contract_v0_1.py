#!/usr/bin/env python3
"""Fail-closed source contract for the IDT relational-zero monograph entrypoint."""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MASTER = ROOT / "monograph/main.tex"
ENTRY = ROOT / "monograph/chapters/02_tir_entrypoint.tex"
CROSSLINK = ROOT / "formalism/00A_tir_relational_zero_entrypoint.md"
DEP_GRAPH = ROOT / "formalism/DEPENDENCY_GRAPH.md"
STATUS = ROOT / "CURRENT_STATUS.md"
EXPORT = ROOT / "DEPENDENCY_EXPORT.json"

EXPECTED_TIR_HEAD = "7c468d83f1c0c6b4972ed0d9396b96333d24a623"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def main() -> int:
    checks: dict[str, bool] = {}
    detail: dict[str, object] = {}

    required = (MASTER, ENTRY, CROSSLINK, DEP_GRAPH, STATUS, EXPORT)
    checks["required_surfaces_exist"] = all(path.is_file() for path in required)
    if not checks["required_surfaces_exist"]:
        missing = [str(p.relative_to(ROOT)) for p in required if not p.is_file()]
        print(json.dumps({"schema": "IDT_RELATIONAL_ZERO_MONOGRAPH_CONTRACT_V0_1",
                          "technical_status": "FAIL",
                          "missing": missing}, indent=2))
        return 1

    master = read(MASTER)
    entry = read(ENTRY)
    crosslink = read(CROSSLINK)
    dep_graph = read(DEP_GRAPH)
    status_text = read(STATUS)
    export = json.loads(read(EXPORT))

    tir_include = r"\include{chapters/02_tir_entrypoint}"
    info_include = r"\include{chapters/01_information}"
    checks["tir_entry_precedes_information"] = (
        master.count(tir_include) == 1
        and master.count(info_include) == 1
        and master.index(tir_include) < master.index(info_include)
    )

    root_tokens = (
        r"\mathfrak Z_{\rm rel}",
        r"(\varnothing,\varnothing)",
        r"\mathcal P=\{p\}",
        r"\Pi_1=\{N,S\}",
        r"\frac12",
        r"\ln2",
        r"\mathbb C^2",
    )
    checks["entry_contains_relational_root_chain"] = all(token in entry for token in root_tokens)

    firewall_tokens = (
        r"0_{\rm rel}",
        "t=0",
        r"\tau_{\rm int}=0",
        "vacuum state",
        "initial event",
    )
    checks["entry_zero_is_not_temporal_zero"] = all(token in entry for token in firewall_tokens)
    checks["entry_has_no_zero_to_physical_promotion"] = (
        "relational zero alone generates temporal dynamics" not in entry.lower()
        and "relational zero is physical time" not in entry.lower()
    )

    checks["crosslink_declares_pretemporal_boundary"] = all(token in crosslink for token in (
        r"\mathfrak Z_{\rm rel}",
        r"(\varnothing,\varnothing)",
        "minimal nontrivial distinction",
        "physical time zero",
        "vacuum state",
        "NOT CLAIMED",
    ))

    pin_match = re.search(r"Synchronized TIR branch foundation pin: `([0-9a-f]{40})`.", crosslink)
    crosslink_pin = pin_match.group(1) if pin_match else None
    checks["crosslink_has_exact_40hex_pin"] = crosslink_pin == EXPECTED_TIR_HEAD

    root_claim = next(
        (c for c in export.get("claims", [])
         if c.get("claim_id") == "IDT.TIR.RELATIONAL_ZERO_ENTRYPOINT"),
        None,
    )
    root_edge = next(
        (e for e in export.get("local_edges", [])
         if e.get("from") == "IDT.TIR.RELATIONAL_ZERO_ENTRYPOINT"
         and e.get("to") == "IDT.TEMPORAL.PRIMITIVE"),
        None,
    )
    old_zero = next(
        (c for c in export.get("claims", [])
         if c.get("claim_id") == "IDT.HALF_SEAM.RELATIONAL_ZERO"),
        None,
    )

    checks["export_root_claim_typed"] = bool(
        root_claim
        and "RELATIONAL_ZERO_TYPED" in root_claim.get("status", "")
        and root_claim.get("evidence_class") == "cross_repo_foundational_import"
        and root_claim.get("upstream_exact_head") == EXPECTED_TIR_HEAD
    )
    checks["crosslink_and_export_pin_identical"] = bool(
        root_claim and crosslink_pin == root_claim.get("upstream_exact_head")
    )
    checks["root_edge_fail_closed"] = bool(
        root_edge
        and root_edge.get("authority") == "CANDIDATE_ONLY"
        and root_edge.get("promotion_required") is True
        and root_edge.get("promotion_gate") == "TIR_RELATIONAL_ZERO_BRANCH_MERGE_AND_CROSS_REPO_PIN"
    )
    checks["legacy_zero_claim_superseded"] = (
        old_zero is None
        or "SUPERSEDED_BY_IDT.TIR.RELATIONAL_ZERO_ENTRYPOINT" in old_zero.get("status", "")
    )

    checks["dependency_graph_exposes_root"] = all(token in dep_graph for token in (
        r"\mathfrak Z_{\rm rel}",
        r"\mathrm{Temporal\ Primitive}",
        "Relational zero is neither",
    ))
    checks["status_exposes_pretemporal_root"] = all(token in status_text for token in (
        r"\mathfrak Z_{\rm rel}",
        r"not \(t=0\)",
        "pre-temporal",
    ))

    stale = ("zero relational carrier", "zero distinction", "H_singleton")
    combined = "\n".join((entry, crosslink, dep_graph, status_text)).lower()
    checks["no_stale_zero_terminology"] = all(term.lower() not in combined for term in stale)

    source_commit = export.get("source_commit")
    checks["export_source_commit_is_40hex"] = bool(
        isinstance(source_commit, str)
        and re.fullmatch(r"[0-9a-f]{40}", source_commit)
    )

    detail["expected_tir_head"] = EXPECTED_TIR_HEAD
    detail["crosslink_pin"] = crosslink_pin
    detail["export_upstream_head"] = root_claim.get("upstream_exact_head") if root_claim else None
    detail["export_source_commit"] = source_commit

    failed = sorted(key for key, value in checks.items() if not value)
    technical_status = "PASS" if not failed else "FAIL"
    receipt = {
        "schema": "IDT_RELATIONAL_ZERO_MONOGRAPH_CONTRACT_V0_1",
        "technical_status": technical_status,
        "physical_promotion": False,
        "checks": checks,
        "failed": failed,
        "detail": detail,
    }
    print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0 if technical_status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
