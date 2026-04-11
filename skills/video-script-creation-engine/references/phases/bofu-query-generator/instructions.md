---
name: bofu-query-generator
description: Generates a comprehensive, localized list of BOFU search queries for real estate content research. Use this skill when the BOFU Video Engine needs to produce search queries for a specific market. This skill takes a market config as input and outputs a structured query list organized by audience, inquiry type, and geographic scope. It does NOT run the searches — it only generates the queries. Trigger when the orchestrator calls for query generation, or when the user asks to "generate queries," "build the query list," or "create search queries" for their market.
---

# BOFU Query Generator

You generate localized search queries for real estate BOFU content research. Your job is to take a member's market config and produce a comprehensive list of queries the BOFU Video Engine will search.

Read the market config at `../../references/market-config.md` before generating any queries (top-level references folder shared across all skills). Every query must be adapted to the member's location, audience, property types, and process terminology. If you cannot access this file path, use the market context provided in the kickoff prompt and your system prompt instead.

**Graeham's default market context:** If no market is specified, default to his primary Bay Area markets: East Palo Alto (EPA — home base), Redwood City (RWC), Palo Alto (PA), Menlo Park (MP), and San Mateo County. Brand positioning is **Bay Area first** with EPA as the deepest local expertise area. See the full config for neighborhoods, secondary markets, and expandable markets.

---

## Geographic Variables

Queries should use the appropriate geographic level for each question type. The config provides:

- **City** — for market-level and general process queries
- **State/Province** — for legal, tax, and regulatory process queries
- **County/Region** — for tax rates, transfer taxes, and jurisdiction-specific questions
- **Metro Area** — as a fallback when local search data is thin
- **Neighborhoods** — for hyperlocal property and market queries

Use the most specific geographic level that fits the query. Tax questions use county. Legal process questions use state/province. Market and pricing questions use city. Property and development questions use neighborhood.

---

## Output Format

Organize the query list into sections. Output as a structured list the orchestrator can work through systematically:

```
## SELLER QUERIES

### Cost & Financial
- [query 1]
- [query 2]
...

### Timing & Seasonal
...

### Preparation & Pricing
...

### Process & What-Happens-Next
...

### Situational & Emotional
...

## BUYER QUERIES

### Cost & Financial
...

(etc.)
```

---

## Query Patterns

Generate queries dynamically by combining the patterns below with the member's localized variables. Do not output these literally — inject the real city, state/province, county/region, neighborhoods, and process terms from the config.

### SELLER — Cost & Financial

- "how much does it cost to sell a house in [CITY]"
- "closing costs for sellers in [CITY] [STATE/PROVINCE]"
- "how much are [TRANSFER_TAX_TERM] in [COUNTY/REGION]"
- "seller closing costs [CITY] [STATE/PROVINCE]"
- "how much will I net selling my house in [CITY]"
- "realtor commission [CITY] [STATE/PROVINCE]"
- "who pays closing costs in [STATE/PROVINCE]"
- "cost to sell a house in [STATE/PROVINCE] breakdown"
- "capital gains tax selling house [STATE/PROVINCE]"
- "do I have to pay buyer's agent commission [STATE/PROVINCE]"
- "how much does staging cost [CITY]"
- "is it worth paying for professional photos to sell my house"
- "average cost of home inspection for seller [CITY]"
- "how much does it cost to break a lease to sell [STATE/PROVINCE]"
- "what fees do sellers pay at closing [STATE/PROVINCE]"

### SELLER — Timing & Seasonal

- "should I sell my house this spring [CITY]"
- "best time to sell a house in [CITY] [STATE/PROVINCE]"
- "when should I list my house [CITY]"
- "how long does it take to sell a house in [CITY]"
- "is now a good time to sell in [CITY]"
- "should I wait to sell my house [CITY]"
- "spring vs fall selling [CITY]"
- "how long does closing take in [STATE/PROVINCE]"
- "how quickly can I sell my house [CITY]"
- "when should I start preparing my house to sell"
- "should I sell before the holidays [CITY]"
- "how far in advance should I contact an agent before selling"

### SELLER — Preparation & Pricing

