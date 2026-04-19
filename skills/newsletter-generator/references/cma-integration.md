# CMA Integration — How the Newsletter Triggers a CMA

The **"What's My Home Worth?"** CTA in every newsletter is the primary conversion action. This document specifies how it connects to the `cma-generator` skill.

## Current State (Manual — Ships Today)

### CTA Button Wiring
```html
<a href="https://graehamwatts.com/home-value?utm_source=newsletter&utm_campaign=[slug]&utm_medium=email"
   style="background:#C5A258;color:#1B2A4A;padding:16px 32px;border-radius:8px;font-weight:800;text-decoration:none;display:inline-block">
   What's My Home Worth?
</a>
```

### End-to-End Flow

1. **Click:** User clicks the CTA in the newsletter.
2. **Landing:** Lands on `graehamwatts.com/home-value` — a GHL-hosted form with fields: name, email, phone, property address, optional notes.
3. **Form submit:** GHL workflow captures the lead as a new contact, tags them with `NEWSLETTER_VALUE_REQUEST`.
4. **Notification:** GHL sends Graeham an SMS + email with the submitter's address.
5. **Manual CMA:** Graeham invokes the `cma-generator` skill with the address:
   ```
   "Generate a CMA for 1234 Example Ave, East Palo Alto CA 94303"
   ```
6. **CMA generates:** The skill pulls comps from MLS, produces Interactive HTML + Email-Safe HTML + PDF formats.
7. **Auto-publish:** CMA HTML auto-publishes to `https://graehamwatts.github.io/cma-reports/CMA_[address].html` via the GitHub Contents API call documented in `cma-generator/references/github_publishing.md`.
8. **Delivery:** Graeham sends the lead the CMA URL with a personalized intro via Gmail (optionally using Gmail MCP).

### Why this is the right current-state flow
- Maintains human quality control on comp selection (agent judgment on which comps are truly comparable)
- Allows Graeham to write a personalized intro that builds relationship
- Gives Graeham the chance to catch weird addresses or obvious fit issues before sending
- Already works — no additional infra to build

---

## Future Auto-Chain (Not Yet Built)

### Goal
When a newsletter reader submits their address, they get a CMA URL in their inbox within 10 minutes — no manual step.

### Required Infrastructure

**1. GHL webhook trigger**
- When the form submits on `graehamwatts.com/home-value-instant`, fire a webhook.
- Webhook target: n8n workflow on Graeham's n8n instance (or Cloudflare Worker, or AWS Lambda).

**2. n8n workflow: `newsletter-cma-autochain`**
- Receives webhook with `{name, email, phone, address, slug}` payload.
- Validates address (must be a real property; dedupe check).
- Invokes the cma-generator via subprocess OR calls an endpoint that wraps it.
- Publishes the CMA HTML to `graehamwatts.github.io/cma-reports/` (existing flow).
- Sends the lead an auto-email via Gmail API:
  - Subject: "Your [City] home value report is ready — [Address]"
  - Body: Brief personal-feel intro + CMA URL + callback CTA
- Notifies Graeham in Slack / SMS with the lead details + CMA URL so he can follow up personally within 24 hours.

**3. Quality control**
- Log every auto-run to a Google Sheet (or Airtable) with: timestamp, address, lead email, CMA URL, any errors.
- Slack alert if any auto-run fails (e.g., MLS pull times out, address unparseable).
- Rate limit: max 5 auto-runs per hour to prevent MLS account getting flagged.

**4. Fallback path**
- If auto-run fails, fall back to manual flow: GHL notifies Graeham, flow continues as Current State.
- User never sees the failure — just a "thanks, we'll send your report shortly" message on form submit.

### Estimated Build Time
- n8n workflow: 2-3 hours
- Testing + edge cases: 2 hours
- GHL form + landing page: 1 hour
- Total: **~5 hours for complete auto-chain**

### When to Build This
Build when Graeham is getting 5+ home-value form submits per week. Below that threshold, manual quality control is higher ROI than automation.

---

## Newsletter Template Button Spec

Use this exact HTML in the newsletter CTA block:

```html
<table role="presentation" cellspacing="0" cellpadding="0" border="0" align="center" style="margin:32px auto">
  <tr>
    <td style="background:#C5A258;border-radius:8px;padding:16px 32px;text-align:center">
      <a href="https://graehamwatts.com/home-value?utm_source=newsletter&utm_campaign={{slug}}&utm_medium=email&utm_content=home_value_cta"
         style="color:#1B2A4A;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif;font-size:16px;font-weight:800;letter-spacing:0.3px;text-decoration:none;display:inline-block">
        What's My Home Worth?
      </a>
    </td>
  </tr>
</table>
<p style="text-align:center;font-size:12px;color:#666;margin-top:8px">
  Free, accurate, neighborhood-specific. Delivered by a licensed REALTOR — not an algorithm.
</p>
```

Replace `{{slug}}` with the newsletter's topic slug for campaign tracking (e.g., `epa-two-years-homicide-free`).

## Tracking Parameters

Every CTA link includes:
- `utm_source=newsletter` — identifies the source
- `utm_campaign=[slug]` — identifies which newsletter (for conversion attribution)
- `utm_medium=email` — identifies channel
- `utm_content=home_value_cta` — identifies which button within the newsletter

These parameters flow into GHL via the hidden-field capture on the form, so Graeham can see which newsletter drove which conversions.

## GHL Keyword Mapping

Newsletter CTAs use GHL keyword **`VALUE`** — pre-configured to:
- Tag the contact `NEWSLETTER_VALUE_REQUEST`
- Enroll in the "Home Value Follow-Up" sequence (3-email drip over 7 days)
- Notify Graeham immediately

## Testing Checklist Before Sending a Newsletter

- [ ] CTA URL includes correct `{{slug}}` replacement
- [ ] CTA button renders in Gmail, Apple Mail, Outlook (test in all 3)
- [ ] Form at `https://graehamwatts.com/home-value` is live and accepting submissions
- [ ] GHL `NEWSLETTER_VALUE_REQUEST` tag is active
- [ ] Tracking params flow through to GHL form fields
- [ ] Graeham receives the SMS + email notification on test submission
