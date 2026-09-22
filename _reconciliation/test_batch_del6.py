
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\cleanup_plan.json", encoding="utf-8"))
dd = plan["delete_my_dup_docs"][1:3]
ids = [d["doc_id"] for d in dd]
url = "https://api.fireberry.com/api/v3/record/1018/batch/delete"
req = urllib.request.Request(url, data=json.dumps({"data": ids}).encode(), headers=HDRS, method="DELETE")
try:
    r = urllib.request.urlopen(req, timeout=30)
    print("DELETE-method:", r.status, r.read()[:300])
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("DELETE-method:", e, body[:200])
