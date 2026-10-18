"""רטרו 18/10/2026 (באישור סער): תוכנית המשך אונליין ⇒ מתקדמים. כתיבה דרך curl ישירות."""
import json, subprocess, time, sys

P = '/home/hermes/.hermes/profiles/revital-pm'
env = {}
for line in open(f'{P}/.env'):
    if '=' in line and not line.startswith('#'):
        k, v = line.split('=', 1); env[k.strip()] = v.strip()
B, K = env['REVITAL_FIREBERRY_BASE'], env['REVITAL_FIREBERRY_TOKEN']
ADV = '31CFC752-938B-4BE7-BCAD-2E36BAFFC733'
FIELDS = ['customobject1051id','name','pcfStatus','pcfCurrentProgram','pcfProduct','pcfActualGroup','pcfSale']


def curl(method, url, body=None):
    a = ['curl', '-s', '-m', '60', '-X', method, '-H', 'tokenid: ' + K, '-H', 'Content-Type: application/json']
    if body is not None:
        a += ['--data', json.dumps(body, ensure_ascii=False)]
    out = subprocess.run(a + [url], capture_output=True, text=True).stdout
    try:
        return json.loads(out)
    except Exception:
        return {'_raw': out[:200]}


def all_records():
    out = []
    for page in range(1, 15):
        r = curl('POST', B + '/api/v3/query', {"objectType": 1051, "fields": [{"name": f} for f in FIELDS],
                                               "pageSize": 500, "pageNumber": page})
        out += r.get('data') or []
        if r.get('isLastPage'):
            break
        time.sleep(1)
    return out


state = json.load(open(f'{P}/cache/mentor_change_20261018/retro_write_plan.json'))
ids = {x['customobject1051id'].upper() for x in state}
fresh = {x['customobject1051id'].upper(): x for x in all_records()}
print('read', len(fresh), 'records | candidates in plan:', len(ids))
to_prog = [x for x in state if fresh.get(x['customobject1051id'].upper(), {}).get('pcfCurrentProgram') == 4]
to_grp = [x for x in to_prog if x['pcfStatus'] in (1, 2) and not fresh.get(x['customobject1051id'].upper(), {}).get('pcfActualGroup')]
print('will set program=3:', len(to_prog), '| also fill group:', len(to_grp))
if '--write' not in sys.argv:
    json.dump({'program': [x['customobject1051id'] for x in to_prog], 'group': [x['customobject1051id'] for x in to_grp]},
              open(f'{P}/cache/mentor_change_20261018/retro_write_ids.json', 'w'), ensure_ascii=False, indent=1)
    print('dry run')
    sys.exit(0)


def batch(items, rec, label):
    ok = 0
    for i in range(0, len(items), 20):
        chunk = items[i:i+20]
        r = curl('POST', B + '/api/v3/record/1051/batch/update', {"data": [{"id": rid, "record": rec} for rid in chunk]})
        good = r.get('success') is True
        ok += len(chunk) if good else 0
        if not good:
            print(label, 'batch', i // 20 + 1, 'FAILED', json.dumps(r, ensure_ascii=False)[:200])
        time.sleep(1.5)
    print(label, 'updated', ok, 'of', len(items))
    return ok


n1 = batch([x['customobject1051id'] for x in to_prog], {'pcfCurrentProgram': 3}, 'program')
time.sleep(2)
n2 = batch([x['customobject1051id'] for x in to_grp], {'pcfActualGroup': ADV}, 'group')
time.sleep(3)

after = {x['customobject1051id'].upper(): x for x in all_records()}
bad_prog = [(x['name'], after.get(x['customobject1051id'].upper(), {}).get('pcfCurrentProgram')) for x in to_prog
            if after.get(x['customobject1051id'].upper(), {}).get('pcfCurrentProgram') != 3]
bad_grp = [x['name'] for x in to_grp if (after.get(x['customobject1051id'].upper(), {}).get('pcfActualGroup') or '').upper() != ADV]
print('\nprogram not updated:', len(bad_prog), bad_prog[:5])
print('group not updated:', len(bad_grp), bad_grp[:5])
open(f'{P}/cache/mentor_change_20261018/retro_after.json', 'w').write(json.dumps(list(after.values()), ensure_ascii=False))
