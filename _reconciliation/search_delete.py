
import re, pathlib
root = pathlib.Path(r"C:\Users\sahar\Claude Code\RevitalYaish")
pats = ["DELETE /api", "מחיקת רשומ", "delete record", "מחיקה דרך הAPI", "מחיקה דרך ה-API"]
seen = set()
for f in root.rglob("*.md"):
    try: t = f.read_text(encoding="utf-8", errors="ignore")
    except: continue
    for p in pats:
        for m in re.finditer(re.escape(p), t):
            s = max(0, m.start()-150); e = min(len(t), m.end()+250)
            snip = t[s:e].replace("\n", " | ")[:350]
            if snip[:80] in seen: continue
            seen.add(snip[:80])
            print(f"=== {f.name[:40]} [{p}] ===")
            print(snip)
            print()
