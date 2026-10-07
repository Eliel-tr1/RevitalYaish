const fs = require('fs');
const { run, loadExec, slim } = require('./harness.js');
const dir = __dirname;
const U = (s) => String(s).toUpperCase();
const ODED = '6C59CE04-55BB-4186-92B7-AA0EA8ADCF28', REVITAL = '0FA826FA-CBC8-4BA5-9CD4-3E59F129F4DE';
const ADV_GROUP = '31CFC752-938B-4BE7-BCAD-2E36BAFFC733', ADV_OWNER = 'FB20B673-5745-41E8-8166-BDE6BE24A4B3';
const PREM_GROUP = 'BD6856EC-2248-480F-9CD1-41CA7CAE26AC', PREM_OWNER = '3F38DCD5-EF74-4706-9933-347EF966292D';
const BOOST_PID = '2F73403A-20DE-47A7-B0CB-DF4761B45F21', PERSONAL = 'D2CE0670-275A-4EF9-96BA-167F5CA053D6', ONLINE = '58A4D4F9-5921-4BFC-BA8E-518877FAA375';
const PREM_PID = 'D9E842A7-F284-4596-BB61-4D2A350EEB5D'; // 12 שבועות

const clone = (o) => JSON.parse(JSON.stringify(o));
const ex = (n) => `${dir}/../research_pro/execs/${n}`;
const code = (wf, when) => fs.readFileSync(`${dir}/${wf}_planner_${when}.js`, 'utf8');
let fails = 0;
const check = (label, cond, extra) => { if (!cond) fails++; console.log((cond ? 'PASS ' : 'FAIL ') + label + (extra ? ' | ' + extra : '')); };
const m1051 = (p) => (p.ops.find(o => o.object === '1051') || { body: {} });
const body = (p) => m1051(p).body;

function base25() { return loadExec(ex('WF25_305936.json')); }
function base23() { return loadExec(ex('WF23_314492.json')); }
function setGroups(inp) { // ensure the groups list has ownerid for advanced & premium groups
  const rows = inp['קבוצות WhatsApp (1068)'].data;
  const g = (id) => rows.find(r => U(r.customobject1068id) === U(id));
  return { adv: g(ADV_GROUP), prem: g(PREM_GROUP), rows };
}

// ---- WF-23: boost ----
{
  let inp = base23(); const gr = setGroups(inp);
  const prod = inp['המוצר (14)'].data.find(p => U(p.productid) === U(BOOST_PID));
  console.log('boost product owner in snapshot', prod.ownerid, '| adv group owner in snapshot', gr.adv && gr.adv.ownerid);
  prod.ownerid = ODED;
  const a = run(code('WF-23', 'before'), clone(inp)), b = run(code('WF-23', 'after'), clone(inp));
  check('WF-23 boost: new owner = product manager (ODED)', body(b).ownerid === ODED, body(b).ownerid);
  check('WF-23 boost: old owner was group/other (not ODED)', body(a).ownerid !== ODED, body(a).ownerid);
  const menuA = a.ops.find(o => o.object === '1059').body.ownerid, menuB = b.ops.find(o => o.object === '1059').body.ownerid;
  check('WF-23 boost: menu allocation owner unchanged', menuA === menuB, menuA + ' / ' + menuB);
  check('WF-23 boost: other 1051 fields unchanged', JSON.stringify({ ...body(a), ownerid: 0 }) === JSON.stringify({ ...body(b), ownerid: 0 }));
  check('WF-23 boost: sale/note/cc/wa unchanged', JSON.stringify(a.ops.filter(o => o.object !== '1051')) === JSON.stringify(b.ops.filter(o => o.object !== '1051')) && JSON.stringify(a.cc) === JSON.stringify(b.cc) && JSON.stringify(a.wa) === JSON.stringify(b.wa));
  // product without manager -> fallback
  const inp2 = clone(inp); inp2['המוצר (14)'].data.find(p => U(p.productid) === U(BOOST_PID)).ownerid = '';
  const a2 = run(code('WF-23', 'before'), clone(inp2)), b2 = run(code('WF-23', 'after'), clone(inp2));
  check('WF-23 boost w/o product manager: falls back to old behaviour', body(a2).ownerid === body(b2).ownerid, body(b2).ownerid);
  check('WF-23 boost w/o product manager: warning added', b2.warnings.length === a2.warnings.length + 1);
}