- "how to prep my home for sale [CITY]"
- "how should I price my home [CITY]"
- "should I renovate before selling [CITY]"
- "what repairs should I make before selling"
- "is it worth replacing carpet before selling"
- "should I paint my house before selling"
- "how to stage a house to sell [CITY]"
- "should I get a pre-listing inspection [CITY]"
- "what home improvements add the most value [CITY]"
- "curb appeal tips to sell house faster"
- "should I replace the roof before selling"
- "is it worth updating the kitchen before selling"
- "what not to fix when selling a house"
- "how do I price my home competitively [CITY]"
- "overpriced house not selling [CITY]"
- "how to determine asking price [CITY]"
- "should I price above or below market value"
- "what is a comparative market analysis [CITY]"
- "Zestimate vs actual home value [CITY]"
- "assessed value vs market value [CITY]"

### SELLER — Process & What-Happens-Next

- "what happens after I accept an offer [STATE/PROVINCE]"
- "what happens at closing for the seller [STATE/PROVINCE]"
- "steps to selling a house in [STATE/PROVINCE]"
- "what do I have to disclose when selling [STATE/PROVINCE]"
- "[SELLER_DISCLOSURE_FORM] what do I need to include"
- "what happens during escrow [STATE/PROVINCE]"
- "how does the home inspection work for sellers"
- "what if the buyer's financing falls through"
- "what if the appraisal comes in low"
- "can a buyer back out after inspection [STATE/PROVINCE]"
- "can I back out of selling my house after accepting an offer [STATE/PROVINCE]"
- "what happens if the buyer asks for repairs after inspection"
- "should I accept a contingent offer [CITY]"
- "what is earnest money and who keeps it [STATE/PROVINCE]"
- "how do multiple offers work [CITY]"
- "what does under contract mean [STATE/PROVINCE]"
- "do I need a [CLOSING_ENTITY] to sell my house in [STATE/PROVINCE]"
- "what is a seller concession [STATE/PROVINCE]"
- "can I sell my house while renting it out [STATE/PROVINCE]"
- "what happens if I sell my house for less than I owe"
- "selling a house with a mortgage [STATE/PROVINCE]"
- "how to sell a house with tenants [STATE/PROVINCE]"
- "can I sell my house if I still owe on it [STATE/PROVINCE]"

### SELLER — Situational & Emotional

- "my house isn't selling what should I do [CITY]"
- "should I lower my asking price [CITY]"
- "no offers on my house [CITY]"
- "house sitting on market too long [CITY]"
- "why isn't my house selling [CITY]"
- "should I take my house off the market [CITY]"
- "should I sell my house in a down market [CITY]"
- "selling a house during divorce [STATE/PROVINCE]"
- "selling inherited house [STATE/PROVINCE]"
- "selling a house after death of spouse [STATE/PROVINCE]"
- "how to sell a house in probate [STATE/PROVINCE]"
- "selling a house with foundation issues [CITY]"
- "should I sell to an iBuyer [CITY]"
- "selling to Opendoor vs listing with agent [CITY]"
- "FSBO vs using an agent [CITY]"
- "should I sell my house or rent it out [CITY]"
- "relocating and need to sell fast [CITY]"
- "underwater on my mortgage should I sell [CITY]"

### BUYER — Cost & Financial

- "how much do I need to buy a house in [CITY]"
- "down payment for a house in [CITY] [STATE/PROVINCE]"
- "closing costs for buyers in [CITY] [STATE/PROVINCE]"
- "hidden costs of buying a house [CITY]"
- "how much house can I afford [CITY]"
- "first time home buyer programs [CITY] [STATE/PROVINCE]"
- "down payment assistance [STATE/PROVINCE]"
- "how much are property taxes in [COUNTY/REGION]"
- "HOA fees in [CITY] [NEIGHBORHOOD]"
- "what credit score do I need to buy a house [STATE/PROVINCE]"
- "FHA vs conventional loan [STATE/PROVINCE]"
- "VA loan requirements [STATE/PROVINCE]"
- "how much are mortgage payments on a [PRICE_RANGE] house [CITY]"
- "is it cheaper to buy or build in [CITY]"
- "cost of home warranty [CITY]"
- "how much does a home inspection cost [CITY]"
- "average utility costs in [CITY]"
- "what is PMI and how do I avoid it"
- "how much do I need in reserves to buy a house"
- "earnest money deposit how much [CITY]"
- "who pays for the appraisal buyer or seller [STATE/PROVINCE]"

