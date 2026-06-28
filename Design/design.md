# GrowthMap Design

Date created: 2026-06-13  
Last updated: 2026-06-28  
Status: **V1 HARD-FROZEN — SEO Opportunity + Conversion-Path Readiness**

## Freeze Rule

This is the fixed App 1 direction.

**NO MORE V1 PRODUCT PIVOTS.**

Do not reopen naming, buyer, funnel, value proposition, evidence categories or paid artifact during implementation. Real user testing may create later iterations, but new ideas do not change V1.

Implementation details may change only to deliver this contract safely and reliably.

## Linked Implementation Design

Detailed module flows, free-version launch sequencing and table responsibilities live in:

- `Design/module-design.md`

This file remains the product contract. The linked module design is the working implementation map.

## Product Direction

GrowthMap helps aspiring and early-stage SEO freelancers decide whether a business is worth approaching and then create a focused, evidence-backed pitch.

The product answers two connected questions:

> Can customers find this business?

> Once they find it, does the website give them the right signals and a usable path towards booking, enquiring, calling or buying?

The first question is **SEO opportunity**.

The second is **conversion-path readiness**.

The product has two stages:

1. Paste a business URL and receive a free SEO prospect qualification.
2. Spend one report token, currently priced at £12, to create a pitch-ready prospect report.

The free result answers:

> Does this business show enough publicly observable SEO opportunity to justify deeper investigation?

The paid result answers:

> What is the strongest defensible SEO or conversion-path opportunity, what evidence supports it, what focused service should be pitched, and how can the freelancer approach the business responsibly?

GrowthMap must not manufacture a problem to sell a report.

## Buyer

Primary buyer:

- aspiring SEO freelancer
- early-stage SEO freelancer
- small SEO agency

The buyer supplies a prospect URL. GrowthMap does not discover or scrape lead lists in V1.

## Funnel And Pricing

- A signed-in user receives three free qualification checks per calendar month.
- Qualification usage counts from the user's allowance whether evidence is newly fetched or served from cache.
- Cache behaviour is internal and is not shown to the user.
- A pitch-ready report costs one report token.
- Initial price: £12 for one token/report.
- Charge the token only after a complete paid report is produced successfully.
- Provider or LLM failures do not consume a token.
- If deeper paid analysis finds no defensible opportunity, the report must not invent one. The no-charge/refund rule must be finalized before checkout is implemented.

Paid bundles remain a later commercial decision.

## V1 Input

Free qualification input:

```text
business_url
```

The URL is normalized to a reusable domain identity.

Market inference:

- A `.co.uk` domain may use United Kingdom and English as an explicit assumption.
- The assumption is stored and included in limitations.
- URL-only qualification does not claim city-level or precise local analysis.
- If the market cannot be inferred safely, return `inconclusive` or request the missing country.

## Free Qualification Contract

### Evidence

#### Existing search visibility and demand

Use DataForSEO Labs `ranked_keywords` for the domain and assumed market.

Retain:

- total ranked keyword count
- estimated organic traffic
- keyword
- ranking URL
- ranking position
- search volume
- CPC
- competition when available

Returned keywords must be classified before scoring:

```text
business_brand
other_company_brand
relevant_commercial
relevant_informational
irrelevant_or_ambiguous
```

Other-company brand terms do not count as useful demand evidence.

#### Basic on-page readiness

Use DataForSEO On-Page Instant Pages or equivalent direct HTML checks on the submitted page.

Retain:

- HTTP status
- HTTPS
- title
- meta description
- H1
- canonical
- indexability
- redirects
- obvious broken-page state
- fetch duration

Observed DataForSEO cost on 2026-06-22:

```text
ranked keywords, 20 rows: $0.012000
one on-page check:        $0.000125
free qualification total: $0.012125
```

#### Technical feasibility

Check:

- page fetch succeeds
- HTTPS works
- normal crawling is not blocked
- page is not explicitly `noindex`

PageSpeed is optional. Rate limiting or provider failure must not fail the complete qualification.

