
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
for url in ["https://api.fireberry.com/api/batch/update", "https://api.fireberry.com/api/v3/batch/update"]:
    req = urllib.request.Request(url, data=json.dumps({"records": []}).encode(), headers=HDRS, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=30)
        print(url, "->", r.status, r.read()[:200])
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(url, "->", e, body[:120])
