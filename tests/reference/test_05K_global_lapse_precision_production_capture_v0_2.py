from decimal import Decimal, getcontext, localcontext

from src.idt.global_lapse_precision_production_capture import (
    GlobalLapsePrecisionCaptureError,
    _canonical_sha,
    build_precision_capture_dataset,
    certify_precision_capture_dataset,
    fractional_offset_from_log_ratio,
    log_ratio_from_fractional_offset,
)


def _base(source_class="REFERENCE_CONTROL", production=False):
    vals=["-2.943597600750136e-19","-6.43016785640077e-19","-8.427872488195288e-19","-11.955018632210269e-19"]
    return build_precision_capture_dataset(
        dataset_id="clock-realdata-control", realization_id="physical:R1", clock_id="C1", reference_patch_id="h0",
        patch_ids=["h0","h1","h2","h3","h4"],
        clock_ratio_edges=[{"x_patch_id":f"h{i}","y_patch_id":"h0","fractional_offset":v} for i,v in enumerate(vals,1)],
        source_owner="control", source_reference="doi:10.5281/zenodo.8184043#Fig3.csv",
        source_commit_or_digest="external-reference", source_class=source_class, production=production,
    )


def test_legacy_float64_collapses_real_scale_but_decimal_roundtrip_does_not():
    vals=[Decimal("-2.943597600750136e-19"),Decimal("-6.43016785640077e-19"),Decimal("-8.427872488195288e-19"),Decimal("-11.955018632210269e-19")]
    assert all(1.0+float(v)==1.0 for v in vals)
    for d in vals:
        l=log_ratio_from_fractional_offset(d)
        assert fractional_offset_from_log_ratio(l)==d


def test_real_scale_star_reconstructs_exactly_at_80_digits():
    cert=certify_precision_capture_dataset(_base())
    assert Decimal(cert.max_log_residual)==0
    assert cert.patch_count==5


def test_injected_1e_minus_22_cycle_defect_fails_closed():
    data=_base()
    l1=Decimal(data["clock_ratio_edges"][0]["log_N_x_given_y"])
    l2=Decimal(data["clock_ratio_edges"][1]["log_N_x_given_y"])
    data["clock_ratio_edges"].append({"x_patch_id":"h2","y_patch_id":"h1","log_N_x_given_y":str((l2-l1)+Decimal("1e-22"))})
    data["dataset_sha256"]=_canonical_sha({k:v for k,v in data.items() if k!="dataset_sha256"})
    try:
        certify_precision_capture_dataset(data)
    except GlobalLapsePrecisionCaptureError:
        return
    raise AssertionError("1e-22 cycle defect must be rejected")


def test_reverse_edge_uses_exact_decimal_negation_regression():
    getcontext().prec=28
    with localcontext() as ctx:
        ctx.prec=80
        l=log_ratio_from_fractional_offset(Decimal("-2.943597600750136e-19"))
    assert l.copy_negate()+l==0
    assert (-l)+l!=0


def test_production_flag_requires_production_source():
    try:
        _base("REFERENCE_CONTROL", True)
    except GlobalLapsePrecisionCaptureError:
        return
    raise AssertionError("reference source must not self-promote")


def test_digest_tamper_fails_closed():
    data=_base(); data["dataset_sha256"]="0"*64
    try:
        certify_precision_capture_dataset(data)
    except GlobalLapsePrecisionCaptureError:
        return
    raise AssertionError("digest tamper must be rejected")


def test_production_shape_is_review_eligible_but_never_self_canonizes():
    cert=certify_precision_capture_dataset(_base("PRODUCTION_SOURCE", True))
    assert cert.production_input and cert.promotion_review_eligible
    assert cert.canon_allowed is False