### Exclusions

Free qualification does not assess:

- complete visual or user experience
- city-level local visibility
- Maps or Local Finder
- AI visibility
- backlinks
- full-site crawling
- missed-keyword discovery
- Search Console or analytics
- outreach wording

### Scoring

The score is calculated in code. The LLM cannot calculate or alter it.

Current scoring dimensions:

```text
demand evidence
SEO headroom
technical feasibility
```

Exact weights and thresholds remain implementation variables until tested against:

- a clearly promising prospect
- a strong business with few defensible gaps
- an ambiguous or data-poor business

Valid outcomes:

```text
good_prospect
possible_prospect
weak_prospect
inconclusive
```

### Qualification LLM

The qualification LLM receives:

- deterministic score
- deterministic classification
- up to three verified signals
- explicit limitations

It may write:

- a short headline
- one or two restrained explanatory sentences

It must not:

- change the score
- invent findings
- recommend paid work
- promise rankings, traffic, leads or revenue

### Free Output

Example:

> **Promising SEO prospect**
>
> The site already appears for commercially valuable dental searches, but several relevant sampled rankings remain outside the top results. There is enough evidence to justify a deeper SEO opportunity report.

The user sees the same result whether the underlying evidence was fetched or reused.

## £12 Paid Report Contract

The Mill Hill Dental experiment validated the paid report as a useful, payable artifact.

The report examines:

- deeper ranked-keyword evidence
- broader keyword demand
- homepage plus up to two relevant pages
- on-page evidence
- paid-only rendered UX and conversion-path evidence
- existing SEO and conversion strengths
- supported opportunity candidates

The report produces:

1. Prospect verdict and confidence
2. One primary pitchable SEO opportunity
3. Evidence supporting that opportunity
4. Existing strengths
5. One recommended service
6. A bounded scope of work
7. Up to two secondary observations
8. Freelancer outreach wording
9. A client-safe evidence extract
10. Explicit limitations and prohibited claims

### Paid Evidence Pipeline

Validated experimental flow:

```text
domain and market
→ 100 ranked keywords
→ broader keyword ideas
→ homepage plus two selected page checks
→ paid-only screenshot evidence
→ keyword relevance classification
→ verified findings and strengths
→ supported opportunity candidates
→ LLM selects one sellable, defensible opportunity
→ code validates the selected candidate
→ LLM writes the final pitch-ready report
```

### Opportunity Selection

Code and provider evidence create the candidate set.

Each candidate includes:

- finding IDs
- commercial value
- evidence strength
- delivery clarity
- overclaim risk
- recommended service
- limitations

The LLM may weigh and select the best opportunity using:

- commercial relevance
- evidence strength
- severity of the demonstrated gap
- clarity of the freelancer's deliverable
- ease of explaining the opportunity
- overclaim risk

The LLM:

- may select only an existing candidate
- must cite supporting finding IDs
- may return `no_defensible_opportunity`
- cannot turn an existing strength alone into a paid problem

Code validates that the selected candidate exists before report generation.

### Paid-Only Conversion-Path Readiness

Rendered-page and bounded conversion-path analysis are justified in the paid report, not in free qualification.

Conversion-path readiness means checking whether an interested visitor receives the right signals and can begin the business's primary public action.

Examples by business type:

- dentist: book or request an appointment
- venue or restaurant: begin a reservation
- solicitor or tradesperson: submit or begin an enquiry
- salon or gym: choose a service and begin booking
- estate agent: request a viewing
- SaaS company: start a trial or request a demo

This is not limited to ecommerce.

Paid UX evidence may include:

- desktop and mobile screenshots
- above-the-fold content visibility
- navigation density
- visible service proposition
- CTA visibility
- CTA destination and first-step availability
- consistent business location, language and currency
- obvious broken forms, booking widgets or third-party integration failures
- clipping, overlap and overflow

V1 limits:

