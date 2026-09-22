
import urllib.request, json, time
HDRS = {"tokenid": "b06663c4-62df-41b7-9111-6653e6b54592", "Content-Type": "application/json"}
URL = "https://api.fireberry.com/api/v3/query"

def fetch_all(ot, fields, name):
    all_rows, page = [], 1
    while True:
        req = urllib.request.Request(URL,
            data=json.dumps({"objectType": ot, "fields": [{"name": f} for f in fields],
                             "pageSize": 500, "pageNumber": page}).encode(), headers=HDRS)
        d = None
        for attempt in range(4):
            try:
                r = urllib.request.urlopen(req, timeout=60)
                d = json.loads(r.read()); break
            except Exception as e:
                print(f"  {name} p{page} a{attempt}: {str(e)[:40]}", flush=True)
                time.sleep(5)
        rows = d.get("data", [])
        all_rows.extend(rows)
        if d.get("isLastPage") or not rows: break
        page += 1
        time.sleep(0.8)
    print(f"{name}: {len(all_rows)} rows, {page} pages", flush=True)
    return all_rows

# Extract everything fresh
opps = fetch_all(4, ["name","statuscode","pcfProduct","pcfProductname","accountid","accountname","pcfclosedate","createdon"], "opps")
time.sleep(1)
pays = fetch_all(1039, ["name","pcfExternalSoftwareID1","pcfPaymentType","pcfNeedToPayIncludingVat","pcfAccountid","pcfNumberOfPayments","pcfFirstPaymentDate","createdon"], "pays")
time.sleep(1)
docs = fetch_all(1018, ["name","pcfExternalSoftwareID1","pcfPaymentDate","pcfPayedIncludingVAT","pcfAccountid","pcfSale","pcfPaymentCollection","pcfReference","createdon"], "docs")
time.sleep(1)
products = fetch_all(14, ["name","pcfItempriceIncludingVAT","pcfProductType","pcfDurationWeeks"], "products")

with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\FRESH_opps.json", "w", encoding="utf-8") as f:
    json.dump(opps, f, ensure_ascii=False)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\FRESH_pays.json", "w", encoding="utf-8") as f:
    json.dump(pays, f, ensure_ascii=False)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\FRESH_docs.json", "w", encoding="utf-8") as f:
    json.dump(docs, f, ensure_ascii=False)
with open(r"C:\Users\sahar\Claude Code\RevitalYaish\_reconciliation\FRESH_products.json", "w", encoding="utf-8") as f:
    json.dump(products, f, ensure_ascii=False)
print("ALL FRESH EXTRACTIONS COMPLETE", flush=True)
