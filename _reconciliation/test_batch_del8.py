
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
url = "https://api.fireberry.com/api/v3/record/1018/batch/delete"
plan = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\cleanup_plan.json", encoding="utf-8"))
d = plan["delete_my_dup_docs"][3]
variants = [
    {"data": [{"Id": d["doc_id"]}]},
    {"data": [{"recordid": d["doc_id"]}]},
    {"data": [{"id": d["doc_id"], "entityName": "customobject1018"}]},
]
for v in variants:
    req = urllib.request.Request(url, data=json.dumps(v).encode(), headers=HDRS, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=30)
        raw = r.read().decode("utf-8","ignore")
        print("variant:", json.dumps(v)[:70], "->", r.status, raw[:250])
        if '"success":true' in raw and '"success":false' not in raw.split('"data"')[1][:300]:
            print("  LOOKS CLEAN"); break
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print("variant:", json.dumps(v)[:70], "->", e, body[:100])
    import time; time.sleep(1)
