
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
docs = json.load(open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\docs_post_cleanup.json", encoding="utf-8"))
my_docs = [d for d in docs if str(d.get("pcfExternalSoftwareID1") or "").startswith("GROW-")]
# use pcfReference for lookup (we stored ref->ext earlier)
# Extract refs from ext: GROW-{ref} or GROW-{ref}-{n}
def ref_from_ext(e):
    e = e.replace("GROW-", "")
    parts = e.rsplit("-", 1)
    if len(parts) == 2 and parts[1].isdigit():
        return parts[0]
    return e

pairs = []
for d in my_docs:
    ref = ref_from_ext(d["pcfExternalSoftwareID1"])
    pairs.append({"id": d["_id"], "ext": d["pcfExternalSoftwareID1"], "ref": ref})

out = []
CH = 20
for i in range(0, len(pairs), CH):
    chunk = pairs[i:i+CH]
    refs = [c["ref"] for c in chunk]
    req = urllib.request.Request("https://api.fireberry.com/api/v3/query",
        data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"},{"name":"pcfSale"},{"name":"pcfPaymentCollection"}],
            "pageSize": 50, "pageNumber": 1,
            "filter": [{"type":"and","conditions":[
                {"fieldName":"pcfReference","operator":"eq-in","value":refs}]}]}).encode(), headers=HDRS)
    d = {"data": []}
    for attempt in range(4):
        try:
            r = urllib.request.urlopen(req, timeout=45)
            d = json.loads(r.read()); break
        except Exception as e:
            print(f"chunk {i} a{attempt}: {str(e)[:40]}", flush=True)
            time.sleep(5)
    for x in d.get("data", []):
        out.append({"ext": x.get("pcfExternalSoftwareID1"), "pcfSale": x.get("pcfSale"),
                    "sale_name": x.get("pcfSalename"), "pcfPaymentCollection": x.get("pcfPaymentCollection"),
                    "collection_name": x.get("pcfPaymentCollectionname"), "_id": x["_id"]})
    if (i//CH) % 20 == 0:
        print(f"{i+len(chunk)}/{len(pairs)} out={len(out)}", flush=True)
    time.sleep(0.8)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\my_docs_linkage_status.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)
print("saved", len(out), flush=True)
