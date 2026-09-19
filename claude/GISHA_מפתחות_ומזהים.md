# מפתחות גישה · רויטל יעיש

מסמך עזר לסשנים אוטומטיים. המפתחות של פיירברי ו-n8n מופיעים גם בהוראות הפרויקט. זה של קלאודצ'אט לא הופיע בשום מקום קבוע, ולכן נוסף כאן.

| מערכת | מפתח | שימוש |
|---|---|---|
| Fireberry | `b06663c4-62df-41b7-9111-6653e6b54592` | header `tokenid`, base `https://api.fireberry.com` |
| n8n Public API | `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NTMwY2U1OC0yNDc1LTQ1ZGEtOTdhNC1iZjBlYzQ4OWExODAiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwiaWF0IjoxNzg1NjY5MTcyfQ.gjbLnTDSHS8yJYWGMdw-fzltrPIpoEcgPm2X1LEkJLo` | header `X-N8N-API-KEY`, base `https://n8n.srv964196.hstgr.cloud` |
| CloudChat | `zBP7UlqAf3j3r9Ry89T1JUprYwjtSIYvIApxqMJjMH2RVtkRuvEMoTEVF6qT` | header `Authorization: Bearer`, base `https://console.thecloud.chat/api` |

## מלכודות ידועות

- **Cloudflare חוסם את urllib של פייתון מול קלאודצ'אט (403).** חובה header `User-Agent` של דפדפן. curl עובד.
- מפרט ה-OpenAPI של קלאודצ'אט נמצא ב-`https://console.thecloud.chat/api-docs` (בשורש, לא תחת `/api`).
- פיירברי: `page_size` מקסימלי 500. שם שדה לא מוכר ב-`fields` מחזיר 0 שורות בשקט.
- פיירברי: פיקליסטים נכתבים כמספרים ומוחזרים כתוויות בעברית.

## מזהי פלואוז בקלאודצ'אט (אומת 20.08.2026)

| תפקיד | שם הפלואו | מזהה |
|---|---|---|
| הזמנה לוובינר | `boost_webinar_invite (1day before)` | `f201689s2623961` |
| תזכורת וובינר בוקר | `boost_webinar (sameday morning)` | `f201689s4552435` |
| וובינר מתחיל | `boost_webinar_(going live)` | `f201689s2623973` |
| פולואפ וובינר | `boost_webinar_followup` | `f201689s4552451` |
| זימון לפגישה | `Client_Notification_new_meeting` | `f201689s403395` |
| תזכורת פגישה יום לפני | `Client_Notification_meeting_reminder_1day` | `f201689s403387` |
| תזכורת פגישה ביום עצמו | `Client_Notification_meeting_reminder_Sameday` | `f201689s403399` |
| תזכורת 30 דקות | `meeting_reminder_30m` | `f201689s4552587` |
| שקילה | `weekly_weighin` | `f201689s4552553` |
| שקילה פולואפ 1 | `weekly_weighin_fu1` | `f201689s4552561` |
| שקילה פולואפ 2 | `weekly_weighin_fu2` | `f201689s4552563` |

**שלב השעה לפני הוובינר בוטל** לבקשת מייק (20.08.2026). אין פלואו ואין הודעה.

## לקוחת הבדיקה

| מערכת | מזהה | פרטים |
|---|---|---|
| פיירברי (אובייקט 1) | `f23e28c0-af71-494c-a8ce-ad5cd19d7694` | סער וינברג (טסט), 0533435240 |
| קלאודצ'אט | `f201689u860230363` | סער וינברג, `+972533435240` |

## מבנה הוובהוק מקלאודצ'אט

```json
{ "userns": "...", "flow_name": "...", "button_clicked": "...", "action": "..." }
```

ערכי `action`: `meet_revital_request`, `schedule approved`, `schedule declined`.
פענוח טלפון: `GET /subscriber/get-info?user_ns=<ns>` מחזיר `phone` ו-`user_id`.

## המלצה

שלושת המפתחות הודבקו בצ'אט לאורך הסשן. מומלץ להחליף את כולם כשמסיימים את ההטמעה.
