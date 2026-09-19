
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def try_op(op):
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1,
            "fields": [{"name":"telephone1"}],
            "pageSize": 10, "pageNumber": 1,
            "filter": [{"type":"or","conditions":[
                {"fieldName":"telephone1","operator":op,"value":["0528928479","0543110840"]}]}]}).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=60)
        d = json.loads(r.read())
        return f"OK {len(d.get('data', []))}"
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        return f"FAIL {body[:80]}"
for op in ["eq-in", "inlist", "list", "oneof"]:
    print(op, try_op(op))
# Also try legacy query API
req = urllib.request.Request("https://api.fireberry.com/api/query",
    data=json.dumps({"query": "(telephone1 = 0528928479)", "fields": "telephone1,_id", "page_size": 10, "objecttype": "1", "page_number": 1}).encode(), headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=60)
    d = json.loads(r.read())
    print("legacy eq:", len(d.get("Data") or []))
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("legacy FAIL", body[:150])
