// ============================================================================
// WF-2X · צומת המוח — בניית תוכנית הפעולה המקצועית
// ============================================================================
// כל ההכרעות העסקיות יושבות כאן, בקוד טהור, ונבדקות ע"י test/run_tests.js
// מתוך קובץ ה-workflow הבנוי — כלומר מה שנבדק הוא מה שרץ בפועל.
//
// שלושה ענפים, מבנה זהה:
//   1. איתור תהליך המכירה  2. איתור הקבוצה/המחזור  3. עדכון המכירה
//   4. יצירה/עדכון של תהליך הליווי  5. נגזרות (תפריט / משימה / הערה)
// ============================================================================

// ==== LOGIC (pure) ====
function PLAN_CORE(ctx) {
  const ev = ctx.ev;
  const cfg = ev._cfg;
  const S = (v) => (v === undefined || v === null) ? '' : String(v).trim();
  const U = (v) => S(v).toUpperCase();
  const rows = (r) => {
    if (!r) return [];
    if (Array.isArray(r)) return r;
    if (Array.isArray(r.data)) return r.data;
    if (r.data && Array.isArray(r.data.Data)) return r.data.Data;
    if (r.data && r.data.Record) return [r.data.Record];
    return [];
  };
  const cut = (s, n) => { const t = S(s); return t.length > n ? t.slice(0, n - 1) + '…' : t; };
  const num = (v) => { const n = parseFloat(v); return isNaN(n) ? 0 : n; };

  function addDaysISO(iso, days) {
    const m = String(iso || '').match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (!m) return null;
    const base = Date.UTC(+m[1], +m[2] - 1, +m[3]);
    const d = new Date(base + days * 86400000);
    const p = (x) => String(x).padStart(2, '0');
    return `${d.getUTCFullYear()}-${p(d.getUTCMonth() + 1)}-${p(d.getUTCDate())}T00:00:00Z`;
  }

  // 🔴 נוסף 15/09 — פורמט תאריך להודעת הוולקאם בוסט (DD.MM.YYYY),
  //    לפי הדוגמה בתבנית welcome_boost_v2 בקלאודצ'אט.
  function formatDMY(iso) {
    const m = String(iso || '').match(/^(\d{4})-(\d{2})-(\d{2})/);
    if (!m) return '';
    return `${m[3]}.${m[2]}.${m[1]}`;
  }

  const ops = [];
  const warnings = [];
  const decisions = ev.classifyReasons ? ev.classifyReasons.slice() : [];
  const add = (o) => { ops.push(o); return '@' + o.ref; };
  const lookupOrOmit = (obj, key, val) => { if (S(val)) obj[key] = S(val); return obj; };

  const sales      = rows(ctx.saleResp);
  const products   = rows(ctx.productResp);
  const mentorings = rows(ctx.mentoringResp);
  const cohorts    = rows(ctx.cohortResp);
  const groups     = rows(ctx.groupsResp);
  const menuAssign = rows(ctx.menuAssignResp);

  const custLabel = ev.accountName || 'לקוחה';
  const execLink = ev.sourceExecutionUrl
    ? `<a href="${ev.sourceExecutionUrl}">${ev.sourceExecutionUrl}</a>` : 'לא נמסר';

  // ---------- 0. ענפים שאין להם תהליך מקצועי ----------
  const HALT = { NO_PROCESS: 'למוצר הזה אין תהליך מקצועי מוגדר — לא בוצעה שום פעולה.',
    UNKNOWN: 'לא ניתן היה לסווג את המוצר לענף מקצועי — לא בוצעה שום פעולה.',
    WRONG_BRANCH: 'המוצר שייך לענף מקצועי אחר — התהליך הזה לא נגע בכלום.' };
  if (HALT[ev.branchKey]) {
    return { branch: ev.branchKey, ops: [], warnings, decisions,
      summary: HALT[ev.branchKey], cc: null, wa: null };
  }

  // ---------- 1. תהליך המכירה ----------
  // 🔴 הכרעת אליאל 19/08: משתמשים בתהליך המכירה ש-WF-20 כבר שייך אליו את
  //    התשלום, ולא מחפשים מחדש לפי קטגוריה. כך אין שום סיכוי שהכסף ישב על
  //    מכירה אחת והתהליך המקצועי על אחרת.
  const sale = sales.find((s) => U(s.opportunityid) === U(ev.saleid)) || sales[0] || null;
  if (!sale) {
    warnings.push('לא נמצא תהליך מכירה — התהליך המקצועי לא יכול להימשך.');
    taskOp('taskNoSale', `אין תהליך מכירה לתהליך מקצועי · ${custLabel}`,
      `התקבל סיום תשלום אך לא נמצא תהליך מכירה מקושר.\n` +
      `מוצר: ${ev.productName} · לקוחה: ${custLabel} · טלפון: ${ev.phone}\n` +
      `ריצת התשלום: ${ev.sourceExecutionUrl}`);
    return { branch: ev.branchKey + '_NO_SALE', ops, warnings, decisions,
      summary: 'לא נמצא תהליך מכירה — נפתחה משימה לטיפול ידני.', cc: null, wa: null };
  }
  const saleId = S(sale.opportunityid);
  decisions.push(`תהליך המכירה: ${S(sale.name)} (שויך ע"י תהליך התשלום).`);

  const product = products.find((p) => U(p.productid) === U(ev.productId)) || products[0] || null;
  const productName = product ? S(product.name) : ev.productName;

  // ---------- 2. הקבוצה והמחזור ----------
  const groupById = (id) => groups.find((g) => U(g.customobject1068id) === U(id)) || null;
  const cohortById = (id) => cohorts.find((c) => U(c.customobject1007id) === U(id)) || null;

  let cohort = null, group = null;

  if (ev.branchKey === 'BOOST') {
    cohort = cohortById(sale.pcfCourse);
    if (cohort) {
      decisions.push(`מחזור הבוסט נלקח מהשיוך הקיים בתהליך המכירה: ${S(cohort.name)}.`);
    } else {
      // נפילה: המחזור הפתוח להרשמה עם תאריך הפתיחה המוקדם ביותר.
      const open = cohorts
        .filter((c) => pickNum(c.pcfStatus) === cfg.COHORT_STATUS_OPEN)
        .sort((a, b) => S(a.pcfStartDate).localeCompare(S(b.pcfStartDate)));
      cohort = open[0] || null;
      if (cohort) {
        decisions.push(`בתהליך המכירה לא היה מחזור משויך — נבחר המחזור הפתוח להרשמה: ${S(cohort.name)}.`);
        warnings.push('מחזור הבוסט נבחר אוטומטית ולא מתוך שיוך קיים — מומלץ לאמת.');
      }
    }
    if (cohort) group = groupById(cohort.pcfwhatspgrouprelated);
    if (!cohort) {
      warnings.push('לא נמצא מחזור בוסט פתוח להרשמה.');
      taskOp('taskNoCohort', `אין מחזור בוסט למכירה · ${custLabel}`,
        `הלקוחה רכשה סדנת בוסט אך לא נמצא מחזור לשייך אליו.\n` +
        `תהליך מכירה: ${saleId}\nריצת התשלום: ${ev.sourceExecutionUrl}`);
    } else if (!group) {
      warnings.push(`למחזור "${S(cohort.name)}" אין קבוצת WhatsApp מקושרת — הלקוחה לא תצורף ולא תקבל קישור.`);
      taskOp('taskNoGroup', `אין קבוצת WhatsApp למחזור · ${custLabel}`,
        `מחזור: ${S(cohort.name)}\nאין קבוצה מקושרת, ולכן אין קישור הזמנה ואין צירוף אוטומטי.\n` +
        `ריצת התשלום: ${ev.sourceExecutionUrl}`);
    }
  } else if (ev.branchKey === 'MENTORING') {
    // 🔴 הכרעת הלקוחה 20/08: בענף הליווי הקבוצה נקבעת **ידנית בתהליך המכירה**,
    //    בשדה "לאיזו קבוצת WhatsApp לשייך?". לא מהמוצר, ובלי שום נפילה
    //    אוטומטית — בחירת קבוצה בשביל הלקוחה היא ניחוש, והיא נפסלה.
    group = groupById(sale.pcfWhatsAppToRef);
    if (group) {
      decisions.push(`הקבוצה נלקחה מתהליך המכירה (שיוך ידני): ${S(group.name)}.`);
    } else {
      warnings.push('🔴 בתהליך המכירה לא שויכה קבוצת WhatsApp — הלקוחה לא תצורף לקבוצה ולא תקבל קישור הצטרפות.');
      // 🔴 הכרעת אליאל 14/09: כשהשדה ריק — משימה מפורשת לשיוך ידני **בשני המקומות**
      //    (במערכת ובוואטסאפ), עם הסבר הסיבה, כדי שמי ששכח ילמד לפעם הבאה.
      //    שני מסלולי התשלום הרגילים מחייבים בחירת קבוצה; רק הקמת הו"ק מתוך
      //    מערכת גרואו עוקפת אותם, ולכן זה המקור הסביר לפער.
      const soBackOffice = S(ev.paymentBranch) === 'STANDING_ORDER_BACKOFFICE';
      const causeLine = soBackOffice
        ? 'הסיבה: התשלום הוקם כהוראת קבע **ישירות במערכת גרואו**, ולא דרך דף הסליקה או טופס התשלום שאינו אשראי. ' +
          'שני המסלולים האלה מחייבים בחירת קבוצה — הקמה ידנית בגרואו עוקפת אותם, ולכן השדה נשאר ריק.'
        : 'הסיבה: השדה "לאיזו קבוצת WhatsApp לשייך?" בתהליך המכירה נשאר ריק. ' +
          'דף הסליקה וטופס התשלום שאינו אשראי מחייבים בחירת קבוצה — אם התשלום לא עבר דרכם, אין מי שימלא את השדה.';
      taskOp('taskNoGroup', `שיוך ידני לקבוצת WhatsApp · ${custLabel}`,
        `הלקוחה רכשה ${productName}, אך לא שויכה לאף קבוצת WhatsApp — לא במערכת ולא בוואטסאפ.\n\n` +
        `${causeLine}\n\n` +
        `🔴 מה צריך לעשות — שתי פעולות, שתיהן חובה:\n` +
        `1. בתהליך המכירה — למלא את השדה "לאיזו קבוצת WhatsApp לשייך?" בקבוצה הנכונה.\n` +
        `2. בוואטסאפ — לצרף את הלקוחה לאותה קבוצה ידנית. הצירוף האוטומטי לא רץ, ולכן היא לא בפנים.\n\n` +
        `⚠️ בלי שתי הפעולות: הלקוחה לא תקבל הודעת וולקאם, לא תשויך למנטורית, ולא תהיה בקבוצה.\n\n` +
        `למניעה בפעם הבאה: הקמת הוראת קבע מתוך גרואו אינה מאפשרת לבחור קבוצה. ` +
        `כשמקימים הו"ק כך — יש למלא את השדה בתהליך המכירה בפיירברי מיד לאחר מכן.\n\n` +
        `מוצר: ${productName}\nתהליך מכירה: ${saleId}\nריצת התשלום: ${ev.sourceExecutionUrl}`);
    }
  }

  function pickNum(v) {
    if (v === null || v === undefined || v === '') return null;
    const n = parseInt(v, 10);
    return isNaN(n) ? null : n;
  }

  // ---------- 3. המדריכה ----------
  // 🔴 שני מקורות שונים, לפי הענף (הכרעת הלקוחה 20/08):
  //    ליווי  → המדריכה של **המוצר שנרכש** (מנהל המוצר בכרטיס המוצר).
  //    בוסט   → מדריכת הקבוצה של מחזור הבוסט (הכרעת אליאל 19/08).
  //    המשך   → אין דרישה; נלקח מה שקיים.
  const needsGroup = (ev.branchKey === 'BOOST' || ev.branchKey === 'MENTORING');
  let mentorId = '';
  if (ev.branchKey === 'MENTORING') {
    mentorId = S(product && product.ownerid);
    if (mentorId) {
      decisions.push('המדריכה נלקחה מהמוצר שנרכש.');
    } else {
      mentorId = S(sale.ownerid);
      warnings.push('למוצר שנרכש אין מדריכה משויכת — נלקח נציג המכירות מתהליך המכירה. מומלץ להשלים "מנהל מוצר" בכרטיס המוצר.');
    }
  } else {
    mentorId = S(group && group.ownerid)
            || S(cohort && cohort.ownerid)
            || S(product && product.ownerid)
            || S(sale.ownerid);
    if (group && S(group.ownerid)) decisions.push('המדריכה נלקחה מרשומת קבוצת ה-WhatsApp.');
    else if (needsGroup && mentorId) warnings.push('לקבוצה אין מדריכה משויכת — נלקחה נפילה (אחראי המחזור / מנהל המוצר / נציג המכירות).');
  }

  // ---------- 4. תאריכים ומספר שבועות ----------
  const giftMap = cfg.WEEKS_GIFT_MAP || {};
  const giftRaw = pickNum(sale.pcfWeeksGift);
  const giftWeeks = (giftRaw !== null && giftMap[giftRaw] !== undefined) ? giftMap[giftRaw] : 0;
  const productWeeks = product ? (num(product.pcfDurationWeeks) || 0) : 0;
  // בענף ההמשך אין אורך תוכנית — הליווי פתוח (סיום 01.01.2099).
  const totalWeeks = (ev.branchKey === 'CONTINUE') ? 0 : (productWeeks + giftWeeks);

  let startDate = ev.purchaseDateISO;
  let endDate = null;
  if (ev.branchKey === 'BOOST') {
    endDate = S(cohort && cohort.pcfEndDate) || null;
    if (!endDate) warnings.push('למחזור הבוסט אין תאריך סיום — "תאריך סיום ליווי" יישאר ריק.');
  } else if (ev.branchKey === 'MENTORING') {
    endDate = totalWeeks > 0 ? addDaysISO(ev.purchaseDateISO, totalWeeks * 7) : null;
    if (!productWeeks) warnings.push('למוצר אין "מספר שבועות לתהליך" — לא ניתן לחשב תאריך סיום ליווי.');
    if (giftWeeks) decisions.push(`נוספו ${giftWeeks} שבועות מתנה מתהליך המכירה (סה"כ ${totalWeeks} שבועות).`);
  } else if (ev.branchKey === 'CONTINUE') {
    startDate = null;                       // "לא לגעת" — לפי האפיון
    endDate = cfg.CONTINUE_END_DATE;
  }

  // ---------- 5. אידמפוטנטיות ----------
  const existing = mentorings.find((m) => U(m.pcfaccountid) === U(ev.accountid)) || null;
  const alreadyDone = existing && S(existing.pcfExternalSoftwareID2) === S(ev.idemKey);
  if (alreadyDone) {
    decisions.push('DUPLICATE — התהליך המקצועי הזה כבר בוצע עבור אותה רכישה.');
    return { branch: 'DUPLICATE', ops: [], warnings, decisions,
      summary: 'הרכישה הזו כבר טופלה — לא בוצעה שום פעולה נוספת.',
      mentoringId: S(existing.customobject1051id), cc: null, wa: null };
  }

  // ---------- 6. עדכון תהליך המכירה ----------
  const saleBody = { statuscode: cfg.SALE_STATUS_CLOSED, pcfStatusUpdateTime: ev.nowISO };
  lookupOrOmit(saleBody, 'pcfProduct', ev.productId);
  if (ev.branchKey === 'BOOST') {
    lookupOrOmit(saleBody, 'pcfCourse', cohort && cohort.customobject1007id);
    lookupOrOmit(saleBody, 'pcfWhatsAppToRef', group && group.customobject1068id);
  }
  // 🔴 בענף הליווי שדה הקבוצה בתהליך המכירה הוא **קלט ידני** — לא נכתב אליו.
  //    דריסה שלו הייתה מוחקת בחירה שהצוות עשה במו ידיו.
  add({ ref: 'sale', kind: 'update', object: '4', recordId: saleId,
    label: 'עדכון תהליך המכירה (4)', body: saleBody });

  // ---------- 7. תהליך הליווי (1051) — רשומה אחת ללקוחה ----------
  const programByBranch = {
    BOOST: cfg.PROGRAM_BOOST, MENTORING: cfg.PROGRAM_PREMIUM, CONTINUE: cfg.PROGRAM_CONTINUE,
  };
  const mentBody = {
    name: cut(`ליווי ${productName} - ${custLabel}`, 190),
    pcfStatus: cfg.MENTOR_STATUS_ACTIVE,
    pcfStatusUpdateTime: ev.nowISO,
    pcfCurrentProgram: programByBranch[ev.branchKey],
    pcfCreatedByPersonOrSystem: 2,
    pcfExternalSoftwareID2: ev.idemKey,
  };
  lookupOrOmit(mentBody, 'pcfaccountid', ev.accountid);
  lookupOrOmit(mentBody, 'pcfSale', saleId);
  lookupOrOmit(mentBody, 'pcfProduct', ev.productId);
  lookupOrOmit(mentBody, 'ownerid', mentorId);
  if (ev.branchKey !== 'CONTINUE') {
    mentBody.pcfCurrentWeek = 0;
    if (startDate) mentBody.pcfStartDate = startDate;
  }
  if (endDate) mentBody.pcfEstimatedEndDate = endDate;
  if (ev.branchKey === 'BOOST') {
    lookupOrOmit(mentBody, 'pcfBoostLinked', cohort && cohort.customobject1007id);
    lookupOrOmit(mentBody, 'pcfActualGroup', group && group.customobject1068id);
  } else if (ev.branchKey === 'MENTORING') {
    lookupOrOmit(mentBody, 'pcfActualGroup', group && group.customobject1068id);
    if (totalWeeks > 0) mentBody.pcfWeeksNumber = totalWeeks;
  }

  let mentRef;
  if (existing) {
    mentRef = add({ ref: 'mentoring', kind: 'update', object: '1051',
      recordId: S(existing.customobject1051id),
      label: 'עדכון תהליך הליווי הקיים (1051)', body: mentBody });
    decisions.push('נמצאה רשומת ליווי קיימת ללקוחה — עודכנה במקום ליצור חדשה.');
  } else {
    mentRef = add({ ref: 'mentoring', kind: 'create', object: '1051',
      label: 'יצירת תהליך ליווי (1051)', body: mentBody });
    decisions.push('לא נמצאה רשומת ליווי — נוצרה רשומה חדשה.');
  }

  // ---------- 8. הקצאה לתפריט — ענף הבוסט בלבד ----------
  if (ev.branchKey === 'BOOST') {
    const menuCatalog = rows(ctx.menuCatalogResp)
      .find((m) => U(m.customobject1060id) === U(cfg.BOOST_MENU_CATALOG_ID)) || null;
    const menuName = menuCatalog ? S(menuCatalog.name) : 'תפריט בוסט';
    // 🔴 לאובייקט 1059 אין שדה "מזהה מערכת חיצונית" (אומת חי — הקריאה נכשלת
    //    ב-Invalid field name). לכן מפתח האידמפוטנטיות נכתב בשדה "הערות".
    const menuStamp = `נוצר אוטומטית · מזהה: ${ev.idemKey}`;
    const dupMenu = menuAssign.find((m) => S(m.pcfNotes).indexOf(ev.idemKey) !== -1);
    if (dupMenu) {
      decisions.push('הקצאת התפריט כבר קיימת לרכישה הזו — לא נוצרה כפילות.');
    } else {
      const menuBody = {
        name: cut(`${menuName} - ${custLabel} 📃`, 190),
        pcfMenuStatus: cfg.MENU_STATUS_READY,
        // 🔴 תפריט הבוסט הוא תמיד סטנדרטי — לא נבנה אישית ללקוחה.
        pcfMenuType: cfg.MENU_TYPE_STANDARD,
        pcfsendtime: ev.purchaseDateISO,
        pcfCreatedByPersonOrSystem: 2,
        pcfNotes: menuStamp,
        pcfFollowupProcess: mentRef,
      };
      lookupOrOmit(menuBody, 'pcfaccountid', ev.accountid);
      lookupOrOmit(menuBody, 'ownerid', mentorId);
      lookupOrOmit(menuBody, 'pcfrelatedietmenu', cfg.BOOST_MENU_CATALOG_ID);
      add({ ref: 'menu', kind: 'create', object: '1059',
        label: 'יצירת הקצאה לתפריט (1059)', body: menuBody });
      if (!menuCatalog) warnings.push('לא נמצאה רשומת קטלוג התפריט של הבוסט — נכתב שם ברירת מחדל.');
    }
  }

  // ---------- 9. משימה למנטורית — ענף הליווי בלבד ----------
  if (ev.branchKey === 'MENTORING') {
    taskOp('taskMenu', `בחירת תפריט ל${custLabel}`,
      `הלקוחה רכשה ${productName} והצטרפה לליווי.\n` +
      `יש לבחור ולשייך לה תפריט מתאים.\n` +
      `תאריך הצטרפות: ${S(ev.purchaseDateISO).slice(0, 10)}\n` +
      `ריצת התשלום: ${ev.sourceExecutionUrl}`,
      { ownerid: mentorId, objectRef: mentRef, objectType: 1051, due: ev.purchaseDateISO });
  }

  // ---------- 10. הערה בתהליך הליווי ----------
  const noteHtml = `<div dir="rtl">התקבלה רכישה והתהליך המקצועי הוקם אוטומטית.<br>` +
    `מוצר: <b>${productName}</b> · סכום: <b>${ev.grossTotal ? ev.grossTotal.toFixed(2) + ' ₪' : '—'}</b>` +
    (cohort ? `<br>מחזור בוסט: <b>${S(cohort.name)}</b>` : '') +
    (group ? `<br>קבוצת WhatsApp: <b>${S(group.name)}</b>`
      : (ev.branchKey === 'MENTORING'
        ? `<br>🔴 <b>לא שויכה קבוצת WhatsApp.</b> השדה "לאיזו קבוצת WhatsApp לשייך?" בתהליך המכירה נשאר ריק` +
          (S(ev.paymentBranch) === 'STANDING_ORDER_BACKOFFICE'
            ? ' — התשלום הוקם כהוראת קבע ישירות במערכת גרואו, מסלול שאינו מחייב בחירת קבוצה.'
            : '.') +
          `<br>נפתחה משימה לשיוך ידני <b>במערכת ובוואטסאפ</b>. הלקוחה אינה בקבוצה עד שיבוצע.`
        : '')) +
    (ev.branchKey === 'MENTORING' && totalWeeks ? `<br>אורך התוכנית: <b>${totalWeeks} שבועות</b>` +
      (giftWeeks ? ` (כולל ${giftWeeks} מתנה)` : '') : '') +
    `<br><b>המשך התהליך מתנהל בריטיינר.</b>` +
    `<br>ריצת התשלום: ${execLink}</div>`;
  add({ ref: 'note', kind: 'create', object: 'note', label: 'הערה על תהליך הליווי',
    body: { notetext: noteHtml, objectid: mentRef, objecttypecode: 1051 } });

  // ---------- 11. הודעת וולקאם וצירוף לקבוצה ----------
  const wantsWelcome = (ev.branchKey === 'BOOST' || ev.branchKey === 'MENTORING');
  const cc = wantsWelcome ? {
    enabled: cfg.SEND_WELCOME !== false,
    flowNs: ev.branchKey === 'BOOST' ? cfg.CC_FLOW_BOOST : cfg.CC_FLOW_MENTOR,
    phone972: ev.phone972,
    // 🔴 16/09/2026 — נדרש כדי ליצור מנויה בקלאודצ'אט כשאין לה, ולכתוב את
    //    המזהה החדש חזרה לתיק הלקוחה בפיירברי.
    accountid: S(ev.accountid),
    accountName: custLabel,
    email: S(ev.email),
    fields: (() => {
      const f = [{ name: cfg.CC_FIELD_GROUP_LINK, value: S(group && group.pcfGroupLink) }];
      // 🔴 שם המנטורית בהודעה נלקח ממדריכת **קבוצת הוואטסאפ** שאליה הלקוחה
      //    מצורפת — לא מהמוצר ולא מהמחזור. הנחיית אליאל 20/08.
      //    התבנית בקלאודצ'אט לא נשלחת כשהשדה ריק, ולכן חסר כאן = אין הודעה.
      f.push({ name: cfg.CC_FIELD_MENTOR, value: S(group && group.owneridname) });
      if (ev.branchKey === 'BOOST') {
        // 🔴 תוקן 15/09 — welcome_boost_v2 דורש {{2}} = תאריך תחילת המחזור.
        //    השדה קיים בקלאודצ'אט אבל אף קוד לא כתב אליו עד עכשיו,
        //    ולכן כל שליחה נדחתה במטא עם #131008 (send-sub-flow החזיר ok
        //    כי זו רק קליטה, והדחיה בפועל קרתה בצד מטא, בשקט מבחינת n8n).
        f.push({ name: cfg.CC_FIELD_BOOST_CYCLE_DATE, value: formatDMY(cohort && cohort.pcfStartDate) });
      }
      if (ev.branchKey === 'MENTORING') {
        f.push({ name: cfg.CC_FIELD_PRODUCT, value: productName });
        f.push({ name: cfg.CC_FIELD_WEEKS, value: totalWeeks ? String(totalWeeks) : '' });
      }
      return f.filter((x) => S(x.value) !== '');
    })(),
  } : null;
  if (cc && !S(group && group.pcfGroupLink)) {
    warnings.push('לקבוצה אין "לינק לקבוצה" — הודעת הוולקאם תצא בלי קישור הצטרפות.');
  }
  if (cc && !S(group && group.owneridname)) {
    warnings.push('🔴 לקבוצת הוואטסאפ אין מדריכה משויכת — שדה "מנטורית" יישאר ריק ' +
      'והתבנית בקלאודצ\'אט לא תישלח. יש להשלים את המדריכה ברשומת הקבוצה.');
  }
  if (cc && ev.branchKey === 'BOOST' && !S(cohort && cohort.pcfStartDate)) {
    warnings.push('🔴 למחזור הבוסט אין "תאריך התחלה" — הודעת הוולקאם תיכשל אצל מטא (#131008), ' +
      'כי {{2}} יישאר ריק.');
  }

  const wa = (wantsWelcome && group && S(group.pcfGreenApiId)) ? {
    enabled: cfg.JOIN_WA_GROUP !== false,
    groupId: S(group.pcfGreenApiId),
    groupRecordId: S(group.customobject1068id),
    groupName: S(group.name),
    inviteLink: S(group.pcfGroupLink),
    chatId: ev.phone972 ? ev.phone972 + '@c.us' : '',
  } : null;

  const summaryByBranch = {
    BOOST: 'הוקם תהליך ליווי בוסט, שויך מחזור וקבוצה, ונוצרה הקצאה לתפריט.',
    MENTORING: 'הוקם תהליך ליווי, שויכה קבוצה, ונפתחה משימה לבחירת תפריט.',
    CONTINUE: 'הוקם/עודכן תהליך ליווי המשך.',
  };

  function taskOp(ref, subject, description, opts) {
    const o = opts || {};
    // 🔴 taskOp נקרא גם לפני ש-saleId מוגדר (מסלול "אין תהליך מכירה").
    //    גישה ישירה ל-const לפני האתחול זורקת ReferenceError ומפילה את כל
    //    התהליך המקצועי. נתפס חי 30/08. הגישה נעשית דרך try.
    let _saleId = '';
    try { _saleId = saleId; } catch (e) { _saleId = ''; }
    const b = {
      subject: cut(subject, 190),
      description: cut(description, 4000),
      statuscode: cfg.DEFAULT_TASK_STATUS,
      prioritycode: cfg.DEFAULT_TASK_PRIORITY,
      tasktypecode: cfg.DEFAULT_TASK_TYPE,
      scheduledend: o.due || ev.todayISO,
      pcfCreatedByPersonOrSystem: 2,
      pcfExternalSoftwareID1: `${ev.idemKey}-TASK-${ref}`,
    };
    lookupOrOmit(b, 'pcfSale', _saleId);
    lookupOrOmit(b, 'pcfClient', ev.accountid);
    lookupOrOmit(b, 'ownerid', o.ownerid || S(sale && sale.ownerid));
    if (o.objectRef) { b.objectid = o.objectRef; b.objecttypecode = o.objectType || 1051; }
    return add({ ref, kind: 'create', object: '10', label: 'משימה לנציגה', body: b });
  }

  return {
    branch: ev.branchKey, ops, warnings, decisions,
    summary: summaryByBranch[ev.branchKey] || 'התהליך המקצועי הושלם.',
    saleId, productName, mentorId,
    cohortId: S(cohort && cohort.customobject1007id),
    cohortName: S(cohort && cohort.name),
    groupId: S(group && group.customobject1068id),
    groupName: S(group && group.name),
    totalWeeks, giftWeeks, startDate, endDate,
    existingMentoringId: S(existing && existing.customobject1051id),
    cc, wa,
  };
}

