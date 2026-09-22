
import urllib.request, json, time, os, sys
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
BASE = "https://api.fireberry.com"
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\FULL_plan.json", encoding="utf-8"))
STATE_F = r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\exec_final_state.json"
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

def with_retry(fn, label, tries=4):
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
                state["errors"].append({"item": label, "err": str(e)[:100]})
                save()
                return None
            time.sleep(5)

# ===== PHASE 1: Sahar's directives =====
print("=== PHASE 1: Sahar directives ===", flush=True)
for d in plan["sahar_directives"]:
    ext = d["ext"]
    if ext in state["sahar_done"]: continue
    
    if d["action"] == "delete_doc_and_payment":
        # Delete doc first, then payment
        if d.get("doc_id"):
            res = with_retry(lambda: single_delete(1018, d["doc_id"]), f"del-doc-{ext}")
            print(f"  {ext} doc delete: {res}", flush=True)
        if d.get("parent_1039"):
            res = with_retry(lambda: single_delete(1039, d["parent_1039"]), f"del-pay-{ext}")
            print(f"  {ext} payment delete: {res}", flush=True)
        state["sahar_done"].append(ext)
        state["deleted_docs"].append(d["doc_id"])
        state["deleted_sos"].append(d["parent_1039"])
    
    elif d["action"] == "delete_doc":
        if d.get("doc_id"):
            res = with_retry(lambda: single_delete(1018, d["doc_id"]), f"del-doc-{ext}")
            print(f"  {ext} doc delete: {res}", flush=True)
        state["sahar_done"].append(ext)
        state["deleted_docs"].append(d["doc_id"])
    
    elif d["action"] == "reparent_and_delete_old_parent":
        # Step 1: batch update doc to new parent + sale
        target = d["target_1039"]
        # Find the sale process of the target payment
        req = urllib.request.Request(f"{BASE}/api/v3/query",
            data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfSale"}],
                "pageSize": 1, "pageNumber": 1,
                "filter": [{"type":"and","conditions":[
                    {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":""}]}]}).encode(), headers=HDRS)
        # Instead, get the target payment's sale from our data
        target_sale = None
        for r in plan["reparent_to_existing"]:
            if r["target_1039"] == target and r.get("target_sale"):
                target_sale = r["target_sale"]; break
        # If not found, query the payment's pcfSale directly
        if not target_sale:
            req = urllib.request.Request(f"{BASE}/api/v3/query",
                data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfSale"}],
                    "pageSize": 1, "pageNumber": 1,
                    "filter": [{"type":"and","conditions":[
                        {"fieldName":"customobject1039id","operator":"eq","value":target}]}]}).encode(), headers=HDRS)
            try:
                rr = urllib.request.urlopen(req, timeout=30)
                dd = json.loads(rr.read())
                if dd.get("data"): target_sale = dd["data"][0].get("pcfSale")
            except: pass
        
        update_body = {"pcfPaymentCollection": target}
        if target_sale: update_body["pcfSale"] = target_sale
        
        ok, results = with_retry(lambda: batch_update(1018, [{"id": d["doc_id"], "record": update_body}]), f"reparent-{ext}")
        print(f"  {ext} reparent: ok={ok}", flush=True)
        
        # Step 2: delete old parent payment
        if d.get("parent_1039"):
            res = with_retry(lambda: single_delete(1039, d["parent_1039"]), f"del-old-{ext}")
            print(f"  {ext} old parent delete: {res}", flush=True)
            state["deleted_sos"].append(d["parent_1039"])
        
        state["sahar_done"].append(ext)
    save()
    time.sleep(1)

# ===== PHASE 2: Reparent 128 docs via batch/update =====
print("=== PHASE 2: Reparent docs ===", flush=True)
reps = [r for r in plan["reparent_to_existing"] if r["doc_id"] not in state["reparent_done"]]
print(f"remaining: {len(reps)}", flush=True)
CH = 20
for i in range(0, len(reps), CH):
    chunk = reps[i:i+CH]
    batch = []
    for r in chunk:
        update = {"pcfPaymentCollection": r["target_1039"]}
        if r.get("target_sale"):
            update["pcfSale"] = r["target_sale"]
        batch.append({"id": r["doc_id"], "record": update})
    
    ok, results = with_retry(lambda b=batch: batch_update(1018, b), f"reparent-batch-{i}")
    if ok == len(chunk):
        state["reparent_done"].extend(r["doc_id"] for r in chunk)
        state["reparent_done"] = list(set(state["reparent_done"]))
        print(f"batch {i//CH}: {ok}/{len(chunk)} total={len(state['reparent_done'])}", flush=True)
    else:
        # Mark successful ones
        okids = set()
        for x in results:
            rid = x["id"]["id"] if isinstance(x.get("id"), dict) else x.get("id", "")
            if x.get("success"): okids.add(rid)
        state["reparent_done"].extend(okids)
        state["reparent_done"] = list(set(state["reparent_done"]))
        fails = [x for x in results if not x.get("success")]
        for f in fails:
            state["errors"].append({"item": "batch-row", "err": f.get("message", "")[:100]})
        print(f"batch {i//CH}: {ok}/{len(chunk)} PARTIAL total={len(state['reparent_done'])}", flush=True)
    save()
    time.sleep(1.5)

print(f"EXEC DONE: sahar={len(state['sahar_done'])} reparent={len(state['reparent_done'])} errors={len(state['errors'])}", flush=True)
