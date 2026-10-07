import json, sys

NODE = 'בניית תוכנית מקצועית'
STAMP = '🔴 07/10/2026 (הנחיית הלקוחה, אישור סער)'


def must_replace(code, old, new, label):
    assert code.count(old) == 1, f'anchor not unique/missing: {label} ({code.count(old)})'
    return code.replace(old, new)


def patch_wf23(code):
    # BOOST: המדריכה בתהליך הליווי = "מנהל מוצר" בכרטיס מוצר הבוסט. הנפילה הקודמת נשמרת רק אם אין מנהל מוצר.
    old = "  // ---------- 4. תאריכים ומספר שבועות ----------"
    new = f"""  // {STAMP}: בוסט, המדריכה בתהליך הליווי נלקחת מ\"מנהל מוצר\" בכרטיס
  //    מוצר הבוסט (אובייקט 14). אין מנהל מוצר ⇒ נשארת הנפילה הקודמת (mentorId).
  //    משפיע רק על בעלי רשומת הליווי (1051). שאר השימושים ב-mentorId לא שונו.
  let processOwnerId = mentorId;
  if (ev.branchKey === 'BOOST') {{
    const exactProduct = products.find((p) => U(p.productid) === U(ev.productId)) || null;
    const prodOwner = S(exactProduct && exactProduct.ownerid);
    if (prodOwner) {{
      processOwnerId = prodOwner;
      decisions.push('המדריכה בתהליך הליווי נלקחה מ\"מנהל מוצר\" בכרטיס מוצר הבוסט.');
    }} else {{
      warnings.push('למוצר הבוסט אין \"מנהל מוצר\", המדריכה בתהליך הליווי נלקחה מהנפילה (קבוצה / מחזור / נציג המכירות).');
    }}
  }}

""" + old
    code = must_replace(code, old, new, 'wf23 section4')
    code = must_replace(code, "  lookupOrOmit(mentBody, 'ownerid', mentorId);",
                        "  lookupOrOmit(mentBody, 'ownerid', processOwnerId);", 'wf23 ownerid')
    return code


def patch_wf24(code):
    # MENTORING: המדריכה בתהליך הליווי = מנהלת קבוצת הוואטסאפ שנבחרה בתהליך המכירה (1068.ownerid).
    old = "  // ---------- 4. תאריכים ומספר שבועות ----------"
    new = f"""  // {STAMP}: פרימיום, המדריכה בתהליך הליווי היא מנהלת קבוצת הוואטסאפ שנבחרה
  //    בתהליך המכירה (1068.ownerid). אין קבוצה / אין מנהלת לקבוצה ⇒ נשארת הנפילה
  //    הקודמת (מנהל המוצר, ואז נציג המכירות). משפיע רק על בעלי רשומת הליווי (1051).
  let processOwnerId = mentorId;
  if (ev.branchKey === 'MENTORING') {{
    const groupOwner = S(group && group.ownerid);
    if (groupOwner) {{
      processOwnerId = groupOwner;
      decisions.push('המדריכה בתהליך הליווי נלקחה ממנהלת קבוצת ה-WhatsApp שנבחרה בתהליך המכירה: ' + S(group.name) + '.');
    }} else if (group) {{
      warnings.push('לקבוצה \"' + S(group.name) + '\" אין מנהלת משויכת, המדריכה בתהליך הליווי נלקחה מהנפילה (מנהל המוצר / נציג המכירות).');
    }}
  }}

""" + old
    code = must_replace(code, old, new, 'wf24 section4')
    code = must_replace(code, "  lookupOrOmit(mentBody, 'ownerid', mentorId);",
                        "  lookupOrOmit(mentBody, 'ownerid', processOwnerId);", 'wf24 ownerid')
    return code


