
import urllib.request, json
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
rid = "467165A3-5FB1-4250-821C-5E49A4162C0A"  # GROW-457562960, amount 347
payed = round(347 / 1.18, 4)
req = urllib.request.Request(f"https://api.fireberry.com/api/record/1018/{rid}",
    data=json.dumps({"pcfPayed": payed}).encode(), headers=HDRS, method="PUT")
r = urllib.request.urlopen(req, timeout=30)
rec = json.loads(r.read())
d = rec.get("data", {}).get("Record", rec.get("data"))
print("PUT pcfPayed =", payed, "-> response:", d.get("pcfPayed"), "| incl:", d.get("pcfPayedIncludingVAT"))
