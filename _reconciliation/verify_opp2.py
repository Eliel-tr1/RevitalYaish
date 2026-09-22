
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
guid = "d0b72253-04ef-4cb2-9de4-b5d9ec111118"
# Try to find it by customobject4id
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 4, "fields": [{"name":"name"},{"name":"statuscode"},{"name":"accountid"}],
        "pageSize": 1, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"customobject4id","operator":"eq","value":guid}]}]}).encode(), headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    print("found:", len(d.get("data", [])))
    if d.get("data"):
        print(json.dumps(d["data"][0], ensure_ascii=False))
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("FAIL:", e, body[:200])