def patch_wf25(code):
    # CONTINUE: אישית = לא נוגעים במדריכה ובקבוצה הקיימות. אונליין = קבוצת המתקדמות ומנהלת הקבוצה.
    old = "\n  function pickNum(v) {"
    new = f"""
  // {STAMP}: תוכנית המשך.
  //   אישית: לא משנים את המדריכה ואת הקבוצה הקיימות ברשומת הליווי.
  //   אונליין: העברה לקבוצת המתקדמות, והמדריכה היא מנהלת הקבוצה (כמו בפרימיום).
  const CONTINUE_ONLINE_PRODUCT_ID = '58A4D4F9-5921-4BFC-BA8E-518877FAA375'; // תוכנית המשך אונליין
  const ADVANCED_GROUP_ID = '31CFC752-938B-4BE7-BCAD-2E36BAFFC733';         // להתאהב בעצמך מחדש רויטל יעיש 1- מתקדמות
  if (ev.branchKey === 'CONTINUE') {{
    if (U(ev.productId) === U(CONTINUE_ONLINE_PRODUCT_ID)) {{
      group = groupById(ADVANCED_GROUP_ID);
      if (group) {{
        decisions.push('תוכנית המשך אונליין: הלקוחה הועברה לקבוצת המתקדמות (' + S(group.name) + ').');
      }} else {{
        warnings.push('🔴 תוכנית המשך אונליין: קבוצת המתקדמות לא נמצאה ברשימת הקבוצות, הקבוצה והמדריכה בתהליך הליווי לא שונו.');
      }}
    }} else {{
      decisions.push('תוכנית המשך אישית: המדריכה והקבוצה בתהליך הליווי הקיים לא שונו.');
    }}
  }}
""" + old
    code = must_replace(code, old, new, 'wf25 anchor')

    old_owner = "  lookupOrOmit(mentBody, 'ownerid', mentorId);"
    new_owner = """  // 🔴 07/10/2026: ברשומת ליווי קיימת, המדריכה משתנה רק באונליין (למנהלת קבוצת המתקדמות).
  //    בכל מקרה אחר בהמשך (אישית, או אונליין בלי קבוצה/מנהלת): לא כותבים ownerid כלל.
  let ownerForRecord = mentorId;
  if (ev.branchKey === 'CONTINUE' && existing) {
    if (!group) {
      ownerForRecord = '';
    } else if (!S(group.ownerid)) {
      ownerForRecord = '';
      warnings.push('🔴 לקבוצת המתקדמות אין מנהלת משויכת, המדריכה בתהליך הליווי לא שונתה.');
    } else {
      ownerForRecord = S(group.ownerid);
    }
  }
  lookupOrOmit(mentBody, 'ownerid', ownerForRecord);"""
    code = must_replace(code, old_owner, new_owner, 'wf25 ownerid')

    old_grp = """  } else if (ev.branchKey === 'MENTORING') {
    lookupOrOmit(mentBody, 'pcfActualGroup', group && group.customobject1068id);
    if (totalWeeks > 0) mentBody.pcfWeeksNumber = totalWeeks;
  }"""
    new_grp = old_grp + """
  // 🔴 07/10/2026: המשך אונליין בלבד כותב קבוצה (המתקדמות). המשך אישית לא כותב קבוצה.
  if (ev.branchKey === 'CONTINUE' && group) {
    lookupOrOmit(mentBody, 'pcfActualGroup', group.customobject1068id);
  }"""
    code = must_replace(code, old_grp, new_grp, 'wf25 group')
    return code


def main():
    out = {}
    for name, fn in (('WF-23', patch_wf23), ('WF-24', patch_wf24), ('WF-25', patch_wf25)):
        wf = json.load(open(f'live_{name}_before.json'))
        n = [x for x in wf['nodes'] if x['name'] == NODE]
        assert len(n) == 1
        old = n[0]['parameters']['jsCode']
        new = fn(old)
        open(f'{name}_planner_before.js', 'w').write(old)
        open(f'{name}_planner_after.js', 'w').write(new)
        n[0]['parameters']['jsCode'] = new
        body = {k: wf[k] for k in ('name', 'nodes', 'connections', 'settings')}
        json.dump(body, open(f'{name}_after_put.json', 'w'), ensure_ascii=False)
        print(name, 'patched', len(old), '->', len(new))


main()