function LOGIC(ctx) {
  const ev = ctx.ev;
  const cfg = ev._cfg;
  const out = PLAN_CORE(ctx);
  const dry = (cfg.DRY_RUN === false) ? false : !ev.liveTest;
  if (ev.liveTest) out.decisions.push('🔴 חשבון בדיקה מורשה — הריצה מתבצעת בפועל.');
  else if (dry) out.decisions.push('🔒 DRY_RUN — תצוגה מקדימה בלבד. אפס כתיבה, אפס הודעות, אפס צירוף לקבוצה.');
  return [{ json: Object.assign({}, ev, out, { DRY_RUN: dry, liveTest: ev.liveTest }) }];
}

// ==== N8N BINDING ====
return LOGIC({
  ev: $('קליטה וסיווג').first().json,
  saleResp: $('תהליך מכירה (4)').first().json,
  productResp: $('המוצר (14)').first().json,
  mentoringResp: $('תהליך ליווי קיים (1051)').first().json,
  cohortResp: $('מחזורי בוסט (1007)').first().json,
  groupsResp: $('קבוצות WhatsApp (1068)').first().json,
  menuCatalogResp: $('קטלוג תפריטים (1060)').first().json,
  menuAssignResp: $('הקצאות תפריט (1059)').first().json,
});
