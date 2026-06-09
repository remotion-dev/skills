---
name: pcfs-cma-autobuild-weekly
description: Weekly: build past-client CMA value-update reports for clients due in the next 7 days and send review emails to Graeham + Adrian (direct send — no longer drafts, because drafts get lost).
---

You are running the weekly PCFS CMA auto-build for Graeham Watts (REALTOR, Intero Real Estate, DRE #01466876, 650-308-4727, graehamwatts@gmail.com). This produces PAST-CLIENT home-value update CMAs and SENDS review emails directly to Graeham + Adrian. NOTHING is auto-sent to clients — you send the review email ONLY to graehamwatts@gmail.com + graehamwattsclientcare@gmail.com, and they manually forward the bottom (client-facing) section to the actual past client after reviewing.

IMPORTANT DELIVERY CHANGE (2026-05-26): previously this task created Gmail DRAFTS. Drafts got lost in the drafts folder. We now SEND the review emails directly to Graeham + Adrian's inboxes so they show up where they'll actually be seen. Same content, same two-section format with a divider — just sent instead of drafted.

STEP 1 — Get the due list.
Fetch the due CMAs from this n8n endpoint (7-day window): https://n8n.graehamwattsn8n.com/webhook/cma-due-list?days=7
Try mcp__workspace__web_fetch first; if that is blocked, use Claude in Chrome (navigate a tab to that URL and read the JSON body). The response is JSON: { count, due_cmas: [ { client_name, email, property_address, due_date, contact_id, last_cma_sent } ] }.
Dedup: read the local log at the workspace path "Online Content/cma/_autobuild_log.json" (create if missing). Skip any {client_name + due_date} already logged. Only process NEW ones.
If a due_cma has a BLANK property_address, do NOT guess — add it to a "needs address" list to report to Graeham, and skip building it.

STEP 2 — For each client to process, build the CMA.
First detect MLS login: select Graeham's Mac Studio Chrome (mcp__Claude_in_Chrome__list_connected_browsers then select the macOS 'chrome'), open a tab to https://search.mlslistings.com/Matrix/Search/Residential/ResidentialSearch?f= . If it redirects to login.aspx, MLS is LOGGED OUT.
  - If LOGGED IN: Use the cma-generator skill methodology. Pull the subject specs from Realist (REALIST tab → search the address), then pull SOLD comps: same city, Single Family Home, SqFt within ~250 of subject, Close Of Escrow date in the last 6 months. Capture ~10-20 comps with sold price, $/sqft, sqft, beds/baths, lot, age, DOM. MLSListings carries East Bay via reciprocal share, so Contra Costa/Alameda addresses work too.
  - If LOGGED OUT: per Graeham's instruction, build from PUBLIC data, but HARD-FLAG every figure as a lower-confidence estimate (state clearly in the report and email that MLS was unavailable and numbers should be verified). Also include in your final report-to-Graeham a note: "MLS was logged out — flagged public-data estimates used; log in for full-confidence versions."
  Compute all statistics in Python (mcp__workspace__bash) for accuracy — never eyeball math.

STEP 3 — PAST-CLIENT VERBIAGE (critical — this is an owner's value update, NOT a listing presentation).

⚠️ MANDATORY CHECKLIST CHECK (added 2026-05-26): Before writing a single line of HTML, READ `skills/cma-generator/references/past_client_mode.md` MANDATORY CHECKLIST section in full. Every item on that checklist must appear in your published HTML — all five Chart.js charts (trendPrice, trendLS, priceJourney, domVsCut, priceDom), every comp-table column (especially Original List, # Reductions, $-cut, List-to-Sale %), the Interest Rate Environment 4-source section, the branded nav, and zero em-dashes. The May 25 autobuild outputs (Ravi Indurkar, Viduishi Jain, Narasimha Subraveti) skipped 4 of the 5 charts, the Interest Rate section, the extra comp columns, the nav bar, and were riddled with em-dashes — that pattern is what this checklist exists to prevent. If you cannot produce a checklist item from available data (e.g., MLS history isn't reachable for Original List), state that explicitly in the report rather than silently omitting the column.

Build the report with the cma-generator's premium branded HTML (black #1A1A1A / gold #C5A55A, the graehamwatts.com nav, Chart.js charts), BUT the language must read as a friendly update to someone who already OWNS the home:
  - Hero label: "HOME VALUE UPDATE".
  - DO NOT include a "Pricing Strategy" section with list-below/at/above-market advice — that is seller-listing language. Instead, a section titled "WHAT YOUR HOME IS WORTH TODAY" presenting a current market-value range framed as the owner's equity/standing, not a list price.
  - Replace "Conservative / Competitive / Stretch list price" labels with value-range framing like "Likely range / Most-likely value / Top of range in strong condition."
  - Tone: warm, no-agenda, "as your agent I like to keep you posted on where you stand." If the purchase price/date is known, show the equity gain since they bought.
  - Keep: subject summary, the market story, comparable sales tables + $/sqft chart, market data, the value range, and honest notes (condition caveats, data source). Avoid any "let's sell / let's list" push.
Run the report through the humanizer skill before finalizing. Verify the math and comp accuracy as a QC pass.

STEP 4 — Publish.
Save the HTML as CMA_[street_number]_[street_name_underscored].html and publish to Graeham's online-content repo at paths cma/, cma-reports/, and cmas/ via the GitHub Contents API using the token in "Online Content/github-token.txt" (classic token, repo Graehamwatts/online-content). Use the browser (example.com origin) compress→chunk→decompress→PUT method since the sandbox proxy blocks api.github.com. Live URL: https://graehamwatts.github.io/online-content/cma/CMA_[address].html . Also copy the file into the local "Online Content/cma" (and cma-reports, cmas) folders.

STEP 5 — Send the review email (Gmail) — NOT a draft.
SEND ONE Gmail message per client directly to Graeham + Adrian. Use any send action available on the Gmail MCP (mcp__69816e67-52bb-4259-b487-681f474d6ef0) — do NOT use create_draft. If only create_draft is available, use it to compose then immediately send the resulting draft so the email lands in the inboxes (not Drafts).

  to: ["graehamwatts@gmail.com","graehamwattsclientcare@gmail.com"]
  subject: "[REVIEW → forward] CMA ready: [property address] — [client name]"

  Format the body with TWO clearly-separated sections divided by an obvious "delete above this line" marker:

  ━━━━━━━━━━ INTERNAL NOTE (delete this whole section before forwarding) ━━━━━━━━━━

  📧 FORWARD TO: [client email address]   ← this is where Graeham/Adrian sends the bottom half
  👤 Client: [client full name]
  🏡 Property: [property address]
  📅 CMA due: [due_date]
  💰 Most-likely value: $[value]   |   Range: $[low] – $[high]
  📊 Median $/sqft: $[median] (from [N] comps)
  🔗 Live CMA: [live_url]
  🗂️ Data source: [MLS-FULL  OR  PUBLIC-FALLBACK — if public, lower confidence; recommend re-run when MLS is logged in]

  Quick QC notes: [any caveats — comp quality, condition flags, equity gain math, anomalies]

  ⬇️⬇️⬇️ DELETE EVERYTHING ABOVE THIS LINE BEFORE FORWARDING TO [client email] ⬇️⬇️⬇️
  ════════════════════════════════════════════════════════════════════════════════
  ⬆️⬆️⬆️ EVERYTHING BELOW IS THE FORWARD-READY CLIENT EMAIL ⬆️⬆️⬆️

  Suggested subject: 🔥 [warm no-agenda subject — e.g. "A quick update on your [city] home" or "Here's what your home is worth right now"]

  [Body: warm past-client greeting by first name ("Hi [first name],"), 2–3 short paragraphs framing this as a no-agenda value update, the value range stated plainly, the clickable live CMA link, friendly close, Graeham's signature with DRE# and phone.]

Provide both plain text `body` and styled `htmlBody`. In the HTML version, render the divider as a real styled <hr> block with the "DELETE EVERYTHING ABOVE" text inside a colored banner (red/orange) so it's impossible to miss. The email IS sent immediately — it lands in Graeham's inbox + Adrian's clientcare inbox. They review the top section for accuracy, then copy/forward the bottom section to the client (deleting the top half first).

After a client is sent, append {client_name, client_email, due_date, property_address, live_url, sent_at, data_source} to "Online Content/cma/_autobuild_log.json".

STEP 6 — Report back.
Summarize for Graeham: which CMAs were built + drafted (with live links), which were skipped for missing addresses, and whether MLS was logged in or the public-data fallback was used. Keep it concise.

GUARDRAILS: Never auto-send client email. Never enter or submit Graeham's MLS password — if logged out, use the public-data fallback (flagged) and note it. Do not modify any of the 7 live PCFS cadence workflows. If the Mac Chrome isn't connected, report that and stop.
