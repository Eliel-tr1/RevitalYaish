
import urllib.request, json, traceback
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
try:
    rows = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\doc_linkage_final.json", encoding="utf-8"))
    state = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\exec_state.json", encoding="utf-8"))
    done = set(state["done_reparent"])
    r0 = next(r for r in rows if r["doc_id"] in done)
    print("test doc:", r0["doc_id"], "target:", r0["target_1039"])
    url = "https://api.fireberry.com/api/v3/record/1018/batch/update"
    body = {"data": [{"id": r0["doc_id"], "record": {"pcfPaymentCollection": r0["target_1039"]}}]}
    print("URL:", url)
    req = urllib.request.Request(url, data=json.dumps(body).encode(), headers=HDRS, method="POST")
    r = urllib.request.urlopen(req, timeout=45)
    raw = r.read().decode("utf-8", "ignore")
    print("STATUS", r.status)
    print("RESPONSE:", raw[:800])
except Exception:
    traceback.print_exc()
