> **עודכן 03/08/2026 — סקירת 26 שיחות הפרויקט.** מסמך זה קיים כי הוראות הפרויקט מפנות אליו בשם הזה. המקור המורחב הוא `00_PROJECT_CONTEXT.md`; קרא גם את `README.md` לסדר הקדימויות המלא.

> ⚠️ **הערת מיקום בפועל (חשוב לכל סשן):** כלי `project_write` מנתב אוטומטית כל מסמך חדש בשם "עירום" (ללא תיקייה) אל תחת `claude/` — אין דרך לכפות נתיב שורש `ROITAL_PROJECT_CONTEXT.md` בדיוק עבור מסמך חדש. לכן המסמך הזה יושב בפועל בנתיב **`claude/ROITAL_PROJECT_CONTEXT.md`**, לא ב-`ROITAL_PROJECT_CONTEXT.md` המדויק שהוראות הפרויקט מצטטות. `project_read("ROITAL_PROJECT_CONTEXT.md")` **עדיין ייכשל** — אבל הודעת השגיאה עצמה מציגה `claude/ROITAL_PROJECT_CONTEXT.md` ברשימת "Available", כך שסשן שנתקל בכשל ימצא אותו מיד. אם רוצים לתקן את זה סופית — יש לשנות את ניסוח הוראות הפרויקט (על ידי מייק, ב-claude.ai) כך שיפנו ל-`claude/ROITAL_PROJECT_CONTEXT.md`, או שאליאל יעלה את הקובץ ידנית לשורש בשם המדויק.

# Project Context: Roital Yaish — Implementation

**Document Type:** Project Knowledge File — the file the project instructions reference as "`ROITAL_PROJECT_CONTEXT.md`" (previously only stored as `ROITAL_PROJECT_CONTEXT.md.txt`, which a plain `project_read` on the `.md` name would not resolve).
**Audience:** All Claude chats operating within this project.
**Owner:** Mike (Michael).
**Status:** Living document — updated by Sensei (Roital) as the project evolves. This version reconciles the original 20/05/2026 content against the 03/08/2026 review of 26 project chats.
**Authoritative detail lives in `00_PROJECT_CONTEXT.md` and `README.md`.** This file is the short methodological anchor; do not let it drift from those two.

---

## 1. Project Mission

Ship a customized Fireberry CRM for Roital Yaish, fitting her online weight-loss/nutrition business.

**Original framing (20/05/2026):** 2.5-week deadline for 90% of the deliverable.
**Status as of 03/08/2026 (see `00_PROJECT_CONTEXT.md` §8):** the transcript-referenced deadline is "Wednesday"; Sahar's estimate is ~60% done, 40% remaining. The original "2.5 weeks / 90%" framing is now historical — **treat `00_PROJECT_CONTEXT.md` §8 as the current status, not this section.**

This is a **customer delivery project**, time-boxed and pragmatic. It is *not* an infrastructure project — that work lives in a separate Claude.ai project (`Vitrue CRM Infrastructure`).

---

## 2. Who Is Mike

