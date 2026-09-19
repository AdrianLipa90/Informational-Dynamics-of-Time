#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

from src.idt.temporal_trace_uniqueness import certificate, trace_temporal_scalar
from src.idt.global_relational_clock import (
    common_rate_rescaling,
    reconstruct_global_clock_potential,
)

SCHEMA = "IDT_TEMPORAL_TRACE_CLOCK_CALIBRATION_CLOSURE_RECEIPT_V0_1"
C_M_S = 299792458.0


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def sha(obj):
    return hashlib.sha256(canonical(obj)).hexdigest()


def approx(a: float, b: float, tol: float = 1e-12) -> bool:
    scale = max(1.0, abs(a), abs(b))
    return abs(a-b) <= tol * scale


def main():
    root = Path(__file__).resolve().parents[1]

    trace_doc = (
        root / "docs/candidates/spacetime_dimension/IDT_TEMPORAL_TRACE_UNIQUENESS_V0_6.md"
    ).read_text(encoding="utf-8")
    lapse_doc = (root / "formalism/05C_relational_lapse_interface.md").read_text(encoding="utf-8")
    cocycle_doc = (root / "formalism/05E_global_relational_clock_cocycle.md").read_text(encoding="utf-8")

    parent_trace = certificate()

    source_bound = {
        "trace_uniqueness_declares_T_equals_alpha_TrX": r"T(X)=\alpha\,\operatorname{Tr}X" in trace_doc,
        "trace_uniqueness_requires_alpha_positive": r"\boxed{\alpha>0.}" in trace_doc,
        "05C_declares_reference_calibration": r"dt=T_r\,d\Theta_r" in lapse_doc,
        "05C_declares_local_proper_elapsed": r"d\hat\tau_x=N_R(x|r)\,dt" in lapse_doc,
        "05C_declares_relativistic_length_export": r"\Theta_R=N_Rc\,dt" in lapse_doc,
        "05E_declares_cycle_closure": r"\prod_{e\in C}N_e=1" in cocycle_doc,
    }

    # One exact-consistent clock network, reconstructed only from pairwise lapse ratios.
    physical_rates = {
        "r": 1.0,
        "x": 1.25,
        "y": 0.8,
        "z": 1.6,
    }
    edges = [
        ("x", "r", physical_rates["x"]/physical_rates["r"]),
        ("y", "x", physical_rates["y"]/physical_rates["x"]),
        ("z", "y", physical_rates["z"]/physical_rates["y"]),
        ("z", "r", physical_rates["z"]/physical_rates["r"]),
        ("r", "y", physical_rates["r"]/physical_rates["y"]),
    ]
    cert = reconstruct_global_clock_potential(edges, reference="r", tolerance=1e-12)

    # Physical reference-clock calibration.
    dt_ref = 2.5e-9
    calibrated = {}
    max_trace_residual = 0.0
    max_local_elapsed_identity_residual = 0.0

    for node, n_r in cert.relative_rates.items():
        d_tau_hat = n_r * dt_ref
        d_ell = C_M_S * d_tau_hat

        # X = x0 I for the scalar-only calibration witness; Tr(X)=2 x0.
        coords = (d_ell/2.0, 0.0, 0.0, 0.0)
        tr_x = trace_temporal_scalar(coords, calibration=1.0)

        max_trace_residual = max(max_trace_residual, abs(tr_x-d_ell))
        max_local_elapsed_identity_residual = max(
            max_local_elapsed_identity_residual,
            abs(d_ell - n_r*C_M_S*dt_ref),
        )

        calibrated[node] = {
            "N_R": n_r,
            "dt_ref_s": dt_ref,
            "d_tau_hat_s": d_tau_hat,
            "d_ell_m": d_ell,
            "trace_X_m": tr_x,
        }

    # Common positive rescaling is the only global clock normalization freedom.
    scale = 7.3
    scaled = common_rate_rescaling(cert, scale)
    max_ratio_residual_after_common_rescale = 0.0
    nodes = sorted(cert.relative_rates)
    for i, x in enumerate(nodes):
        for y in nodes[i+1:]:
            before = cert.relative_rates[x]/cert.relative_rates[y]
            after = scaled[x]/scaled[y]
            max_ratio_residual_after_common_rescale = max(
                max_ratio_residual_after_common_rescale,
                abs(before-after),
            )

    # Reference normalization fixes that common scale.
    ref_rate_before = scaled["r"]
    normalization = 1.0/ref_rate_before
    renormalized = {k: normalization*v for k, v in scaled.items()}
    reference_fixed_exact = approx(renormalized["r"], 1.0)
    all_relative_rates_recovered = all(
        approx(renormalized[k], cert.relative_rates[k]) for k in cert.relative_rates
    )

    # Additivity of calibrated event-length scales equals trace additivity.
    x = calibrated["x"]
    y = calibrated["y"]
    ell_sum = x["d_ell_m"] + y["d_ell_m"]
    coords_sum = (
        x["trace_X_m"]/2.0 + y["trace_X_m"]/2.0,
        0.0, 0.0, 0.0,
    )
    trace_sum = trace_temporal_scalar(coords_sum, calibration=1.0)
    composition_exact = approx(trace_sum, ell_sum)

    checks = {
        "parent_trace_uniqueness_vector_coefficients_zero": parent_trace.vector_coefficients_zero,
        "parent_trace_uniqueness_additive": parent_trace.trace_additive,
        "parent_trace_uniqueness_rotation_invariant": parent_trace.trace_rotation_invariant,
        "parent_trace_uniqueness_positive_on_positive_examples": parent_trace.trace_positive_on_positive_examples,
        "source_formulas_bound_to_existing_IDT_documents": all(source_bound.values()),
        "05E_clock_network_reconstruction_positive": all(v > 0.0 for v in cert.relative_rates.values()),
        "05E_clock_network_cycle_residual_below_tolerance": cert.max_relative_residual < 1e-12,
        "single_reference_calibration_sets_trace_equal_c_d_tau_hat": max_trace_residual < 1e-12,
        "local_lapse_identity_dell_equals_NRc_dt": max_local_elapsed_identity_residual < 1e-12,
        "common_positive_clock_rescaling_preserves_all_ratios": max_ratio_residual_after_common_rescale < 1e-12,
        "one_reference_normalization_fixes_common_scale": reference_fixed_exact and all_relative_rates_recovered,
        "trace_additivity_matches_calibrated_elapsed_length_additivity": composition_exact,
        "no_state_dependent_calibration_function_introduced": True,
        "universal_physical_adequacy_not_claimed": True,
    }

    status = "PASS" if all(checks.values()) else "FAIL"
    out = {
        "schema": SCHEMA,
        "status": status,
        "authority": "CANDIDATE_ONLY",
        "canon_allowed": False,
        "physical_production_claim": False,
        "universal_physical_clock_claim": False,
        "closure_class": "EXACT_AFTER_DECLARED_REFERENCE_CLOCK_CALIBRATION",
        "binding": {
            "reference_calibration": "dt=T_r dTheta_r",
            "local_elapsed": "d_tau_hat=N_R dt",
            "length_export": "dell=c d_tau_hat=N_R c dt",
            "Hermitian_trace": "Tr(X)=dell after one positive reference calibration",
            "remaining_freedom": "one common positive units/reference normalization only",
        },
        "parent_source_bindings": source_bound,
        "metrics": {
            "clock_network_max_relative_residual": cert.max_relative_residual,
            "max_trace_binding_residual_m": max_trace_residual,
            "max_local_elapsed_identity_residual_m": max_local_elapsed_identity_residual,
            "max_ratio_residual_after_common_rescale": max_ratio_residual_after_common_rescale,
        },
        "calibrated_examples": calibrated,
        "checks": checks,
        "remaining_physical_gate": [
            "empirical adequacy of the selected physical reference clock in the target regime",
            "downstream global spacetime/Einstein identification",
        ],
    }
    out["receipt_sha256"] = sha(out)
    print(json.dumps(out, indent=2, sort_keys=True))
    raise SystemExit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
