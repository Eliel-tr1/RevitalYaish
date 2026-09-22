
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# Query with a known opp _id from opps_all.json to verify format works
opps = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\opps_all.json", encoding="utf-8"))
# check if d0b72253 is in our extraction
target = "d0b72253-04ef-4cb2-9de4-b5d9ec111118"
found = [o for o in opps if o["_id"].lower() == target]
print("in our extract:", len(found))
if found:
    print(json.dumps(found[0], ensure_ascii=False))
# also try direct lookup
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 4, "fields": [{"name":"name"}], "pageSize": 1, "pageNumber": 1,
        "filter": [{"type":"and","conditions":[
            {"fieldName":"_id","operator":"eq","value":target}]}]}).encode(), headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    print("API lookup:", len(d.get("data", [])))
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("API FAIL:", e, body[:200])