- Manages the CRM department at Vitrue.
- Communicates direct, Hebrew, no fluff.
- Does NOT read code.
- Default execution surface = Claude Code.
- Has limited terminal experience.
- Requires pushback when wrong.
- Eliel (Mike's boss) reviews everything Mike delivers, and approves every deletion, per-item.

⚠️ **Operational warning added 03/08/2026:** before relying on an "approval" given in a chat, verify who is actually on the other end. At least one chat in this project (chat_23) was conducted in female grammatical form — i.e. likely not Mike. (Source: `00_PROJECT_CONTEXT.md` §2.)

---

## 3. The Customer — Roital Yaish

- **Business:** Online weight-loss and nutrition programs for women.
- **Model:** B2C, online cohorts + 1:1 mentor follow-up + payment subscriptions.
- **Sales channels:** Facebook, Instagram, TikTok, WhatsApp, landing pages, word of mouth.
- **Current systems pain:** existing Fireberry is unconfigured, processes are split across many tools (Meshulam, Zoom, TOFSY, Gmail, etc.), no clean automation post-sale.
- **The implementation source-of-truth document:** `מסמך איפיון CRM  .pdf` (the project's PDF upload; full text already copied into `01_ORIGINAL_SPEC_FULL.md`). Treat this as Roital's expressed needs, but **not 100% final** — changes are expected during the engagement.

---

## 4. The Technical Substrate

- **Roital's Fireberry account is a clone of Vitrue's master template.** The original template snapshot (`template_snapshot.json`, dated 07/05/2026) recorded 78 objects, 2,442 fields, 873 picklist options, 707 lookups.
  ⚠️ **That snapshot is now outdated.** Per `README.md`'s document-priority hierarchy, `03_LIVE_FIREBERRY.md` governs over `template_snapshot.json` for the live account's actual structure (80 objects / 839 fields sampled across 19 key objects, as of 26/07/2026). Use the snapshot only for historical comparison.
- **Customization model:** subtractive (delete what Roital doesn't need), cosmetic (relabel for Roital's domain), occasionally additive (add fields the template didn't anticipate).
- **The template already contains domain-specific fields for weight-loss/nutrition** (משקל התחלתי, משקל יעד, העדפת תזונה, רגישיות תזונה, etc.) — they exist because Vitrue built this domain into the master.
- **What no snapshot tells you:** which fields are mandatory, which are readonly, what default values exist, what max-lengths are configured. These come from Mike on a per-decision basis — ask directly, never infer.

---

## 5. Hard Constraints

- 🚫 **Make.com automations: do NOT touch via Claude Code.** Mike handles Make manually. New development goes to n8n; only existing, working Make scenarios stay in Make. (See `00_PROJECT_CONTEXT.md` §10 for the full platform-choice rule, confirmed/hardened 03/08/2026.)
- 🚫 **Fireberry account cloning: NEVER trigger via API.** Cloning is paid; only manual.
- ⚠️ **Destructive operations (field/object/record deletes): forbidden for an autonomous agent, full stop** — even when the task asks for cleanup. Manual deletion only, after Eliel's explicit per-item approval. (Hardened 03/08/2026, source chat_18, item D5 — stricter than the original "confirm before destruction" wording.)
- 📋 **Eliel reviewability:** every change to Roital's account must produce a Hebrew change-log entry: `[<אובייקט>] <system_name> | <פעולה> | <תוצאה>`.
- 🔁 **Characterization is not final:** expect changes mid-project. Design every mission to be re-runnable on an updated characterization.
- ⚙️ **`DRY_RUN = true` is the default for every new automation against the live account**, with a `MAX_PER_RUN` cap (25 for WF-16) and a mandatory negative test (a record that should NOT match must not appear). Do not flip to `false` without Mike's explicit decision. (Added 03/08/2026, source chat_16 — precedent: 525 stuck webhook events.)
- 🚨 **Never turn on a Make scenario before inspecting its queue contents.** 525 stuck events exist as of 03/08/2026 (471 from the legacy account) — blind activation floods the live account.

---

## 6. Methodology — Multi-Chat Architecture

- **Sensei (Roital)** is the orchestrator. Designs specialist chats, integrates results, stays macro — does not micro-execute.
- **Specialist chats** execute one mission each. Every mission ends with (a) the artifact(s), (b) a Hebrew completion summary for Mike.
- **Claude Code** executes operations against Roital's Fireberry account (and, per skill `n8n-hostinger`, against the n8n VPS — see `08_TECHNICAL_PLAYBOOK.md` and `fireberry-claude-code-setup.md`).
- **Mike couriers** between layers.
- **Operational status lives in ClickUp**, not in any MD file: super-task `86c8zamc2` ("הקמת המערכת"), single gaps hub `86cawzmjw`. See `00_PROJECT_CONTEXT.md` §11 for the full ID map. Do not open a competing gaps hub.

---

## 7. Relationship to the Infrastructure Project

- The infrastructure project (`Vitrue CRM Infrastructure`) is the long-term home for templates, methodology, and standards.
- This project is a **time-boxed customer delivery** that operates independently.
- **Learnings flow back manually:** Mike summarizes friction points, surprises, and patterns from this project and feeds them into the infrastructure project's Phase 2 (Characterization System) design.
- **Artifacts do NOT auto-sync between projects:** if a file is updated here, the infrastructure project does not see it, and vice versa. Snapshots are taken at upload time.

---

## 8. Output Standards

Every artifact produced inside this project must be:
- **Markdown** for any Claude-to-Claude artifact (English).
- **Hebrew** for anything Mike or Eliel reads.
- **Self-contained** — readable by a future chat with no prior context.
- **Operational** — every section enables an action or a decision.
- **Eliel-reviewable** for change logs — written so Eliel can scan 50 entries in 10 minutes.
- **Re-runnable** — designed to survive a characterization update without restart.

---

## 9. Document Maintenance

- **Edited by Sensei (Roital)**, with specialist chats writing back into their own domain's docs.
- Docs live in this claude.ai Project's Knowledge — no manual re-upload cycle is required once a doc is written here via `project_write`.
- **This file's twin, `ROITAL_PROJECT_CONTEXT.md.txt`, is superseded** — it now only carries a pointer to this file. Eliel should delete the `.txt` copy manually when convenient (agents cannot delete project docs).

---

## שינויים במסמך הזה — Change Log

| # | מה שונה | מקור |
|---|---|---|
| 1 | ניסיון ליצור מסמך בשם `ROITAL_PROJECT_CONTEXT.md` בשורש נחסם ע"י הכלי — נוצר בפועל תחת `claude/ROITAL_PROJECT_CONTEXT.md`. תועד כהערת מיקום למעלה | מגבלת כלי `project_write`, סקירת 03/08/2026 |
| 2 | תוכן מקורי מ-`ROITAL_PROJECT_CONTEXT.md.txt` (20/05/2026) הועתק ורוכך אל מול `00_PROJECT_CONTEXT.md` המעודכן | סקירת 03/08/2026 |
| 3 | §1 — מסגרת "2.5 שבועות / 90%" סומנה כהיסטורית; הופנתה לסטטוס העדכני ב-`00_PROJECT_CONTEXT.md` §8 (יום רביעי / 60%–40%) | `00_PROJECT_CONTEXT.md` §8 |
| 4 | §2 — נוספה אזהרת "לוודא מי בעל/ת הצ'אט" (chat_23) | `00_PROJECT_CONTEXT.md` §2 |
| 5 | §4 — מספרי ה-template_snapshot (78/2,442/873/707) סומנו כמיושנים; `03_LIVE_FIREBERRY.md` גובר לפי היררכיית `README.md` | `README.md` §היררכיית קדימות |
| 6 | §5 — כלל המחיקות הוחמר מ"אישור לפני הרס" ל"מחיקה ע\"י סוכן אוטונומי אסורה לחלוטין, ידני בלבד" | chat_18 (D5) |
| 7 | §5 — נוספו `DRY_RUN=true` כברירת מחדל, `MAX_PER_RUN`, בדיקת שלילה חובה, ואיסור הדלקת תרחיש לפני בדיקת התור (525 אירועים תקועים) | chat_16, chat_22, chat_26 |
| 8 | §6 — נוסף עוגן לניהול הסטטוס בפועל: ClickUp `86c8zamc2` / `86cawzmjw`, לא מסמכי MD | `00_PROJECT_CONTEXT.md` §11 |
| 9 | §9 — עודכן שאין מחזור העלאה ידני יותר (המסמך חי כ-project doc); נוסף קישור למסמך המצביע `.txt` | סקירת 03/08/2026 |
