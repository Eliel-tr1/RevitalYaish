
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# Try deleting a TEST doc we control? We don't have spare. Use one of MY duplicate docs (approved for deletion):
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\cleanup_plan.json", encoding="utf-8"))
d0 = plan["delete_my_dup_docs"][0]
url = "https://api.fireberry.com/api/v3/record/1018/batch/delete"
for payload in [{"data": [{"id": d0["doc_id"]}]}, {"data": [d0["doc_id"]]}]:
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers=HDRS, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print("payload variant OK:", json.dumps(payload)[:60], "->", r.status, r.read()[:200])
        break
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print("variant failed:", json.dumps(payload)[:60], "->", e, body[:120])
