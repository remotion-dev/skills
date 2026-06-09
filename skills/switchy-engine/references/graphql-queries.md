# Switchy GraphQL & REST — raw queries

All GraphQL calls: `POST https://graphql.switchy.io/v1/graphql`, header
`Api-Authorization: <token>`. Queries only — there are no GraphQL mutations.

## 0. Smoke test (confirms token is active)
Matches the documented example. If this returns your workspace, the token works.
```graphql
query SmokeTest {
  workspaces { id name companyName createdDate }
  domains(where: { removedDate: { _is_null: true } }) { name createdDate }
}
```
If it returns `errors` or empty, the token likely needs API access enabled via
Switchy live chat.

## 1. Confirm the per-link field names (MANDATORY before analytics)
The public docs never document per-link analytics fields. Introspect them:
```graphql
query ConfirmLinksType {
  __type(name: "links") {
    name
    fields { name description type { name kind ofType { name kind } } }
  }
}
```
Scan the output for the click/scan counter. Likely candidates given the Hasura
schema: a scalar like `clicks` / `clicksCount` / `visits`, OR a relationship
exposed as `clicks_aggregate { aggregate { count } }`. **Do not assume — confirm.**
If `links` isn't the type name, run full introspection:
```graphql
query { __schema { queryType { name } types { name kind } } }
```

## 2. Per-link analytics — scalar-count shape (try first)
Replace `clicks` with whatever step 1 revealed.
```graphql
query LinkAnalytics {
  links(where: { removedDate: { _is_null: true } }) {
    id            # this is the slug (domain/id is the short URL)
    domain
    url           # destination
    title
    tags
    clicks        # <-- VERIFY this field name via introspection
  }
}
```

## 3. Per-link analytics — aggregate shape (fallback)
If clicks live in a child table (Hasura exposes `<rel>_aggregate`):
```graphql
query LinkAnalyticsAggregate {
  links(where: { removedDate: { _is_null: true } }) {
    id domain url title tags
    clicks_aggregate { aggregate { count } }
  }
}
```
`scripts/switchy_analytics.py` tries shape #2 then falls back to #3 automatically.

## 4. Time-windowed clicks (if a clicks/events table exists)
Once introspection reveals the events table + its timestamp column, filter by date
for week-over-week reporting (column names are placeholders — confirm them):
```graphql
query ClicksLast30d($since: timestamptz!) {
  links(where: { removedDate: { _is_null: true } }) {
    id domain
    clicks_aggregate(where: { createdDate: { _gte: $since } }) {
      aggregate { count }
    }
  }
}
```

## 5. Creating a tracked, pixeled link (REST — not GraphQL)
```bash
curl 'https://api.switchy.io/v1/links/create' \
  -H 'Content-Type: application/json' \
  -H 'Api-Authorization: YOUR_TOKEN' \
  -d '{
    "link": {
      "url": "https://graehamwatts.com/home-value",
      "domain": "hi.switchy.io",
      "id": "epa-report",
      "title": "EPA Report CTA",
      "tags": ["newsletter","consumer"],
      "pixels": [
        { "platform": "facebook", "value": "FB_PIXEL_ID" },
        { "platform": "ga",       "value": "G-XXXXXXX" }
      ],
      "showGDPR": true
    },
    "autofill": true
  }'
```
- `pixels[].platform` ∈ {linkedin, facebook, gtm, quora, pinterest, twitter, ga,
  bing, nexus, adroll, adwords}. **No tiktok** — route TikTok via `gtm`.
- `showGDPR: true` shows a consent popup when pixels are present. In CA, leaving it
  true is the safer default for cold consumer traffic; it slightly reduces match
  rate. Decision flagged for Graeham.
- Premium domains `hi.switchy.io` / `swiy.io` are only available to *official*
  integrations via API; your default workspace domain is used otherwise.
- QR codes: Switchy generates a QR for any link in-app. Via API, generate the link
  then render the QR client-side (any QR lib encoding the short URL), or export
  from the Switchy dashboard. A QR scan = a click = a pixel fire on redirect.

## Notes
- `id` in the link object IS the slug; the public short URL is `domain/id`.
- Always pass `tags` — the analytics + audience-hygiene layer segments on them.
