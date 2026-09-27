// ============================================================
//  dash-api - auth + compact dataset for the Revital dashboard
//  No Fireberry token ever reaches the browser. Read-only,
//  except admin_update_coaching (explicit write, admin-token gated).
//  Snapshot mode: the dataset is prebuilt after every sync, gzipped,
//  stored in the private bucket "dash-private" and served by signed URL.
// ============================================================
import { createClient } from "jsr:@supabase/supabase-js@2";
import { gzipSync, strToU8 } from "npm:fflate@0.8.2";

const enc = new TextEncoder();
const hex = (b: ArrayBuffer) => Array.from(new Uint8Array(b)).map((x) => x.toString(16).padStart(2, "0")).join("");
async function sha256(s: string) { return hex(await crypto.subtle.digest("SHA-256", enc.encode(s))); }
async function hmac(secret: string, msg: string) {
  const k = await crypto.subtle.importKey("raw", enc.encode(secret), { name: "HMAC", hash: "SHA-256" }, false, ["sign"]);
  return hex(await crypto.subtle.sign("HMAC", k, enc.encode(msg)));
}

const CORS = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type, x-dash-token, x-admin-token, x-sync-secret",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { ...CORS, "Content-Type": "application/json" } });

const SNAP_BUCKET = "dash-private";
const SNAP_PATH = "snapshot.json.gz";
const COACHING_COLS = "id,name,createdon,status,status_label,account_id,account_name,ownerid,ownername,product_id,product_name,program,program_label,cont_status,cont_status_label,satisfaction,satisfaction_label,start_date,est_end_date,premium_end_date,initial_weight,current_weight,target_weight,weeks_number,current_week,weigh_count,last_weigh_date,meetings_total,meetings_done,distance_to_goal,group_id,group_name,cycle_name,watched_zoom_label";

// deno-lint-ignore no-explicit-any
type Row = Record<string, any>;
// deno-lint-ignore no-explicit-any
async function buildDataset(db: any, forSnapshot: boolean) {
  const all = async (t: string, cols: string) => {
    const out: Row[] = [];
    for (let from = 0; ; from += 1000) {
      const r = await db.from(t).select(cols).order(cols.split(",")[0]).range(from, from + 999);
      if (r.error) throw new Error(t + ": " + r.error.message);
      out.push(...(r.data as Row[]));
      if ((r.data?.length ?? 0) < 1000) break;
    }
    return out;
  };
  const none = async () => [] as Row[];
  const [users, products, sources, campaigns, groups, catalog, leads, opps, coaching, weighins, menus, cycles, events, regs, orders, payments, paydocs, camDaily, snaps, syncState, syncLog, accounts0] = await Promise.all([
    all("fb_user", "id,name,statuscode"),
    all("fb_product", "id,name,product_type,product_type_label,price,duration_weeks"),
    all("fb_utm_source", "id,name"),
    all("fb_campaign", "id,name"),
    all("fb_wa_group", "id,name,capacity,current_count,available,status_label,program_label,ownername"),
    all("fb_menu_catalog", "id,name,category_label,menu_type_label,calories"),
    // leads are not used by any board (the marketing board counts from sale processes) - skipped in snapshots
    forSnapshot ? none() : all("fb_lead", "id,createdon,record_type,utm_source_id,utm_source_name,utm_campaign_id,utm_campaign_name,utm_adset_name,ownername"),
    all("fb_opportunity", "id,name,createdon,statuscode,status_label,ownerid,ownername,product_id,product_name,utm_source_name,utm_campaign_name,cycle_id,cycle_name,cashflow,revenue,closedate,dayspast,last_entry,legacy_crm_created_on,account_id"),
    all("fb_coaching", COACHING_COLS),
    all("fb_weighin", "id,weight,week_index,weigh_date,change_from_start,weight_delta,coaching_id,coaching_name,ownername"),
    all("fb_menu_alloc", "id,name,createdon,menu_type,menu_type_label,menu_status,menu_status_label,dietitian_id,dietitian_name,fee,paid_status,paid_status_label,paid_date,sent_ts,send_time,msg_sent,valid_to,coaching_id,coaching_name,catalog_id,catalog_name"),
    all("fb_cycle", "id,name,status,status_label,start_date,end_date,product_id,product_name,event_link,quota,registered,w_registered,w_attended,w_completed,w_attend_rate,w_complete_rate,w_avg_min,w_median_min,w_peak,w_drop_min,w_qa,w_duration_min"),
    all("fb_event", "id,name,status_label,event_type_label,start_date,quota,registered,product_name"),
    all("fb_event_reg", "id,status,status_label,event_id,event_name,createdon"),
    all("fb_order", "id,name,createdon,statuscode,status_label,ownername,product_name,total,collected,balance,closedate"),
    all("fb_payment", "id,name,createdon,status_label,pay_type,pay_type_label,need_to_pay,need_to_pay_pre_vat,total_paid,left_to_pay,num_payments,first_pay,last_pay,sale_id,legacy_created_on"),
    all("fb_payment_doc", "id,pay_status,pay_status_label,pay_type,pay_type_label,amount,amount_pre_vat,pay_date,sale_id,payment_collection_id"),
    all("fb_campaign_daily", "id,the_date,campaign_name,spent,clicks,impressions,cpc,cpm,ctr,conversions"),
    all("fact_daily_snapshot", "snap_date,metrics"),
    all("sync_state", "object_type,object_label,record_count,last_run_at"),
    db.from("sync_log").select("started_at,finished_at,api_calls,records_upserted,status,error,trigger_type").order("started_at", { ascending: false }).limit(5).then((r: Row) => r.data ?? []),
    all("fb_account", "id,name,phone"),
  ]);
  // phones are only needed for clients that have a coaching record (board 6)
  let accounts = accounts0;
  if (forSnapshot) { const ids = new Set(coaching.map((c: Row) => c.account_id)); accounts = accounts0.filter((a: Row) => ids.has(a.id)); }
  return {
    ok: true, generated_at: new Date().toISOString(),
    sync: { state: syncState, log: syncLog },
    users, products, sources, campaigns, groups, catalog,
    leads, opps, coaching, weighins, menus, cycles, events, regs, orders, payments, paydocs,
    campaign_daily: camDaily, snapshots: snaps, accounts,
  };
}

