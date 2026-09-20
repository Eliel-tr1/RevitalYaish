
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def qname(val, label):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1,
            "fields": [{"name":"accountname"},{"name":"telephone1"}],
            "pageSize": 10, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"accountname","operator":"contains","value":val}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        d = json.loads(r.read())
        rows = d.get("data", [])
        print(label, "->", len(rows))
        for x in rows[:5]: print("   ", json.dumps(x, ensure_ascii=False))
        return rows
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(label, "FAIL", body[:120]); return []

qname("יעקב לבי", "exact name")
qname("לבי", "surname")
qname("יעקב", "first name")
