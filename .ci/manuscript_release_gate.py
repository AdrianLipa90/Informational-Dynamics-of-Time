#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MASTER=ROOT/"monograph/main.tex"
GRAPH=ROOT/"DEPENDENCY_EXPORT.json"
VGRAPH=ROOT/"validation/dependency_graph.json"

def fail(msg): raise SystemExit("FAIL: "+msg)

s=MASTER.read_text(encoding="utf-8")
targets=re.findall(r"\\(?:input|include)\{([^}]+)\}",s)
if len(targets)!=len(set(targets)): fail("duplicate input/include target")
files=[MASTER]
for t in targets:
    p=ROOT/"monograph"/(t+".tex" if not Path(t).suffix else t)
    if not p.is_file(): fail(f"missing TeX source: {p}")
    files.append(p)
full="\n".join(p.read_text(encoding="utf-8") for p in files)
labels=re.findall(r"\\label\{([^}]+)\}",full)
refs=re.findall(r"\\(?:ref|eqref|pageref|autoref|cref|Cref|nameref)\{([^}]+)\}",full)
refs+=re.findall(r"\\hyperref\[([^]]+)\]",full)
cites=[k.strip() for m in re.findall(r"\\cite[a-zA-Z*]*\{([^}]+)\}",full) for k in m.split(",") if k.strip()]
bib=re.findall(r"\\bibitem(?:\[[^]]*\])?\{([^}]+)\}",full)
for name,seq in (("label",labels),("bibitem",bib)):
    d={x for x in seq if seq.count(x)>1}
    if d: fail(f"duplicate {name}s: {sorted(d)}")
mr=sorted(set(refs)-set(labels)); mc=sorted(set(cites)-set(bib))
if mr: fail(f"missing refs: {mr}")
if mc: fail(f"missing cites: {mc}")
if targets.index("chapters/02_tir_entrypoint") > targets.index("chapters/01_information"):
    fail("TIR entrypoint must precede information chapter")
for token in [
    r"\mathfrak Z_{\rm rel}",
    r"0_{\rm rel}",
    r"t=0",
    r"\tau_{\rm int}=0",
    "vacuum state",
    "initial event",
    "IDT imports this root rather than re-deriving or reinterpreting it",
]:
    if token not in full: fail(f"missing relational-zero firewall token: {token}")

def audit_graph(path,claim_key,edge_key):
    g=json.loads(path.read_text(encoding="utf-8"))
    nodes=g.get(claim_key,[])
    ids=[n.get("claim_id",n.get("id")) for n in nodes]
    if len(ids)!=len(set(ids)): fail(f"duplicate IDs in {path}")
    edges=g.get(edge_key,[])
    if edges:
        ss=set(ids)
        bad=[e for e in edges if e.get("from") not in ss or e.get("to") not in ss]
        if bad: fail(f"orphan edges in {path}: {bad}")
    return g,ids,edges

g,ids,edges=audit_graph(GRAPH,"claims","local_edges")
vg,vids,vedges=audit_graph(VGRAPH,"nodes","edges")
by={c["claim_id"]:c for c in g["claims"]}
entry=by.get("IDT.TIR.RELATIONAL_ZERO_ENTRYPOINT")
if not entry: fail("missing IDT.TIR.RELATIONAL_ZERO_ENTRYPOINT")
if "IDT_TEMPORAL_PROMOTION_FALSE" not in entry.get("status",""): fail("temporal non-promotion firewall missing")
bridge=[e for e in edges if e.get("from")=="IDT.TIR.RELATIONAL_ZERO_ENTRYPOINT" and e.get("to")=="IDT.TEMPORAL.PRIMITIVE"]
if len(bridge)!=1 or bridge[0].get("authority")!="CANDIDATE_ONLY" or not bridge[0].get("promotion_required"):
    fail(f"bad relational-zero -> temporal primitive edge: {bridge}")
print(json.dumps({
 "schema":"IDT_MANUSCRIPT_RELEASE_GATE_V0_1",
 "status":"PASS",
 "tex_files":len(files),
 "labels":len(set(labels)),
 "refs":len(refs),
 "citations":len(cites),
 "bibitems":len(set(bib)),
 "dependency_claims":len(ids),
 "dependency_edges":len(edges),
 "validation_graph_nodes":len(vids),
},indent=2,sort_keys=True))
