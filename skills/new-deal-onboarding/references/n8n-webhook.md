# N8N Workflow Reference — PCFS New Deal GHL Push

This is the N8N workflow that handles the GHL portion of new-deal onboarding. It's a webhook-triggered workflow so the skill can fire it with one HTTP call.

**Workflow ID**: `rwgvg3NFd53pqbdm`
**Workflow Name**: PCFS — New Deal Onboarding (GHL Push)
**Webhook URL**: `https://graehamwatts.app.n8n.cloud/webhook/pcfs-new-deal-ghl`
**Method**: POST
**Auth**: None on webhook (the workflow itself uses GHL OAuth credential `EDW8BCWywlEUrylq`)
**Status**: Created INACTIVE — needs to be activated in N8N before first use.

## Workflow Structure

```
[Webhook Trigger] 
   → [Set: Parse + Normalize Inputs]
   → [HTTP Search GHL by Email]
   → [IF: Contact Exists?]
       ├─ TRUE → [HTTP PUT /contacts/{id}] → [HTTP Set Custom Fields] → [HTTP Add Tags]
       └─ FALSE → [HTTP POST /contacts/] → [HTTP Set Custom Fields] → [HTTP Add Tags]
   → [Respond to Webhook with contactId + status]
```

## Webhook Input Schema

```json
{
  "first_name": "string (required)",
  "last_name": "string (required)",
  "email": "string (required)",
  "phone": "string E.164 (required)",
  "address1": "string (required)",
  "city": "string (required)",
  "state": "string 2-letter (required)",
  "postal_code": "string (required)",
  "coe_date": "string YYYY-MM-DD (required)",
  "buyer_or_seller": "string B|S (required)",
  "buying_address": "string (optional, only if B)",
  "selling_address": "string (optional, only if S)",
  "epa": "string Y|N (optional, default N)",
  "birthday": "string YYYY-MM-DD (optional)",
  "tags_to_add": "array of strings (optional)"
}
```

## Webhook Output Schema

Success:
```json
{
  "ok": true,
  "contactId": "ABC123xyz",
  "operation": "create" | "update",
  "ghlResponse": { /* truncated raw GHL response */ }
}
```

Failure:
```json
{
  "ok": false,
  "error": "error message",
  "stage": "search" | "create" | "update" | "set-fields" | "tags",
  "ghlStatus": 422
}
```

## GHL API Calls (for reference)

### Search by email
```
GET https://services.leadconnectorhq.com/contacts/search/duplicate?locationId=6wuU3haUH7uNeT20E3UZ&email={email}
Authorization: Bearer {accessToken}
Version: 2021-07-28
```

### Create contact
```
POST https://services.leadconnectorhq.com/contacts/
Authorization: Bearer {accessToken}
Version: 2021-07-28
Content-Type: application/json

{
  "locationId": "6wuU3haUH7uNeT20E3UZ",
  "firstName": "...",
  "lastName": "...",
  "email": "...",
  "phone": "...",
  "address1": "...",
  "city": "...",
  "state": "...",
  "postalCode": "...",
  "tags": ["past-client", "buyer", "2026"]
}
```

### Update contact
```
PUT https://services.leadconnectorhq.com/contacts/{contactId}
Authorization: Bearer {accessToken}
Version: 2021-07-28
Content-Type: application/json

{
  "firstName": "...",
  ...
  "customFields": [
    { "id": "MYBybCgfZiUZTl9aSvSd", "value": "2026-04-29" },
    { "id": "aMXm4T9X30OrJmCbFz4l", "value": "123 Main St San Jose CA 95129" }
  ]
}
```

### Add tags (alternative if not in create body)
```
POST https://services.leadconnectorhq.com/contacts/{contactId}/tags
Authorization: Bearer {accessToken}
Version: 2021-07-28
Content-Type: application/json

{ "tags": ["past-client", "buyer", "2026"] }
```

## Why a single webhook workflow?

We considered chaining 3 separate workflows (search → upsert → tag) but a single webhook is cleaner because:
1. Atomic — if anything fails, we know which stage and can return early
2. Single source of truth — one place to debug, one place to update field IDs
3. Faster — no inter-workflow handoff latency

If we ever need to re-use the upsert logic from another flow, we'll extract it to a sub-workflow then.

## Setting It Up (one-time)

To create the workflow in N8N:

1. Use `mcp__n8n-mcp__n8n_create_workflow` or build manually in the N8N UI
2. Create a Webhook trigger, path `pcfs-new-deal-ghl`
3. Add HTTP Request nodes per the structure above
4. Configure GHL OAuth credential (re-use the existing `wIsb5mNoRmq7fh1Q` credential — confirm it has contacts:write scope)
5. Test with the curl payload below
6. Activate the workflow
7. Copy the webhook URL into this file's header

## Test Curl

```bash
curl -X POST https://graehamwatts.app.n8n.cloud/webhook/pcfs-new-deal-ghl \
  -H "Content-Type: application/json" \
  -d '{
    "first_name": "TEST",
    "last_name": "PCFS-Onboard",
    "email": "test-pcfs-onboard@example.com",
    "phone": "+15555550100",
    "address1": "1 Test St",
    "city": "San Jose",
    "state": "CA",
    "postal_code": "95129",
    "coe_date": "2026-04-29",
    "buyer_or_seller": "B",
    "buying_address": "1 Test St San Jose CA 95129",
    "selling_address": "",
    "epa": "N",
    "tags_to_add": ["past-client", "buyer", "2026", "TEST"]
  }'
```

After test runs successfully, delete the test contact from GHL.

## Open Tasks (when wiring this up)

- [ ] Create the workflow in N8N (manual or via MCP)
- [ ] Verify Buying Property Address custom field ID (data-spec.md has placeholder `bGn4kT9X30OrJmCbFz4l` — confirm via /customFields API call)
- [ ] Smoke test with TEST payload
- [ ] Delete TEST contact
- [ ] Update the workflow ID + webhook URL in SKILL.md once active
