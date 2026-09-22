
# -*- coding: utf-8 -*-
import urllib.request, json, time, os, sys

HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
BASE = "https://api.fireberry.com"
BASEDIR = os.path.dirname(os.path.abspath(__file__))

def load(fn):
    return json.load(open(os.path.join(BASEDIR, fn), encoding="utf-8"))

def del_req(ot, rid):
    req = urllib.request.Request(f"{BASE}/api/record/{ot}/{rid}", headers=HDRS, method="DELETE")
    r = urllib.request.urlopen(req, timeout=45)
    return r.status

def put_req(ot, rid, body):
    req = urllib.request.Request(f"{BASE}/api/record/{ot}/{rid}",
        data=json.dumps(body).encode(), headers=HDRS, method="PUT")
    r = urllib.request.urlopen(req, timeout=45)
    return r.status

PHASE = sys.argv[1] if len(sys.argv) > 1 else "all"
plan = load("cleanup_plan.json")
STATE_F = os.path.join(BASEDIR, "exec_state.json")
state = {"done_delete_sos": [], "done_delete_docs": [], "done_reparent": [], "errors": []}
if os.path.exists(STATE_F):
    state = json.load(open(STATE_F, encoding="utf-8"))

def save():
    json.dump(state, open(STATE_F, "w", encoding="utf-8"), ensure_ascii=False)

def with_retry(fn, label, tries=4):
    for attempt in range(tries):
        try:
            return fn()
        except Exception as e:
            code = getattr(e, "code", None)
            if code == 429:
                time.sleep(15)
                continue
            body = getattr(e, "read", lambda: b"")()
            if attempt == tries - 1:
                state["errors"].append({"item": label, "err": str(e)[:100], "body": body.decode("utf-8","ignore")[:150]})
                save()
                return None
            time.sleep(5)

if PHASE in ("all", "reparent"):
    print("=== PHASE: reparent docs (1029) ===", flush=True)
    reps = plan["reparent_docs"]
    for i, r in enumerate(reps):
        if r["doc_id"] in state["done_reparent"]: continue
        res = with_retry(lambda: put_req(1018, r["doc_id"],
            {"pcfPaymentCollection": r["target_1039"], "pcfSale": r["target_1039"]}), r["doc_ext"])
        if res:
            state["done_reparent"].append(r["doc_id"])
            state["done_reparent"] = list(set(state["done_reparent"]))
        if i % 25 == 0:
            print(f"reparent {i}/{len(reps)} done={len(state['done_reparent'])} err={len(state['errors'])}", flush=True)
            save()
        time.sleep(1.2)
    save()

if PHASE in ("all", "docs"):
    print("=== PHASE: delete dup docs (541) ===", flush=True)
    dds = plan["delete_my_dup_docs"]
    for i, d in enumerate(dds):
        if d["doc_id"] in state["done_delete_docs"]: continue
        res = with_retry(lambda: del_req(1018, d["doc_id"]), d["doc_ext"])
        if res:
            state["done_delete_docs"].append(d["doc_id"])
        if i % 25 == 0:
            print(f"docs {i}/{len(dds)} done={len(state['done_delete_docs'])} err={len(state['errors'])}", flush=True)
            save()
        time.sleep(1.2)
    save()

if PHASE in ("all", "sos"):
    print("=== PHASE: delete redundant SOs (393) ===", flush=True)
    sos = plan["delete_sos"]
    for i, s in enumerate(sos):
        if s["so_id"] in state["done_delete_sos"]: continue
        res = with_retry(lambda: del_req(1039, s["so_id"]), s["so_ext"])
        if res:
            state["done_delete_sos"].append(s["so_id"])
        if i % 25 == 0:
            print(f"sos {i}/{len(sos)} done={len(state['done_delete_sos'])} err={len(state['errors'])}", flush=True)
            save()
        time.sleep(1.2)
    save()

print(f"EXEC DONE: sos={len(state['done_delete_sos'])} docs={len(state['done_delete_docs'])} reparent={len(state['done_reparent'])} errors={len(state['errors'])}", flush=True)
