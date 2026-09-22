
import urllib.request, json, time, random
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\cleanup_plan.json", encoding="utf-8"))
random.seed(99)

# 1. Verify deleted SOs are gone (sample 15 of 393)
sos_sample = random.sample(plan["delete_sos"], 15)
still_there = 0
for s in sos_sample:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1039, "fields": [{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 2, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value": s["so_ext"]}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    n = len(json.loads(r.read()).get("data", []))
    if n > 0:
        still_there += 1
        print("STILL EXISTS:", s["so_ext"])
    time.sleep(0.5)
print(f"deleted SOs verified: {15-still_there}/15 gone")

# 2. Verify deleted docs are gone (sample 15 of 541)
dds = random.sample(plan["delete_my_dup_docs"], 15)
still = 0
for d in dds:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"}],
            "pageSize": 2, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value": d["doc_ext"]}]}]}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=30)
    n = len(json.loads(r.read()).get("data", []))
    if n > 0:
        still += 1
        print("STILL EXISTS:", d["doc_ext"])
    time.sleep(0.5)
print(f"deleted docs verified: {15-still}/15 gone")

# 3. Verify reparented docs point to correct 1039 (sample 15 of 1029)
reps = random.sample(plan["reparent_docs"], 15)
correct = 0
for r in reps:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfPaymentCollection"}],
            "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value": r["doc_ext"]}]}]}).encode(), headers=HDRS)
    rr = urllib.request.urlopen(req, timeout=30)
    rows = json.loads(rr.read()).get("data", [])
    if rows:
        parent = str(rows[0].get("pcfPaymentCollection") or "").upper()
        if parent == r["target_1039"].upper():
            correct += 1
        else:
            print("WRONG PARENT:", r["doc_ext"], "got", parent[:8], "want", r["target_1039"][:8])
    time.sleep(0.5)
print(f"reparented verified: {correct}/15 correct parent")