### BUYER — Timing & Readiness

- "is now a good time to buy a house [CITY] [STATE/PROVINCE]"
- "should I buy a house now or wait [CITY]"
- "when is the best time to buy in [CITY]"
- "how long does it take to buy a house [CITY]"
- "how long does the mortgage process take [STATE/PROVINCE]"
- "should I buy before interest rates go up [CITY]"
- "how long does pre-approval take"
- "when should I get pre-approved"
- "should I buy now or wait for prices to drop [CITY]"
- "housing market forecast [CITY] [STATE/PROVINCE]"
- "is the housing market going to crash [CITY]"
- "will home prices go down in [CITY]"
- "should I wait for lower mortgage rates"

### BUYER — Process & What-Happens-Next

- "steps to buying a house in [STATE/PROVINCE]"
- "what happens after my offer is accepted [STATE/PROVINCE]"
- "what happens during the home inspection"
- "what to expect at closing [STATE/PROVINCE]"
- "what is escrow and how does it work [STATE/PROVINCE]"
- "what does the [CLOSING_ENTITY] do [STATE/PROVINCE]"
- "how does the appraisal process work"
- "what if the appraisal comes in low as a buyer"
- "can I back out of buying a house after inspection [STATE/PROVINCE]"
- "what are contingencies in a real estate contract [STATE/PROVINCE]"
- "what is due diligence period [STATE/PROVINCE]"
- "what does pending mean on a house listing"
- "how to make a competitive offer [CITY]"
- "how to win a bidding war [CITY]"
- "should I waive inspection [CITY]"
- "what happens if I lose the bidding war [CITY]"
- "how to negotiate home price [CITY]"
- "what repairs can I ask the seller to make"
- "should I ask for closing cost credits"
- "what is a buyer's agent agreement [STATE/PROVINCE]"
- "do I have to sign a buyer broker agreement [STATE/PROVINCE]"
- "what does a buyer's agent do for me"
- "can I buy a house without an agent [STATE/PROVINCE]"
- "what to look for during a home showing"
- "red flags when buying a house"
- "how many houses should I look at before buying"

### BUYER — Situational & Emotional

- "first time home buyer mistakes [CITY]"
- "biggest regrets buying a house"
- "what I wish I knew before buying a house [CITY]"
- "buying a house with student loans"
- "can I buy a house with bad credit [STATE/PROVINCE]"
- "buying a house as a single person [CITY]"
- "scared to buy a house"
- "is it worth buying a fixer upper [CITY]"
- "should I buy a new construction or resale [CITY]"
- "buying a house sight unseen [CITY]"
- "relocating to [CITY] what to know"
- "moving to [CITY] pros and cons"
- "renting vs buying [CITY] [STATE/PROVINCE]"
- "can I buy a house before selling mine [STATE/PROVINCE]"
- "bridge loan for buying before selling [STATE/PROVINCE]"
- "what if I can't sell my house before buying another"
- "buying in a seller's market [CITY]"
- "outbid on a house what to do next"
- "lost multiple offers [CITY]"
- "how to buy a house in a competitive market [CITY]"

### TRADE-OFF / DECISION (Both Audiences)

- "should I sell before buying [CITY]"
- "rent vs buy [CITY] [STATE/PROVINCE]"
- "is it worth renovating before selling [CITY]"
- "sell house as-is or fix up [CITY]"
- "should I wait to sell [CITY]"
- "sell and rent back [CITY]"
- "is it better to sell or rent out my house [CITY]"
- "new construction vs resale [CITY]"
- "condo vs townhouse [CITY]"
- "buy in [NEIGHBORHOOD_1] vs [NEIGHBORHOOD_2]"
- "is it worth buying now with high interest rates [CITY]"
- "should I pay points to lower my rate"
- "15 year vs 30 year mortgage [CITY]"
- "adjustable rate vs fixed rate mortgage"
- "should I make a lowball offer [CITY]"
- "is it worth buying a house that needs work [CITY]"
- "keep my house or sell it [CITY]"
- "is it a buyer's or seller's market in [CITY]"

