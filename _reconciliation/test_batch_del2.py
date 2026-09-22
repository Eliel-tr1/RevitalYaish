
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
url = "https://api.fireberry.com/api/v3/record/1018/batch/delete"
req = urllib.request.Request(url, data=json.dumps({"data": []}).encode(), headers=HDRS, method="POST")
try:
    r = urllib.request.urlopen(req, timeout=30)
    print("batch/delete ->", r.status, r.read()[:300])
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("batch/delete ->", e, body[:200])
