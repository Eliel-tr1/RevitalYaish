
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"

def count_all(ot):
    all_rows, page = [], 1
    while True:
        req = urllib.request.Request(URL,
            data=json.dumps({"objectType": ot, "fields": [{"name":"pcfExternalSoftwareID1"},{"name":"pcfAccountid"}],
                             "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
        d = None
        for attempt in range(4):
            try:
                r = urllib.request.urlopen(req, timeout=60)
                d = json.loads(r.read()); break
            except Exception as e:
                print(f"p{page} a{attempt}: {str(e)[:40]}", flush=True)
                time.sleep(5)
        rows = d.get("data", [])
        all_rows.extend(rows)
        if d.get("isLastPage") or not rows: break
        page += 1
        time.sleep(1.0)
    return all_rows

docs = count_all(1018)
print("total 1018 now:", len(docs), flush=True)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\docs_post_cleanup.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False)
import re
pat = re.compile(r"^[0-9A-Fa-f-]{36}#\d+$")
exts = [str(d.get("pcfExternalSoftwareID1") or "") for d in docs]
my_reco_docs = sum(1 for e in exts if e.startswith("GROW-"))
mig_docs = sum(1 for e in exts if pat.match(e))
print(f"  live/my GROW docs: {my_reco_docs}")
print(f"  migration schedule docs: {mig_docs}")