- homepage plus no more than two selected service pages
- fixed timeouts
- no login or form interaction
- no real enquiry submission
- no reservation confirmation
- no purchase or payment
- no personal or sensitive data entry
- browser failure does not invalidate other report evidence
- conversion-path findings stay separate from SEO findings
- screenshots use a defined retention/deletion policy

The 2026-06-22 experiment used a user-supplied screenshot. Automated capture remains an implementation task.

## Validated Mill Hill Dental Sample

Target:

```text
https://millhilldentist.co.uk/
```

The paid pipeline selected:

> **Invisalign Landing-Page SEO Optimisation**

Primary evidence:

| Query | Position | Search volume | CPC |
|---|---:|---:|---:|
| invisalign aligners london | 86 | 1,900 | $29.64 |
| cheap invisalign london | 87 | 720 | $23.74 |
| invisalign doctors near me | 55 | 140 | $12.17 |
| invisalign treatment near me | 74 | 140 | $28.41 |

Existing strengths included:

- top-10 visibility for core Mill Hill and North London dentist terms
- a live, substantial Invisalign page
- visible online-booking CTA

Secondary observations:

- emergency dental-care SEO
- above-the-fold conversion-path clarity

Observed successful paid-run DataForSEO cost:

```text
100 ranked keywords: $0.020000
keywords for site:   $0.075000
three page checks:   $0.000375
total:               $0.095375
```

Experimental runtime:

```text
279.35 seconds
```

OpenAI inference cost was not captured and must be stored in production.

Artifacts:

- `Ideation/Reports/qualification-millhilldentist-2026-06-22.md`
- `Ideation/Reports/paid-pipeline-millhilldentist-2026-06-22.json`
- `Ideation/Reports/paid-report-millhilldentist-2026-06-22.md`
- `Ideation/Samples/millhilldentist-homepage-2026-06-22.png`

## Code And LLM Responsibilities

Code owns:

- URL and domain normalization
- market inference
- cache lookup
- monthly qualification allowance
- provider calls
- parsing and validation
- deterministic pre-filtering
- free qualification scoring
- evidence and finding IDs
- candidate validation
- persistence
- provider and LLM cost tracking
- failure handling
- token charging after successful paid completion

The qualification LLM owns:

- short wording of the verified free result

The paid evidence LLM owns:

- bounded keyword relevance classification where deterministic rules are insufficient
- converting verified evidence into candidate opportunities

The opportunity-selection LLM owns:

- weighing supported candidates
- selecting one primary sellable opportunity

The report LLM owns:

- explaining the selected evidence
- drafting the bounded scope
- creating outreach and client-safe wording
- stating limitations

No LLM may invent rankings, demand, page facts, competitors, traffic, bookings, leads or revenue.

## Final V1 Value Proposition

GrowthMap qualifies and equips an SEO freelancer using two evidence layers:

```text
DISCOVERABILITY
Can the business be found for valuable searches?

CONVERSION-PATH READINESS
Once found, does the site provide the right signals and a usable path towards the primary customer action?
```

The paid report selects one primary sellable opportunity from either layer.

Examples:

- service page has measurable commercial ranking headroom
- booking CTA or widget fails to load
- location or currency becomes inconsistent during booking
- contact or enquiry path is broken
- navigation obscures the service proposition and primary action

Visual criticism alone is not the product. Findings must connect to discoverability, trust, clarity or the ability to begin a customer action.

## V1 Failure Rules

- Cached and fresh qualifications have identical user-facing behaviour.
- Provider failure returns `inconclusive`, not `weak_prospect`.
- PageSpeed failure does not fail qualification.
- Paid browser failure does not erase valid SEO evidence.
- Failed paid generation does not consume a token.
- A selected opportunity must reference existing candidate and finding IDs.
- A paid report must acknowledge existing strengths.
- A paid report must not be generated when no defensible opportunity survives validation.

The commercial handling of `no_defensible_opportunity` must be fixed before checkout implementation.

## Database Requirements

The schema must support these distinct concepts:

### Identity and access

- users

### Prospect identity and reusable cache

- normalized prospects/domains
- market assumption
- first and last seen dates