### JURISDICTION-SPECIFIC PROCESS

- "do I need a [CLOSING_ENTITY] to buy a house in [STATE/PROVINCE]"
- "how much is [TRANSFER_TAX_TERM] in [COUNTY/REGION]"
- "[SELLER_DISCLOSURE_FORM] requirements [STATE/PROVINCE]"
- "attorney review period [STATE/PROVINCE]"
- "escrow timeline [STATE/PROVINCE]"
- "title insurance cost [STATE/PROVINCE]"
- "who picks the [CLOSING_ENTITY] buyer or seller [STATE/PROVINCE]"
- "property tax rate [COUNTY/REGION] [STATE/PROVINCE]"
- "homestead exemption [STATE/PROVINCE]"
- "HOA disclosure requirements [STATE/PROVINCE]"
- "[STATE/PROVINCE] real estate contract contingencies"
- "what is required to disclose when selling a house [STATE/PROVINCE]"
- "lead paint disclosure [STATE/PROVINCE]"
- "septic inspection required [STATE/PROVINCE]"
- "well water testing requirements [STATE/PROVINCE]"
- "radon testing [STATE/PROVINCE] real estate"

### NEIGHBORHOOD & HYPERLOCAL

- "homes for sale in [NEIGHBORHOOD] [CITY]"
- "[NEIGHBORHOOD] real estate market"
- "[NEIGHBORHOOD] vs [NEIGHBORHOOD] [CITY]" (property features and price comparisons ONLY)
- "new construction in [NEIGHBORHOOD] [CITY]"
- "new subdivision [CITY]"
- "[LOCAL_HOT_TOPIC] impact on real estate [CITY]"
- "[LOCAL_HOT_TOPIC] [NEIGHBORHOOD]"
- "property values in [NEIGHBORHOOD] [CITY]"
- "what's being built in [NEIGHBORHOOD]"
- "new development near [CITY]"
- "housing market in [NEIGHBORHOOD] [CITY]"
- "[CITY] real estate market update"
- "home prices in [NEIGHBORHOOD] going up or down"
- "is [NEIGHBORHOOD] a good investment"
- "cost of living in [CITY] [STATE/PROVINCE]"
- "moving to [CITY] from [COMMON_ORIGIN_CITY]"
- "what to know before moving to [CITY]"
- "pros and cons of living in [CITY]"
- "pros and cons of living in [NEIGHBORHOOD]"

Generate additional hyperlocal queries for any local hot topics from the config — new subdivisions, employer relocations, infrastructure projects, zoning changes, etc.

### TRIGGER-WORD MODIFIED EXAMPLES

After generating the core queries above, also produce modified versions of the strongest ones using these decision-stage modifiers:

best, how to choose, vs, comparison, top, review, recommend, recommendation, worth it, pros and cons, should I, mistakes, regret, wish I knew, before you, don't, avoid

Examples:
- "mistakes selling a house in [CITY]"
- "things to avoid when buying a house [CITY]"
- "best way to sell your house fast [CITY]"
- "pros and cons of selling as-is [CITY]"
- "regrets buying new construction [CITY]"
- "what I wish I knew before selling [CITY]"
- "things to do before listing your house [CITY]"
- "don't sell your house before doing this [CITY]"
- "best home improvements before selling [CITY]"
- "worst mistakes first time buyers make [CITY]"
- "recommend a home inspector [CITY]"

---

## Rules

- Only generate queries for the audience specified in the config (buyers, sellers, or both). Skip irrelevant sections.
- Use the most specific geographic variable that fits each query type.
- Inject state/province-specific process terms (closing entity, transfer tax, disclosure form) from the config.
- Generate neighborhood-level queries for every neighborhood listed in the config.
- Generate queries for every local hot topic listed in the config.
- Do NOT generate any query that could violate Fair Housing guidelines (no demographic descriptions of neighborhoods, no school quality rankings, no "safe neighborhood" language).
