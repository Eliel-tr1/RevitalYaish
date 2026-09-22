
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
guid = "D0B72253-04EF-4CB2-9DE4-B5D9EC111118"
url = f"https://api.fireberry.com/api/record/4/{guid}"
req = urllib.request.Request(url, headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=30)
    d = json.loads(r.read())
    rec = d.get("data", {}).get("Record", d.get("data"))
    print("GET OK:", rec.get("name") if rec else "?")
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("GET FAIL:", e, body[:300])
