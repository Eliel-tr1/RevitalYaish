
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\cleanup_plan.json", encoding="utf-8"))
dd = plan["delete_my_dup_docs"][1:3]
ids = [d["doc_id"] for d in dd]
url = "https://api.fireberry.com/api/v3/record/1018/batch/delete"
req = urllib.request.Request(url, data=json.dumps({"data": [{"id": i} for i in ids]}).encode(), headers=HDRS, method="POST")
r = urllib.request.urlopen(req, timeout=30)
raw = r.read().decode("utf-8", "ignore")
print("STATUS", r.status)
print(raw[:500])
# verify actually deleted
time.sleep(2)
import urllib.request as U
ok = 0
for i in ids:
    q = U.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"}], "pageSize": 1, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[{"fieldName":"pcfExternalSoftwareID1","operator":"eq","value": next(x["doc_ext"] for x in dd if x["doc_id"]==i)}]}]}).encode(), headers=HDRS)
    rr = U.urlopen(q, timeout=30)
    n = len(json.loads(rr.read()).get("data", []))
    print(i[:8], "exists:", n)
