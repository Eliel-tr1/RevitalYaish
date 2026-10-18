import json

STAMP = '🔴 18/10/2026 (בקשת הלקוחה, אישור סער)'
PLANNER = 'בניית תוכנית מקצועית'
NORMALIZE = 'נירמול וסיווג'


def rep(code, old, new, label):
    assert code.count(old) == 1, f'anchor {label}: {code.count(old)}'
    return code.replace(old, new)


# ---------------- WF-25: אונליין => תוכנית נוכחית = מתקדמים ----------------
wf = json.load(open('live_WF-25_before.json'))
node = [n for n in wf['nodes'] if n['name'] == PLANNER][0]
code = node['parameters']['jsCode']

old_decl = "  const CONTINUE_ONLINE_PRODUCT_ID = '58A4D4F9-5921-4BFC-BA8E-518877FAA375'; // תוכנית המשך אונליין"
new_decl = "  let programOverride = null;\n" + old_decl
code = rep(code, old_decl, new_decl, 'wf25 programOverride decl')

old_online = """      group = groupById(ADVANCED_GROUP_ID);
      if (group) {"""
new_online = """      group = groupById(ADVANCED_GROUP_ID);
      // 🔴 18/10/2026: תוכנית המשך אונליין היא המסלול המתקדם, ולכן התוכנית
      //    הנוכחית ברשומת הליווי נכתבת כ"מתקדמים" ולא כ"המשך".
      programOverride = cfg.PROGRAM_ADVANCED;
      if (group) {"""
code = rep(code, old_online, new_online, 'wf25 online branch')

old_prog = """  const programByBranch = {
    BOOST: cfg.PROGRAM_BOOST, MENTORING: cfg.PROGRAM_PREMIUM, CONTINUE: cfg.PROGRAM_CONTINUE,
  };"""
new_prog = old_prog + """
  // 🔴 18/10/2026: עקיפת התוכנית לפי סוג רכישת ההמשך (אונליין ⇒ מתקדמים).
  const programCode = (programOverride !== null) ? programOverride : programByBranch[ev.branchKey];"""
code = rep(code, old_prog, new_prog, 'wf25 programByBranch')

code = rep(code, "    pcfCurrentProgram: programByBranch[ev.branchKey],",
           "    pcfCurrentProgram: programCode,", 'wf25 pcfCurrentProgram')

open('WF-25_planner_before.js', 'w').write(node['parameters']['jsCode'])
open('WF-25_planner_after.js', 'w').write(code)
node['parameters']['jsCode'] = code
json.dump({k: wf[k] for k in ('name', 'nodes', 'connections', 'settings')},
          open('WF-25_after_put.json', 'w'), ensure_ascii=False)

# ---------------- WF-20: מיפוי שם גרואו "ליווי אונליין מתקדמות" ----------------
wf20 = json.load(open('live_WF-20_before.json'))
n20 = [n for n in wf20['nodes'] if n['name'] == NORMALIZE][0]
code20 = n20['parameters']['jsCode']
old_alias = "    'ליווי אונליין מנטורית אישית': '58A4D4F9-5921-4BFC-BA8E-518877FAA375',       // תוכנית המשך אונליין"
new_alias = old_alias + "\n    'ליווי אונליין מתקדמות': '58A4D4F9-5921-4BFC-BA8E-518877FAA375',            // תוכנית המשך אונליין (349 ₪, המסלול המתקדם)"
code20 = rep(code20, old_alias, new_alias, 'wf20 alias')
open('WF-20_normalize_before.js', 'w').write(n20['parameters']['jsCode'])
open('WF-20_normalize_after.js', 'w').write(code20)
n20['parameters']['jsCode'] = code20
json.dump({k: wf20[k] for k in ('name', 'nodes', 'connections', 'settings')},
          open('WF-20_after_put.json', 'w'), ensure_ascii=False)

print('patched WF-25 planner and WF-20 normalize')
