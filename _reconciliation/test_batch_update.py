
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# find one already-reparented doc to test idempotent update
rows = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\doc_linkage_final.json", encoding="utf-8"))
state = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\exec_state.json", encoding="utf-8"))
done = set(state["done_reparent"])
r0 = next(r for r in rows if r["doc_id"] in done)
url = "https://api.fireberry.com/api/v3/record/1018/batch/update"
body = {"data": [{"id": r0["doc_id"], "record": {"pcfPaymentCollection": r0["target_1039"]}}]}
req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="POST")
try:
    r = urllib.request.urlopen(req, timeout=45)
    print("STATUS", r.status)
    print(json.dumps(json.loads(r.read()), ensure_ascii=False)[:600])
except Exception as e:
    body2 = getattr(e, "read", lambda: b"")()
    print("FAIL", e, body2[:300])
