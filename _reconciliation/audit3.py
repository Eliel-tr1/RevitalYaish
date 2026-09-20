
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
rid = "E22E00BC-A261-476C-8484-41FC153ACA4B"
req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}", headers=HDRS)
try:
    r = urllib.request.urlopen(req, timeout=30)
    rec = json.loads(r.read())
    data = rec.get("data", {}).get("Record", rec.get("data"))
    interesting = {k: v for k, v in data.items() if v not in (None, "", []) and ("pcf" in k.lower() or k in ("name",))}
    print(json.dumps(interesting, ensure_ascii=False, indent=1)[:2000])
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("GET FAIL", body[:150])
