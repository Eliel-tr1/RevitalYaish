
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
# Probe variations of batch endpoints on both object shapes
candidates = [
    "https://api.fireberry.com/api/batch/create",
    "https://api.fireberry.com/api/batch/update",
    "https://api.fireberry.com/api/batch/delete",
    "https://api.fireberry.com/api/batch/upsert",
    "https://api.fireberry.com/api/v1/batch/update",
    "https://api.fireberry.com/api/v2/batch/update",
]
for url in candidates:
    req = urllib.request.Request(url, data=json.dumps({"objectType": 1018, "records": []}).encode(), headers=HDRS, method="POST")
    try:
        r = urllib.request.urlopen(req, timeout=20)
        print(url, "->", r.status, r.read()[:150])
    except Exception as e:
        body = getattr(e, "read", lambda: b"")()
        print(url, "->", e, body[:100])
