
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\cleanup_plan.json", encoding="utf-8"))
dd = plan["delete_my_dup_docs"][1:3]
ids = [d["doc_id"] for d in dd]
# variant: {"id": ..., "record": null}
url = "https://api.fireberry.com/api/v3/record/1018/batch/delete"
for payload in [{"data": [{"id": i, "record": {}} for i in ids]},
                {"data": [{"id": i, "objectType": 1018} for i in ids]}]:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=HDRS, method="POST")
    r = urllib.request.urlopen(req, timeout=30)
    raw = r.read().decode("utf-8", "ignore")
    print("variant:", json.dumps(payload)[:60], "->", raw[:300])
    time.sleep(1)
    # verify
    any_deleted = True
    for x in dd:
        q = urllib.request.Request("https://api.fireberry.com/api/v3/query",
            data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"}], "pageSize": 1, "pageNumber": 1,
                "filter": [{"type":"and","conditions":[{"fieldName":"pcfExternalSoftwareID1","operator":"eq","value": x["doc_ext"]}]}]}).encode(), headers=HDRS)
        rr = urllib.request.urlopen(q, timeout=30)
        n = len(json.loads(rr.read()).get("data", []))
        if n > 0: any_deleted = False
    print("  actually deleted:", any_deleted)
    if any_deleted: break
