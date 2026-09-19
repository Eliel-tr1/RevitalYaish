
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"

def count_pages(ot, cond_prefix, label):
    all_rows, page = [], 1
    while True:
        req = urllib.request.Request(URL,
            data=json.dumps({"objectType": ot,
                "fields": [{"name":"pcfExternalSoftwareID1"}],
                "pageSize": 500, "pageNumber": page,
                "filter": [{"type":"or","conditions":[
                    {"fieldName":"pcfExternalSoftwareID1","operator":"eq-in","value":[cond_prefix + "-0", cond_prefix + "-1"]},
                    {"fieldName":"pcfExternalSoftwareID1","operator":"eq","value":cond_prefix}]}]}).encode(), headers=HDRS)
        # Simplified: just count via pagination without filter is too heavy (14k docs).
        # Instead: count via known list? We verify by sampling below.
        break
    return 0

# Better: fetch ALL 1018 ext ids again (fast, 29 pages) and count reco docs
all_rows, page = [], 1
while True:
    req = urllib.request.Request(URL,
        data=json.dumps({"objectType": 1018, "fields": [{"name":"pcfExternalSoftwareID1"}],
                         "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
    for attempt in range(3):
        try:
            r = urllib.request.urlopen(req, timeout=60)
            d = json.loads(r.read()); break
        except Exception:
            if attempt == 2: raise
            time.sleep(3)
    rows = d.get("data", [])
    all_rows.extend(rows)
    if d.get("isLastPage") or not rows: break
    page += 1
    time.sleep(0.7)

reco_docs = [x for x in all_rows if str(x.get("pcfExternalSoftwareID1") or "").startswith("GROW-") and "DD-RECO" not in str(x.get("pcfExternalSoftwareID1"))]
# all GROW-* docs include live WF-20 ones too
grow_docs = [x for x in all_rows if str(x.get("pcfExternalSoftwareID1") or "").startswith("GROW-")]
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\docs_extids_after.json", "w", encoding="utf-8") as f:
    json.dump(all_rows, f, ensure_ascii=False)
print("total 1018 docs now:", len(all_rows))
print("GROW-* docs total:", len(grow_docs))
print("saved")
