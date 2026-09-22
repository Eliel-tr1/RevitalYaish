# -*- coding: utf-8 -*-
# Finish cleanup using batch API where Fireberry supports it (create/update),
# single DELETE for deletions (the only delete path; used by migration itself for rollback).
# Pacing: batch calls 1.5s apart, single DELETE 0.8s apart (migration's own deletion cadence).
import urllib.request, json, time, os, sys

HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
BASE = "https://api.fireberry.com"
BASEDIR = os.path.dirname(os.path.abspath(__file__))

plan = json.load(open(os.path.join(BASEDIR, "cleanup_plan.json"), encoding="utf-8"))
STATE_F = os.path.join(BASEDIR, "exec_state.json")
state = json.load(open(STATE_F, encoding="utf-8"))

def save():
    json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False)

def batch_update(ot, batch):
    url = f"{BASE}/api/v3/record/{ot}/batch/update"
    req = urllib.request.Request(url, data=json.dumps({"data": batch}).encode(), headers=HDRS, method="POST")
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    results = d.get("data", [])
    ok = sum(1 for x in results if x.get("success"))
    return ok, results

def single_delete(ot, rid):
    req = urllib.request.Request(f"{BASE}/api/record/{ot}/{rid}", headers=HDRS, method="DELETE")
    r = urllib.request.urlopen(req, timeout=45)
    return r.status

def with_retry(fn, label, tries=4, pause=8):
    for attempt in range(tries):
        try:
            return fn()
        except Exception as e:
            code = getattr(e, "code", None)
            if code == 429:
                print(f"  429 on {label}, waiting 20s", flush=True)
                time.sleep(20)
                continue
            body = getattr(e, "read", lambda: b"")()
            if attempt == tries - 1:
                state["errors"].append({"item": label, "err": str(e)[:100], "body": body.decode("utf-8","ignore")[:150]})
                save()
                return None
            time.sleep(pause)

PHASE = sys.argv[1] if len(sys.argv) > 1 else "all"

# ============ PHASE 1: remaining reparents via batch/update (20/call) ============
if PHASE in ("all", "reparent"):
    reps = [r for r in plan["reparent_docs"] if r["doc_id"] not in set(state["done_reparent"])]
    print(f"=== reparent remaining: {len(reps)} docs via batch/update ===", flush=True)
    CH = 20
    for i in range(0, len(reps), CH):
        chunk = reps[i:i+CH]
        batch = [{"id": r["doc_id"], "record": {"pcfPaymentCollection": r["target_1039"], "pcfSale": r["target_1039"]}} for r in chunk]
        res = with_retry(lambda b=batch: batch_update(1018, b), f"reparent-batch-{i}")
        if res:
            ok, results = res
            if ok == len(chunk):
                state["done_reparent"].extend(r["doc_id"] for r in chunk)
                state["done_reparent"] = list(set(state["done_reparent"]))
            else:
                # partial: mark only successful rows
                okids = {x["id"]["id"] if isinstance(x.get("id"), dict) else x["id"] for x in results if x.get("success")}
                state["done_reparent"].extend(okids)
                state["done_reparent"] = list(set(state["done_reparent"]))
                fails = [x for x in results if not x.get("success")]
                for f in fails:
                    state["errors"].append({"item": "batch-row", "err": f.get("message", "")[:100]})
            print(f"batch {i//CH}: ok={ok}/{len(chunk)} total={len(state['done_reparent'])}", flush=True)
        save()
        time.sleep(1.5)
    save()

# ============ PHASE 2: delete dup docs (single DELETE - no batch delete endpoint) ============
if PHASE in ("all", "docs"):
    dds = [d for d in plan["delete_my_dup_docs"] if d["doc_id"] not in set(state["done_delete_docs"])]
    print(f"=== delete dup docs remaining: {len(dds)} (single DELETE - Fireberry has no batch delete) ===", flush=True)
    for i, d in enumerate(dds):
        if d["doc_id"] in state["done_delete_docs"]: continue
        res = with_retry(lambda: single_delete(1018, d["doc_id"]), d["doc_ext"])
        if res:
            state["done_delete_docs"].append(d["doc_id"])
        if i % 50 == 0:
            print(f"docs {i}/{len(dds)} done={len(state['done_delete_docs'])} err={len(state['errors'])}", flush=True)
            save()
        time.sleep(0.8)
    save()

# ============ PHASE 3: delete redundant SOs (single DELETE) ============
if PHASE in ("all", "sos"):
    sos = [s for s in plan["delete_sos"] if s["so_id"] not in set(state["done_delete_sos"])]
    print(f"=== delete redundant SOs remaining: {len(sos)} ===", flush=True)
    for i, s in enumerate(sos):
        if s["so_id"] in state["done_delete_sos"]: continue
        res = with_retry(lambda: single_delete(1039, s["so_id"]), s.get("so_ext") or s["so_name"])
        if res:
            state["done_delete_sos"].append(s["so_id"])
        if i % 50 == 0:
            print(f"sos {i}/{len(sos)} done={len(state['done_delete_sos'])} err={len(state['errors'])}", flush=True)
            save()
        time.sleep(0.8)
    save()

print(f"EXEC DONE: sos={len(state['done_delete_sos'])}/393 docs={len(state['done_delete_docs'])}/541 reparent={len(state['done_reparent'])}/1029 errors={len(state['errors'])}", flush=True)