// ---- WF-24: premium (synthetic from WF-25 exec) ----
function premium(inp, mut) {
  inp = clone(inp);
  const ev = inp['קליטה וסיווג']; ev.branchKey = 'MENTORING'; ev.productId = PREM_PID; ev.categoryCode = 101; ev.idemKey = 'PRO-MENTORING-TEST';
  ev.paymentBranch = 'NEW_PURCHASE';
  const prods = inp['המוצר (14)'].data; let p = prods.find(x => U(x.productid) === U(PREM_PID)); if (!p) { p = { productid: PREM_PID, name: 'תוכנית ליווי 12 שבועות', categorycode: 101, pcfDurationWeeks: 12, ownerid: ODED }; prods.push(p); }
  p.ownerid = ODED;
  inp['תהליך מכירה (4)'].data[0].pcfWhatsAppToRef = PREM_GROUP;
  mut && mut(inp);
  return inp;
}
{
  let inp = premium(setGroups(base25()) && base25());
  const rows = inp['קבוצות WhatsApp (1068)'].data; const pg = rows.find(r => U(r.customobject1068id) === U(PREM_GROUP));
  console.log('premium group owner in snapshot', pg && pg.ownerid);
  const a = run(code('WF-24', 'before'), clone(inp)), b = run(code('WF-24', 'after'), clone(inp));
  check('WF-24 premium: old owner = product manager', body(a).ownerid === ODED, body(a).ownerid);
  check('WF-24 premium: new owner = group manager', body(b).ownerid === PREM_OWNER, body(b).ownerid);
  check('WF-24 premium: group written unchanged', body(a).pcfActualGroup === body(b).pcfActualGroup && body(b).pcfActualGroup === PREM_GROUP);
  check('WF-24 premium: other 1051 fields unchanged', JSON.stringify({ ...body(a), ownerid: 0 }) === JSON.stringify({ ...body(b), ownerid: 0 }));
  check('WF-24 premium: task owner unchanged', JSON.stringify(a.ops.filter(o => o.object === '10')) === JSON.stringify(b.ops.filter(o => o.object === '10')));
  check('WF-24 premium: cc/wa unchanged', JSON.stringify(a.cc) === JSON.stringify(b.cc) && JSON.stringify(a.wa) === JSON.stringify(b.wa));
  // no group selected
  const inpN = premium(base25(), (i) => { i['תהליך מכירה (4)'].data[0].pcfWhatsAppToRef = ''; });
  const a2 = run(code('WF-24', 'before'), clone(inpN)), b2 = run(code('WF-24', 'after'), clone(inpN));
  check('WF-24 premium without group: identical to old', JSON.stringify(slim(a2)) === JSON.stringify(slim(b2)));
  // group without manager
  const inpO = premium(base25(), (i) => { i['קבוצות WhatsApp (1068)'].data.find(r => U(r.customobject1068id) === U(PREM_GROUP)).ownerid = ''; });
  const a3 = run(code('WF-24', 'before'), clone(inpO)), b3 = run(code('WF-24', 'after'), clone(inpO));
  check('WF-24 premium group without manager: owner falls back to old', body(a3).ownerid === body(b3).ownerid, body(b3).ownerid);
}

