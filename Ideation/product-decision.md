# App 1 Product Decision

Date created: 2026-06-13
Last updated: 2026-06-28
Status: Supersedes earlier local-demand, service-page and local-visibility MVP directions

## Decision

App 1 is **GrowthMap**.

GrowthMap helps aspiring and early-stage SEO freelancers decide whether a business is worth approaching, then later create a focused, evidence-backed prospect report.

The frozen V1 product direction is:

```text
email + business URL
-> free SEO prospect qualification
-> sample GBP 12 paid report
-> paid report pipeline later
```

The authoritative product contract is `Design/design.md`.

The implementation/module design is `Design/module-design.md`.

## Buyer

Primary buyer:

- aspiring SEO freelancer
- early-stage SEO freelancer
- small SEO agency

The buyer supplies a prospect URL. GrowthMap does not discover or scrape lead lists in V1.

## Product Thesis

SEO freelancers need a fast way to decide whether a business has enough public SEO opportunity to justify deeper investigation.

GrowthMap must help them avoid two bad outcomes:

- wasting time on prospects with no defensible opportunity
- manufacturing weak problems just to sell a report

The free product qualifies whether enough SEO opportunity exists.

The paid product later turns defensible evidence into a pitch-ready report with one primary sellable opportunity.

## V1 Funnel

### Stage 1: Free Qualification Live

Ship first:

- capture email and business URL
- auto-create or reuse a lightweight user
- normalize the prospect domain
- enforce monthly free qualification allowance
- fetch or reuse public SEO evidence
- classify and summarize evidence
- calculate the qualification score in code
- return a restrained free qualification result
- link to a sample paid report

No password registration is required before value is shown.

No outbound email is required in the first free version.

### Stage 2: Sample Paid Report

Before checkout and paid self-serve generation exist, show a sample GBP 12 report.

Current sample artifacts:

- `Ideation/Reports/qualification-millhilldentist-2026-06-22.md`
- `Ideation/Reports/paid-pipeline-millhilldentist-2026-06-22.json`
- `Ideation/Reports/paid-report-millhilldentist-2026-06-22.md`

### Stage 3: Paid Pipeline Later

Build only after free qualification is live and the sample report has been tested.

Later paid scope:

- checkout/token purchase
- report-token ledger
- deeper evidence collection
- screenshot/rendered UX evidence
- conversion-path readiness evidence
- opportunity candidates
- selected opportunity
- final report generation

## Free Qualification Contract

Input:

- email
- business URL

Evidence:

- DataForSEO ranked keyword evidence
- DataForSEO on-page/page evidence
- one LLM interpretation call for keyword classification, grouping and evidence summary

Code owns:

- scoring
- outcome
- limitations
- final qualification assembly

The LLM does not calculate or change the qualification score.

Valid outcomes:

- `good_prospect`
- `possible_prospect`
- `weak_prospect`
- `inconclusive`

Provider failure must not be treated as `weak_prospect`. Missing core demand evidence should usually return `inconclusive`.

## Paid Report Contract

The paid report is not live yet.

The accepted paid-report direction is:

- one primary evidence-backed sellable opportunity
- up to two secondary observations
- existing strengths
- recommended focused service
- bounded scope of work
- outreach wording
- client-safe evidence extract
- limitations and prohibited claims

The paid report may include conversion-path readiness and rendered UX evidence.

The free qualification may not.

## Superseded Directions

The following were useful learning pivots but are no longer the current V1:

- local demand gap report based on service + city input
- service-page opportunity and improvement brief
- Local Visibility Prospect Brief based on Maps or Local Finder
- competitor visibility comparison as the first MVP
- AI/GEO visibility measurement
- full local SEO audit
- business-owner-first buyer

These ideas may become later iterations only if real validation justifies them.

## Pricing Decision

Pricing hypothesis:

- free qualification first
- paid report sample visible before checkout
- later paid report price: GBP 12 per report/token

Do not build checkout until the no-defensible-opportunity rule is finalized.

## Scope Boundary

Allowed in V1:

- public URL-only qualification
- public SEO evidence
- reusable prospect/domain evidence cache
- email capture/lightweight account
- restrained qualification result
- sample paid report

Not in first production slice:

- lead-list discovery
- full account registration
- outbound email automation
- checkout
- automated outreach
- recurring monitoring
- Google Business Profile management
- AI visibility scoring
- guaranteed rankings, traffic, leads or revenue
- full technical SEO audit
- polished PDF generation

## One-Line Pitch

GrowthMap helps SEO freelancers qualify whether a business has enough public SEO opportunity to justify a deeper pitch-ready report.
