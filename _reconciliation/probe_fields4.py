
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
def probe(f):
    body = {"objectType": 4, "fields": [{"name": f}], "pageSize": 1, "pageNumber": 1}
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query", data=json.dumps(body).encode(), headers=HDRS)
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return f + ": OK"
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        return f + ": FAIL " + body[:80].decode("utf-8", "ignore")
for f in ["name","statuscode","pcfProduct","pcfAccountid","pcfclosedate","createdon","pcfincomingcashflow","pcfPrimaryContact"]:
    print(probe(f))