// ---- WF-25: continue ----
function cont(pid, mut) { const i = base25(); i['קליטה וסיווג'].productId = pid; const pr = i['המוצר (14)'].data; if (!pr.find(p => U(p.productid) === U(pid))) pr.push({ productid: pid, name: 'x', categorycode: 102, ownerid: REVITAL }); mut && mut(i); return i; }
{
  const inp = cont(PERSONAL);
  const exOwner = 'EXIST-OWNER-0000'; inp['תהליך ליווי קיים (1051)'].data[0].ownerid = exOwner;
  const a = run(code('WF-25', 'before'), clone(inp)), b = run(code('WF-25', 'after'), clone(inp));
  check('WF-25 personal+existing: old code overwrote owner', body(a).ownerid === REVITAL, body(a).ownerid);
  check('WF-25 personal+existing: new code writes NO ownerid', !('ownerid' in body(b)));
  check('WF-25 personal+existing: new code writes NO pcfActualGroup', !('pcfActualGroup' in body(b)));
  const strip = (x) => { const c = { ...x }; delete c.ownerid; delete c.pcfActualGroup; return c; };
  check('WF-25 personal+existing: all other 1051 fields identical', JSON.stringify(strip(body(a))) === JSON.stringify(strip(body(b))));
  check('WF-25 personal+existing: sale/note ops identical', JSON.stringify(a.ops.filter(o => o.object === '4')) === JSON.stringify(b.ops.filter(o => o.object === '4')));
  // personal, no existing record -> create as before
  const inpC = cont(PERSONAL, (i) => { i['תהליך ליווי קיים (1051)'].data = []; });
  const a2 = run(code('WF-25', 'before'), clone(inpC)), b2 = run(code('WF-25', 'after'), clone(inpC));
  check('WF-25 personal no existing (create): ownerid as before', body(a2).ownerid === body(b2).ownerid && body(b2).ownerid === REVITAL, body(b2).ownerid);
  check('WF-25 personal no existing: no group', !('pcfActualGroup' in body(b2)));
}
{
  const inp = cont(ONLINE);
  const a = run(code('WF-25', 'before'), clone(inp)), b = run(code('WF-25', 'after'), clone(inp));
  check('WF-25 online+existing: owner = advanced group manager', body(b).ownerid === ADV_OWNER, body(b).ownerid);
  check('WF-25 online+existing: group = advanced group', body(b).pcfActualGroup === ADV_GROUP);
  check('WF-25 online: program still 4, dates identical', body(b).pcfCurrentProgram === body(a).pcfCurrentProgram && body(b).pcfEstimatedEndDate === body(a).pcfEstimatedEndDate && body(b).pcfStartDate === body(a).pcfStartDate && body(b).pcfPremiumEndDate === body(a).pcfPremiumEndDate);
  check('WF-25 online: no welcome / no WA join', b.cc === null && b.wa === null);
  const inpC = cont(ONLINE, (i) => { i['תהליך ליווי קיים (1051)'].data = []; });
  const b2 = run(code('WF-25', 'after'), clone(inpC));
  check('WF-25 online no existing: owner+group of advanced', body(b2).ownerid === ADV_OWNER && body(b2).pcfActualGroup === ADV_GROUP);
  // advanced group missing from list
  const inpM = cont(ONLINE, (i) => { i['קבוצות WhatsApp (1068)'].data = i['קבוצות WhatsApp (1068)'].data.filter(r => U(r.customobject1068id) !== U(ADV_GROUP)); });
  const b3 = run(code('WF-25', 'after'), clone(inpM));
  check('WF-25 online, adv group missing + existing: no owner/group written + warning', !('ownerid' in body(b3)) && !('pcfActualGroup' in body(b3)) && b3.warnings.some(w => w.includes('קבוצת המתקדמות')));
  // advanced group without manager
  const inpO = cont(ONLINE, (i) => { i['קבוצות WhatsApp (1068)'].data.find(r => U(r.customobject1068id) === U(ADV_GROUP)).ownerid = ''; });
  const b4 = run(code('WF-25', 'after'), clone(inpO));
  check('WF-25 online, adv group w/o manager + existing: group written, owner untouched, warning', !('ownerid' in body(b4)) && body(b4).pcfActualGroup === ADV_GROUP && b4.warnings.some(w => w.includes('אין מנהלת')));
  // premium end date logic still intact
  check('WF-25 online: premium end date preserved logic intact', 'pcfPremiumEndDate' in body(b) === ('pcfPremiumEndDate' in body(a)));
}
// regression: continue branch with other product (inactive test product) behaves like personal
{
  const inp = cont('BF672C30-0000-0000-0000-000000000000');
  const b = run(code('WF-25', 'after'), clone(inp));
  check('WF-25 other continue product: treated like personal (no owner/group written)', !('ownerid' in body(b)) && !('pcfActualGroup' in body(b)));
}
console.log(fails ? `\n${fails} FAILED` : '\nALL PASSED');
process.exit(fails ? 1 : 0);
