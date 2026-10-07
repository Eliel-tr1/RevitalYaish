// Harness: runs planner code (old vs new) on real execution inputs and synthetic scenarios.
const fs = require('fs');
const dir = process.argv[2];
const NODES = ['קליטה וסיווג','תהליך מכירה (4)','המוצר (14)','תהליך ליווי קיים (1051)','מחזורי בוסט (1007)','קבוצות WhatsApp (1068)','קטלוג תפריטים (1060)','הקצאות תפריט (1059)'];

function run(code, inputs) {
  const $ = (name) => ({ first: () => ({ json: inputs[name] }), all: () => [{ json: inputs[name] }] });
  const fn = new Function('$', code);
  const r = fn($);
  return r[0].json;
}
function loadExec(f) {
  const d = JSON.parse(fs.readFileSync(f));
  const rd = d.data.resultData.runData; const inp = {};
  for (const n of NODES) inp[n] = rd[n][0].data.main[0][0].json;
  return inp;
}
const slim = (p) => ({
  branch: p.branch, ops: p.ops.map(o => ({ref:o.ref, kind:o.kind, object:o.object, recordId:o.recordId, body:o.body})),
  warnings: p.warnings, decisions: p.decisions, cc: p.cc, wa: p.wa, groupId: p.groupId, groupName: p.groupName,
});
module.exports = { run, loadExec, slim, NODES };
if (require.main === module) {
  const which = process.argv[3]; // WF-23 / WF-25
  const oldC = fs.readFileSync(`${dir}/${which}_planner_before.js`, 'utf8');
  const newC = fs.readFileSync(`${dir}/${which}_planner_after.js`, 'utf8');
  const files = fs.readdirSync(`${dir}/../research_pro/execs`).filter(f => f.startsWith(which.replace('-','') + '_'));
  let diffs = 0;
  for (const f of files) {
    const inp = loadExec(`${dir}/../research_pro/execs/${f}`);
    const a = slim(run(oldC, inp)), b = slim(run(newC, inp));
    const ja = JSON.stringify(a), jb = JSON.stringify(b);
    const ownerOld = (a.ops.find(o=>o.object==='1051')||{body:{}}).body.ownerid;
    const ownerNew = (b.ops.find(o=>o.object==='1051')||{body:{}}).body.ownerid;
    const groupNew = (b.ops.find(o=>o.object==='1051')||{body:{}}).body.pcfActualGroup;
    if (ja !== jb) { diffs++;
      // field-level diff of 1051 op, other ops
      const keys = new Set();
      a.ops.forEach((o,i)=>{ const o2=b.ops[i]; for (const k of new Set([...Object.keys(o.body),...Object.keys(o2.body)])) if (JSON.stringify(o.body[k])!==JSON.stringify(o2.body[k])) keys.add(o.ref+'.'+k); });
      console.log(f, 'DIFF fields:', [...keys].join(','), '| decisions+', b.decisions.length-a.decisions.length, '| warnings+', b.warnings.length-a.warnings.length);
    } else console.log(f, 'identical');
    if (process.argv[4]) console.log('   ownerOld', ownerOld, 'ownerNew', ownerNew, 'groupNew', groupNew);
  }
  console.log('files', files.length, 'with diffs', diffs);
}
