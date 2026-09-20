
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def q(op, val, label):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1,
            "fields": [{"name":"accountname"},{"name":"telephone1"}],
            "pageSize": 10, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"accountname","operator":op,"value":val}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read())
        rows = d.get("data", [])
        print(label, "->", len(rows))
        for x in rows[:6]: print("   ", json.dumps(x, ensure_ascii=False)[:120])
        return rows
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(label, "FAIL", body[:100]); return []

q("like", "יעקב לבי", "like")
q("eq", "יעקב לבי", "eq exact")
# fallback: fetch accounts pages and grep name locally (accounts ~725, cheap)
all_rows, page = [], 1
while True:
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1, "fields": [{"name":"accountname"},{"name":"telephone1"}],
                         "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    rows = d.get("data", [])
    all_rows.extend(rows)
    if d.get("isLastPage") or not rows: break
    page += 1
import json as J
print("total accounts:", len(all_rows))
matches = [x for x in all_rows if "לבי" in (x.get("accountname") or "")]
print("לבי matches:")
for x in matches: print("   ", json.dumps(x, ensure_ascii=False))
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\all_accounts.json", "w", encoding="utf-8") as f:
    J.dump(all_rows, f, ensure_ascii=False)
