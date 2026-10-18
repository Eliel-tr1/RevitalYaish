const fs = require('fs');
const path = require('path');
const H = require('../mentor_change_20261007/harness.js');
const dir = __dirname;
const load = (f, when) => fs.readFileSync(`${dir}/${f}_planner_${when}.js`, 'utf8');
const old25 = load('WF-25', 'before'), new25 = load('WF-25', 'after');
const ex = (n) => `../research_pro/execs2/${n}`;
const body = (p) => (p.ops.find(o => o.object === '1051') || { body: {} }).body;
const PERSONAL = 'D2CE0670-275A-4EF9-96BA-167F5CA053D6', ONLINE = '58A4D4F9-5921-4BFC-BA8E-518877FAA375';
const ADV_GROUP = '31CFC752-938B-4BE7-BCAD-2E36BAFFC733', ADV_OWNER = 'FB20B673-5745-41E8-8166-BDE6BE24A4B3';
let fails = 0;
const check = (l, c, x) => { if (!c) fails++; console.log((c ? 'PASS ' : 'FAIL ') + l + (x ? ' | ' + x : '')); };

console.log('--- real executions (all online) ---');
for (const f of fs.readdirSync(path.join(dir, '../research_pro/execs2')).filter(f => f.startsWith('WF-25_'))) {
  const inp = H.loadExec(path.join(dir, ex(f)));
  const a = H.run(old25, JSON.parse(JSON.stringify(inp)));
  const b = H.run(new25, JSON.parse(JSON.stringify(inp)));
  const same = (k) => JSON.stringify(body(a)[k]) === JSON.stringify(body(b)[k]);
  console.log(f, '|', inp['קליטה וסיווג'].accountName, '| product', inp['קליטה וסיווג'].productId.slice(0, 8));
  check('  program now 3 (מתקדמים)', body(b).pcfCurrentProgram === 3, 'old=' + body(a).pcfCurrentProgram + ' new=' + body(b).pcfCurrentProgram);
  check('  group = advanced', body(b).pcfActualGroup === ADV_GROUP);
  check('  owner = advanced group manager', body(b).ownerid === ADV_OWNER);
  check('  dates unchanged', same('pcfStartDate') && same('pcfEstimatedEndDate') && same('pcfPremiumEndDate'));
  check('  status/name/product/week unchanged', same('pcfStatus') && same('name') && same('pcfProduct') && same('pcfCurrentWeek'));
  check('  no welcome / no wa join', JSON.stringify(b.cc) === JSON.stringify(a.cc) && JSON.stringify(b.wa) === JSON.stringify(a.wa));
  check('  sale + note-only changes', JSON.stringify(a.ops.filter(o => o.object !== '1051' && o.object !== 'note')) === JSON.stringify(b.ops.filter(o => o.object !== '1051' && o.object !== 'note')));
}

console.log('\n--- synthetic: personal continuation (program must stay 4) ---');
{
  const inp = H.loadExec(path.join(dir, ex('WF-25_369664.json')));
  inp['קליטה וסיווג'].productId = PERSONAL;
  const pr = inp['המוצר (14)'].data;
  const a = H.run(old25, JSON.parse(JSON.stringify(inp)));
  const b = H.run(new25, JSON.parse(JSON.stringify(inp)));
  check('personal: program still 4', body(b).pcfCurrentProgram === 4, String(body(b).pcfCurrentProgram));
  check('personal: identical to old behaviour (existing record)', JSON.stringify(H.slim(a)) === JSON.stringify(H.slim(b)));
}
console.log('\n--- synthetic: online with no advanced group ---');
{
  const inp = H.loadExec(path.join(dir, ex('WF-25_369664.json')));
  inp['קבוצות WhatsApp (1068)'].data = inp['קבוצות WhatsApp (1068)'].data.filter(r => !String(r.customobject1068id).toUpperCase().startsWith('31CFC752'));
  const b = H.run(new25, JSON.parse(JSON.stringify(inp)));
  check('no group: program still 3', body(b).pcfCurrentProgram === 3);
  check('no group: no group/owner written', !('pcfActualGroup' in body(b)) && !('ownerid' in body(b)));
  check('no group: warning raised', (b.warnings || []).some(w => w.includes('קבוצת המתקדמות')));
}
console.log(fails ? `\n${fails} FAILED` : '\nALL PASSED');
process.exit(fails ? 1 : 0);
