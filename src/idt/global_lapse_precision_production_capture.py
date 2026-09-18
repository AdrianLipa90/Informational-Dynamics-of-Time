from __future__ import annotations

import hashlib, json
from dataclasses import dataclass
from decimal import Decimal, InvalidOperation, localcontext
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "IDT_GLOBAL_LAPSE_PRECISION_CAPTURE_V0_2"
ENCODING = "DECIMAL_LOG_N"
ALLOWED_SOURCE_CLASSES = {"PRODUCTION_SOURCE", "REFERENCE_CONTROL", "CANDIDATE_SOURCE", "EXTERNAL_PROCESS_DATA_REFERENCE"}

class GlobalLapsePrecisionCaptureError(ValueError):
    pass

D = Decimal

def _id(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise GlobalLapsePrecisionCaptureError(f"{name} must be a non-empty string")
    return value.strip()

def _dec(value: Any, name: str) -> Decimal:
    try: out=D(str(value))
    except (InvalidOperation, ValueError, TypeError) as exc: raise GlobalLapsePrecisionCaptureError(f"{name} must parse as Decimal") from exc
    if not out.is_finite(): raise GlobalLapsePrecisionCaptureError(f"{name} must be finite")
    return out

def log_ratio_from_fractional_offset(delta: Any, *, precision: int=80) -> Decimal:
    d=_dec(delta,"fractional_offset")
    if d <= -1: raise GlobalLapsePrecisionCaptureError("fractional_offset must satisfy delta > -1")
    with localcontext() as ctx:
        ctx.prec=precision
        return +(D(1)+d).ln()

def fractional_offset_from_log_ratio(log_n: Any, *, precision: int=80) -> Decimal:
    x=_dec(log_n,"log_N_x_given_y")
    with localcontext() as ctx:
        ctx.prec=precision
        return +(x.exp()-D(1))

def _normalize_edge(edge: Mapping[str,Any], index: int, precision: int) -> dict[str,str]:
    if not isinstance(edge, Mapping): raise GlobalLapsePrecisionCaptureError(f"edge {index} must be an object")
    x=_id(edge.get("x_patch_id"),f"edge {index} x_patch_id"); y=_id(edge.get("y_patch_id"),f"edge {index} y_patch_id")
    has_log="log_N_x_given_y" in edge; has_delta="fractional_offset" in edge
    if has_log == has_delta: raise GlobalLapsePrecisionCaptureError(f"edge {index} must provide exactly one of log_N_x_given_y or fractional_offset")
    logn=_dec(edge["log_N_x_given_y"],f"edge {index} log_N_x_given_y") if has_log else log_ratio_from_fractional_offset(edge["fractional_offset"],precision=precision)
    return {"x_patch_id":x,"y_patch_id":y,"log_N_x_given_y":str(logn)}

def _normalize_provenance(prov: Mapping[str,Any]) -> dict[str,str]:
    if not isinstance(prov,Mapping): raise GlobalLapsePrecisionCaptureError("provenance must be an object")
    source_class=_id(prov.get("source_class"),"provenance.source_class")
    if source_class not in ALLOWED_SOURCE_CLASSES: raise GlobalLapsePrecisionCaptureError("unsupported provenance.source_class")
    return {"source_owner":_id(prov.get("source_owner"),"provenance.source_owner"),"source_reference":_id(prov.get("source_reference"),"provenance.source_reference"),"source_commit_or_digest":_id(prov.get("source_commit_or_digest"),"provenance.source_commit_or_digest"),"source_class":source_class}

def _canonical_sha(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()

def build_precision_capture_dataset(*,dataset_id:str,realization_id:str,clock_id:str,reference_patch_id:str,patch_ids:Sequence[str],clock_ratio_edges:Sequence[Mapping[str,Any]],source_owner:str,source_reference:str,source_commit_or_digest:str,source_class:str,production:bool,precision_digits:int=80,tolerance_log:str="1e-40") -> dict[str,Any]:
    if not isinstance(precision_digits,int) or precision_digits<28: raise GlobalLapsePrecisionCaptureError("precision_digits must be integer >= 28")
    tol=_dec(tolerance_log,"tolerance_log")
    if tol<=0: raise GlobalLapsePrecisionCaptureError("tolerance_log must be positive")
    patches=[_id(v,"patch_id") for v in patch_ids]
    if not patches or len(set(patches))!=len(patches): raise GlobalLapsePrecisionCaptureError("patch_ids must be non-empty and unique")
    edges=[_normalize_edge(e,i,precision_digits) for i,e in enumerate(clock_ratio_edges)]
    if not edges: raise GlobalLapsePrecisionCaptureError("clock_ratio_edges must be non-empty")
    prov=_normalize_provenance({"source_owner":source_owner,"source_reference":source_reference,"source_commit_or_digest":source_commit_or_digest,"source_class":source_class})
    if bool(production) != (source_class=="PRODUCTION_SOURCE"): raise GlobalLapsePrecisionCaptureError("production must be true iff source_class=PRODUCTION_SOURCE")
    data={"schema":SCHEMA,"encoding":ENCODING,"precision_digits":precision_digits,"tolerance_log":str(tol),"dataset_id":_id(dataset_id,"dataset_id"),"realization_id":_id(realization_id,"realization_id"),"clock_id":_id(clock_id,"clock_id"),"reference_patch_id":_id(reference_patch_id,"reference_patch_id"),"patch_ids":patches,"clock_ratio_edges":edges,"provenance":prov,"production":bool(production)}
    data["dataset_sha256"]=_canonical_sha(data)
    return data

@dataclass(frozen=True)
class GlobalLapsePrecisionCertificate:
    input_valid: bool; integrity_valid: bool; cocycle_valid: bool; patch_coverage_valid: bool
    production_input: bool; promotion_review_eligible: bool; canon_allowed: bool
    dataset_id: str; realization_id: str; clock_id: str; reference_patch_id: str; dataset_sha256: str
    encoding: str; precision_digits: int; tolerance_log: str; max_log_residual: str; patch_count: int; edge_count: int
    patch_log_lapse: dict[str,str]; patch_fractional_lapse: dict[str,str]; source_class: str

def certify_precision_capture_dataset(data: Mapping[str,Any], *, expected_patch_ids: Iterable[str]|None=None) -> GlobalLapsePrecisionCertificate:
    if not isinstance(data,Mapping) or data.get("schema")!=SCHEMA: raise GlobalLapsePrecisionCaptureError(f"schema must equal {SCHEMA}")
    if data.get("encoding")!=ENCODING: raise GlobalLapsePrecisionCaptureError(f"encoding must equal {ENCODING}")
    precision=data.get("precision_digits")
    if not isinstance(precision,int) or precision<28: raise GlobalLapsePrecisionCaptureError("precision_digits must be integer >= 28")
    tol=_dec(data.get("tolerance_log"),"tolerance_log")
    if tol<=0: raise GlobalLapsePrecisionCaptureError("tolerance_log must be positive")
    patches=[_id(v,"patch_id") for v in data.get("patch_ids",[])]
    if not patches or len(set(patches))!=len(patches): raise GlobalLapsePrecisionCaptureError("patch_ids must be non-empty and unique")
    ref=_id(data.get("reference_patch_id"),"reference_patch_id")
    if ref not in set(patches): raise GlobalLapsePrecisionCaptureError("reference_patch_id must belong to patch_ids")
    prov=_normalize_provenance(data.get("provenance"))
    prod=data.get("production")
    if type(prod) is not bool: raise GlobalLapsePrecisionCaptureError("production must be boolean")
    if prod != (prov["source_class"]=="PRODUCTION_SOURCE"): raise GlobalLapsePrecisionCaptureError("production/source_class mismatch")
    expected_sha=_canonical_sha({k:v for k,v in data.items() if k!="dataset_sha256"})
    if data.get("dataset_sha256")!=expected_sha: raise GlobalLapsePrecisionCaptureError("dataset_sha256 mismatch")
    edges=[_normalize_edge(e,i,precision) for i,e in enumerate(data.get("clock_ratio_edges",[]))]
    if not edges: raise GlobalLapsePrecisionCaptureError("clock_ratio_edges must be non-empty")
    pset=set(patches)
    adj={p:[] for p in patches}; clean=[]
    for e in edges:
        x,y=e["x_patch_id"],e["y_patch_id"]
        if x not in pset or y not in pset: raise GlobalLapsePrecisionCaptureError("clock-ratio edge endpoint is outside patch_ids")
        l=_dec(e["log_N_x_given_y"],"log_N")
        clean.append((x,y,l)); adj[y].append((x,l)); adj[x].append((y,l.copy_negate()))
    with localcontext() as ctx:
        ctx.prec=precision
        rates={ref:D(0)}; queue=[ref]; maxr=D(0)
        while queue:
            s=queue.pop(0)
            for t,inc in adj[s]:
                cand=rates[s]+inc
                if t not in rates: rates[t]=cand; queue.append(t)
                else:
                    r=abs(rates[t]-cand); maxr=max(maxr,r)
                    if r>tol: raise GlobalLapsePrecisionCaptureError(f"additive log cocycle failed: residual={r}")
        if set(rates)!=pset: raise GlobalLapsePrecisionCaptureError("clock graph disconnected")
        for x,y,l in clean:
            r=abs((rates[x]-rates[y])-l); maxr=max(maxr,r)
            if r>tol: raise GlobalLapsePrecisionCaptureError(f"log edge incompatible with global potential: residual={r}")
        logs={k:str(+rates[k]) for k in sorted(rates)}
        offs={k:str(+(rates[k].exp()-D(1))) for k in sorted(rates)}
    if expected_patch_ids is not None and set(map(str,expected_patch_ids))!=pset: raise GlobalLapsePrecisionCaptureError("patch coverage mismatch")
    return GlobalLapsePrecisionCertificate(True,True,True,True,prod,prod,False,_id(data.get("dataset_id"),"dataset_id"),_id(data.get("realization_id"),"realization_id"),_id(data.get("clock_id"),"clock_id"),ref,expected_sha,ENCODING,precision,str(tol),str(maxr),len(patches),len(edges),logs,offs,prov["source_class"])
