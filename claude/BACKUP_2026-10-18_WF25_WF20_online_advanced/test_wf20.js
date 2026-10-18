// Replay WF-20 plan node (old vs new) on the saved כרמית גל / איילת בירק לוי executions.
const fs = require('fs');
const dir = __dirname;
const NODES = ['קריאת פרטי המסמך','חיפוש לקוחה לפי טלפון (1)','חיפוש תשלום לפי מזהה עסקה (1039)','חיפוש תהליך מכירה (4)','חיפוש תשלומים של הלקוחה (1039)','חיפוש תיעודי תשלום (1018)','קטלוג המוצרים (14)','מסמכים אחרונים (1038)','מסמך המקור לפי מספר (1038)','תיעוד המקור לפי מספר מסמך (1018)'];

function planCode(when) { return fs.readFileSync(`${dir}/../research_pro/WF20/17_בניית_תוכנית_פעולה.js`, 'utf8'); }

function runPlan(code, inputs) {
  const $ = (name) => ({ first: () => ({ json: inputs[name] }), all: () => [{ json: inputs[name] }] });
  const wf = { id: 'WF20' }, ex = { id: 'x' };
  const fn = new Function('$', '$workflow', '$execution', code);
  return fn($, wf, ex)[0].json;
}

// rebuild ev with patched cfg from WF-20 normalize (new alias) vs original cfg
const normNew = fs.readFileSync(`${dir}/WF-20_normalize_after.js`, 'utf8');
const normOld = fs.readFileSync(`${dir}/WF-20_normalize_before.js`, 'utf8');
function cfgOf(code) {
  const m = code.match(/const CFG = (\{[\s\S]*?\n\});/);
  return eval('(' + m[1] + ')');
}
const cfgOld = cfgOf(normOld), cfgNew = cfgOf(normNew);
console.log('alias old present:', 'ליווי אונליין מתקדמות' in cfgOld.PRODUCT_NAME_ALIASES, '| new:', 'ליווי אונליין מתקדמות' in cfgNew.PRODUCT_NAME_ALIASES);

const files = ['WF-20_370767.json', 'WF-20_370868.json'];
let fails = 0;
for (const f of files) {
  const d = JSON.parse(fs.readFileSync(`${dir}/../research_pro/execs2/${f}`));
  const rd = d.data.resultData.runData;
  const inputs = {};
  for (const n of NODES) inputs[n] = rd[n][0].data.main[0][0].json;
  const evOld = JSON.parse(JSON.stringify(inputs['קריאת פרטי המסמך']));
  const evNew = JSON.parse(JSON.stringify(inputs['קריאת פרטי המסמך']));
  evOld._cfg = cfgOld; evNew._cfg = cfgNew;
  inputs['קריאת פרטי המסמך'] = evOld;
  const a = runPlan(planCode(), inputs);
  inputs['קריאת פרטי המסמך'] = evNew;
  const b = runPlan(planCode(), inputs);
  const desc = evNew.descriptionText;
  console.log('\n==', f, '| GROW desc:', desc, '|', b.accountName);
  console.log('   old productId:', JSON.stringify(a.productId), '| new:', JSON.stringify(b.productId), '|', b.productName);
  console.log('   new warnings:', (b.warnings || []).filter(w => w.includes('מוצר')));
  if (!(b.productId && b.productId.startsWith('58A4D4F9'))) { fails++; console.log('   FAIL: still unmatched'); }
  if (!((a.warnings || []).some(w => w.includes('לא זוהה מוצר')))) { fails++; console.log('   FAIL: old code did not warn'); }
}
console.log(fails ? `\n${fails} FAILED` : '\nALL PASSED');
process.exit(fails ? 1 : 0);
