
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
rid = "467165A3-5FB1-4250-821C-5E49A4162C0A"
payed = round(347 / 1.18, 4)
req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}",
    data=json.dumps({"pcfPayed": payed}).encode(), headers=HDRS, method="PUT")
try:
    r = urllib.request.urlopen(req, timeout=30)
    raw = r.read().decode("utf-8", "ignore")
    print("status:", r.status)
    # find pcfPayed in raw
    import re
    m = re.search(r'"pcfPayedIncludingVAT":\s*([0-9.]+)', raw)
    m2 = re.search(r'"pcfPayed":\s*([0-9.]+)', raw)
    print("incl:", m.group(1) if m else None, "| payed:", m2.group(1) if m2 else None)
except Exception as e:
    body = getattr(e, "read", lambda: b"")()
    print("FAIL", e, body[:200])