// column-oriented encoding: {c:[cols], r:[[...],...]} - the browser decodes back to objects
const compactTable = (rows: Row[]) => { const c = rows.length ? Object.keys(rows[0]) : []; return { c, r: rows.map((o) => c.map((k) => o[k] ?? null)) }; };
const COMPACT = ["opps", "coaching", "paydocs", "payments", "accounts", "weighins", "menus", "cycles"];

const gzip = (s: string) => gzipSync(strToU8(s), { level: 6 });

Deno.serve(async (req) => {
  if (req.method === "OPTIONS") return new Response("ok", { headers: CORS });

  const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!, { auth: { persistSession: false } });
  const cfgRows = await db.from("app_config").select("key,value");
  const cfg: Record<string, string> = {};
  for (const r of cfgRows.data ?? []) cfg[r.key] = r.value;

  let body: Record<string, unknown> = {};
  try { body = await req.json(); } catch (_e) { /* ok */ }
  const action = String(body.action ?? "data");

  if (action === "login") {
    const pw = String(body.password ?? "");
    const got = await sha256(cfg.auth_salt + pw);
    if (got !== cfg.auth_sha256) { await new Promise((r) => setTimeout(r, 900)); return json({ error: "bad_password" }, 401); }
    const exp = Date.now() + 12 * 3600 * 1000;
    return json({ token: exp + "." + (await hmac(cfg.sync_secret, String(exp))), expires: exp });
  }

  // ---------- snapshot build: called by fb-sync after every run ----------
  if (action === "build_snapshot") {
    if (req.headers.get("x-sync-secret") !== cfg.sync_secret) return json({ error: "unauthorized" }, 401);
    const t0 = Date.now();
    const ds: Row = await buildDataset(db, true);
    console.log("snapshot: queried", Date.now() - t0);
    const builtAt = ds.generated_at as string;
    for (const k of COMPACT) ds[k] = compactTable(ds[k]);
    ds.compact = COMPACT;
    let raw: string | null = JSON.stringify(ds);
    const rawLen = raw.length;
    console.log("snapshot: stringified", Date.now() - t0, rawLen);
    const gz = gzip(raw); raw = null;
    console.log("snapshot: gzipped", Date.now() - t0, gz.length);
    const up = await db.storage.from(SNAP_BUCKET).upload(SNAP_PATH, gz, { contentType: "application/octet-stream", upsert: true });
    console.log("snapshot: uploaded", Date.now() - t0, up.error?.message ?? "ok");
    if (up.error) return json({ error: "upload: " + up.error.message }, 500);
    await db.from("app_config").upsert([{ key: "snapshot_version", value: builtAt }], { onConflict: "key" });
    return json({ ok: true, version: builtAt, raw_bytes: rawLen, gz_bytes: gz.length, ms: Date.now() - t0 });
  }

  // ---------- admin: separate password gate for בקרת נציגים ----------
  if (action === "admin_login") {
    const pw = String(body.password ?? "");
    const got = await sha256(cfg.admin_auth_salt + pw);
    if (got !== cfg.admin_auth_sha256) { await new Promise((r) => setTimeout(r, 900)); return json({ error: "bad_password" }, 401); }
    const exp = Date.now() + 12 * 3600 * 1000;
    return json({ admin_token: exp + "." + (await hmac(cfg.sync_secret + ":admin", String(exp))), expires: exp });
  }

  if (action === "admin_update_coaching") {
    const at = req.headers.get("x-admin-token") ?? String(body.admin_token ?? "");
    const [aExpS, aSig] = at.split(".");
    const aExpN = Number(aExpS);
    if (!aExpN || !aSig || aExpN < Date.now() || (await hmac(cfg.sync_secret + ":admin", aExpS)) !== aSig) return json({ error: "unauthorized" }, 401);

    const coachingId = String(body.coaching_id ?? "");
    if (!/^[0-9a-fA-F-]{36}$/.test(coachingId)) return json({ error: "bad_coaching_id" }, 400);
    const fields: Record<string, unknown> = {};
    if (body.ownerid !== undefined) fields.ownerid = body.ownerid === null ? null : String(body.ownerid);
    if (body.group_id !== undefined) fields.pcfActualGroup = body.group_id === null ? null : String(body.group_id);
    if (Object.keys(fields).length === 0) return json({ error: "no_fields" }, 400);

    const cur = await db.from("fb_coaching").select("ownerid,group_id").eq("id", coachingId).maybeSingle();
    if (cur.error || !cur.data) return json({ error: "coaching_not_found" }, 404);

    const res = await fetch(`https://api.fireberry.com/api/record/1051/${coachingId}`, {
      method: "PUT",
      headers: { "tokenid": cfg.fireberry_token, "Content-Type": "application/json" },
      body: JSON.stringify(fields),
    });
    if (!res.ok) {
      const txt = await res.text();
      return json({ error: "fireberry_write_failed", detail: txt.slice(0, 500) }, 502);
    }

    const logs = [];
    if (body.ownerid !== undefined) logs.push({ coaching_id: coachingId, field: "ownerid", old_value: cur.data.ownerid, new_value: body.ownerid });
    if (body.group_id !== undefined) logs.push({ coaching_id: coachingId, field: "group_id", old_value: cur.data.group_id, new_value: body.group_id });
    if (logs.length) await db.from("admin_change_log").insert(logs);

    const now = new Date().toISOString();
    if (body.ownerid !== undefined) await db.from("fb_coaching").update({ ownerid: body.ownerid, ownername: body.ownername ?? null, local_edit_at: now }).eq("id", coachingId);
    if (body.group_id !== undefined) await db.from("fb_coaching").update({ group_id: body.group_id, group_name: body.group_name ?? null, local_edit_at: now }).eq("id", coachingId);

    return json({ ok: true });
  }

  const tok = req.headers.get("x-dash-token") ?? String(body.token ?? "");
  const [expS, sig] = tok.split(".");
  const expN = Number(expS);
  if (!expN || !sig || expN < Date.now() || (await hmac(cfg.sync_secret, expS)) !== sig) return json({ error: "unauthorized" }, 401);

  // ---------- sync: fire and forget, UI polls syncstatus ----------
  if (action === "sync") {
    const last = await db.from("sync_log").select("id,started_at,finished_at").order("started_at", { ascending: false }).limit(1).maybeSingle();
    const lastAt = last.data?.started_at ? new Date(last.data.started_at).getTime() : 0;
    if (last.data && !last.data.finished_at && Date.now() - lastAt < 5 * 60 * 1000) return json({ ok: true, already_running: true, log_id: last.data.id });
    if (Date.now() - lastAt < 3 * 60 * 1000) return json({ ok: false, cooldown: true, seconds: Math.ceil((3 * 60 * 1000 - (Date.now() - lastAt)) / 1000) });
    const p = fetch(Deno.env.get("SUPABASE_URL")! + "/functions/v1/fb-sync", {
      method: "POST", headers: { "x-sync-secret": cfg.sync_secret, "Content-Type": "application/json" },
      body: JSON.stringify({ trigger: "manual-ui" }),
    }).catch(() => {});
    // deno-lint-ignore no-explicit-any
    const rt = (globalThis as any).EdgeRuntime;
    if (rt && typeof rt.waitUntil === "function") rt.waitUntil(p);
    await new Promise((r) => setTimeout(r, 1200));
    return json({ ok: true, started: true });
  }

  if (action === "syncstatus") {
    const r = await db.from("sync_log").select("id,started_at,finished_at,api_calls,records_upserted,status,error,trigger_type").order("started_at", { ascending: false }).limit(1).maybeSingle();
    return json({ ok: true, log: r.data ?? null });
  }

  // ---------- dataset, snapshot mode ----------
  if (body.mode === "snapshot" && cfg.snapshot_version) {
    const version = cfg.snapshot_version;
    // edits made from board 6 after the snapshot was built
    const pr = await db.from("fb_coaching").select(COACHING_COLS).gt("local_edit_at", version);
    const patch = { coaching: pr.data ?? [] };
    if (body.have === version) return json({ ok: true, unchanged: true, version, patch });
    const signed = await db.storage.from(SNAP_BUCKET).createSignedUrl(SNAP_PATH, 120);
    if (signed.error || !signed.data?.signedUrl) return json({ error: "signed_url: " + (signed.error?.message ?? "none") }, 500);
    return json({ ok: true, version, url: signed.data.signedUrl, patch });
  }

  // ---------- dataset, live (fallback / legacy clients) ----------
  try {
    return json(await buildDataset(db, false));
  } catch (e) {
    return json({ error: String(e) }, 500);
  }
});