### Free qualification

- one user qualification request
- monthly allowance usage
- cached evidence version used
- deterministic score and classification
- user-facing qualification result

### Evidence collection

- provider/LLM run
- stage and endpoint/model
- request status
- provider task ID
- input/output JSON
- actual cost
- timestamps and errors

### Parsed evidence

- ranked keywords
- keyword ideas
- page checks
- screenshot/render evidence
- conversion-path checks and observed steps
- verified findings
- strengths and limitations

### Paid report

- report request
- supported opportunity candidates
- selected opportunity
- final structured report JSON
- report status and completion time

### Commerce

- report-token products
- payments
- append-only token ledger
- one report charge after successful completion

The schema should reuse public prospect evidence across users while keeping each user's qualification allowance, report ownership and token history separate.

## V1 Boundaries

Not included:

- lead-list discovery
- automated outreach
- recurring monitoring
- Search Console or analytics access
- backlink campaigns
- Google Business Profile management
- AI visibility
- guaranteed rankings or revenue
- full technical site audit
- completing real bookings, enquiries or purchases
- background workers in the first hand-coded slice
- polished PDF generation

## Build Order

1. Freeze the two-stage product and artifacts. **Complete**
2. Agree the compact V1 database model.
3. Create the modular Python structure manually.
4. Build shared `core` configuration and database infrastructure.
5. Build the reusable `users` module.
6. Build the reusable `billing` module and token-ledger rules.
7. Build the GrowthMap `qualifications` module.
8. Build the GrowthMap `reports` module.
9. Build the dashboard read models and endpoints.
10. Integrate evidence providers one stage at a time.
11. Add bounded LLM stages and validation.
12. Test promising, strong/no-gap and inconclusive businesses.

## Modular Code Structure

GrowthMap will be organised by business responsibility:

```text
app/
├── core/
│   ├── config.py
│   └── database.py
├── users/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   └── routes.py
├── billing/
│   ├── models.py
│   ├── schemas.py
│   ├── repository.py
│   ├── service.py
│   └── routes.py
├── qualifications/
├── reports/
└── dashboard/
```

Each business module uses the same layer responsibilities:

- `routes.py`: receives HTTP requests and returns HTTP responses
- `schemas.py`: defines Pydantic input and output shapes
- `service.py`: owns business decisions and workflows
- `repository.py`: owns SQL and Postgres reads/writes
- `models.py`: represents stored or domain entities

Shared infrastructure belongs in `core`:

- `config.py`: environment and application settings
- `database.py`: connections and transaction handling

Healthy dependency direction:

```text
route → service → repository → database
```

Modules collaborate through service functions. For example, the reports service asks the billing service to check or charge tokens; it does not write directly to the token ledger.

The reusable public interfaces should stay small:

```text
register_user(...)
authenticate_user(...)
get_token_balance(...)
credit_tokens(...)
charge_report_token(...)
```

These modules are proved inside GrowthMap before being extracted into a shared package for later apps.

Prevs will create this structure manually from scratch so the architecture and Python imports are understood rather than generated invisibly.

## Next Build Session

Next build session: **Saturday, 27 June 2026**.

There is no GrowthMap coding planned between 22 and 27 June because of a hackathon and conference.

The Saturday session begins with a one-question-at-a-time cumulative quiz. If the module boundaries are unclear, review them before creating folders.

Saturday's practical objective:

1. Create the package and module folders manually.
2. Understand the purpose of `__init__.py`.
3. Practise imports between modules.
4. Create `core/config.py`.
5. Create `core/database.py`.
6. Stop before building the user module unless the structure is understood.

## Current Decision

Build the qualification-first GrowthMap:

```text
paste URL
→ three free SEO prospect qualifications per month
→ £12 pitch-ready report
→ one evidence-backed SEO or conversion-path opportunity
```

The product contract and Mill Hill Dental sample report are hard-frozen. Database design is the next implementation stage. New product ideas go to later iterations and do not interrupt V1 delivery.
