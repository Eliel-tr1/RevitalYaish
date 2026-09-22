
import re, pathlib
root = pathlib.Path(r"C:\Users\sahar\Claude Code\RevitalYaish")
patterns = ["batch/create", "batch/update", "batch/delete", "batchrequest", "BatchRequest", "batch_api", "api/batch"]
seen = set()
for f in root.rglob("*.md"):
    try: t = f.read_text(encoding="utf-8", errors="ignore")
    except: continue
    for p in patterns:
        for m in re.finditer(re.escape(p), t):
            s = max(0, m.start()-200); e = min(len(t), m.end()+300)
            snip = t[s:e]
            key = snip[:100]
            if key in seen: continue
            seen.add(key)
            print(f"=== {f.name} [{p}] ===")
            print(snip.replace("\n", " | ")[:450])
            print()
