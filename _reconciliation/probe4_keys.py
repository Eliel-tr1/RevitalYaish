
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
    data=json.dumps({"objectType": 4, "fields": [{"name":"name"}], "pageSize": 1, "pageNumber": 1}).encode(), headers=HDRS)
r = urllib.request.urlopen(req, timeout=30)
d = json.loads(r.read())
print("all keys:", list(d.get("data", [{}])[0].keys()))
