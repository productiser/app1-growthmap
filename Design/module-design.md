# GrowthMap Module Design

Date created: 2026-06-28
Status: Working implementation design for the frozen V1 product

## Purpose

This document translates the frozen GrowthMap V1 product contract into module flows and table responsibilities.

Source of truth:

- Product contract: `Design/design.md`
- This file: module interactions, launch sequence and database responsibility map
- Deprecated schema draft: `Design/DDL.sql` must not be applied until replaced

## Launch Sequence

V1 should reach production in three stages.

### Stage 1: Free Qualification Live

Ship the free qualification flow first.

User-facing promise:

> Paste a business URL and get a restrained SEO prospect qualification.

Implementation scope:

- Capture business URL first.
- Run only cheap URL/domain validation before email capture.
- Capture email before expensive provider or LLM calls.
- Auto-create or reuse a lightweight user account from the email.
- Do not require password registration before the user sees value.
- Do not send outbound email in the first free version.
- Enforce a monthly free qualification allowance.
- Normalize and cache reusable prospect/domain evidence.
- Store each user's qualification request and result.
- Show a CTA to view a sample paid report.

### Stage 2: Paid Report Shown As Sample

Before checkout and paid self-serve generation exist, show a sample paid report.

User-facing promise:

> See what the GBP 12 pitch-ready report will look like.

Implementation scope:

- Link from the free result to the sample report.
- Use the Mill Hill Dental style artifact as the product example.
- Do not charge tokens yet.
- Do not build checkout yet.
- Use feedback from free users to validate whether the paid artifact is compelling.

### Stage 3: Paid Pipeline Later

Build paid generation after the free version is live and the sample report has been tested.

Later scope:

- Token purchase and ledger.
- Paid report request.
- Deeper evidence collection.
- Browser/screenshot evidence.
- Opportunity candidate validation.
- Final paid report generation.
- No-defensible-opportunity handling before checkout is enabled.

## Module 1- Free Qualification Interaction Flow

Draw this flow before writing schema or code.

```text
Visitor
  -> enters business_url
  -> system normalizes URL/domain
  -> system checks that market/domain is minimally usable
  -> user enters email to run the free qualification
  -> system normalizes email
  -> system creates or finds lightweight user
  -> system creates or finds prospect identity by normalized domain
  -> system creates qualification_request with public access token
  -> system checks monthly free allowance
  -> system checks reusable prospect evidence cache
  -> if cache is usable: reuse evidence
  -> if cache is missing/stale: fetch ranked keywords and page/on-page evidence
  -> system parses provider evidence
  -> system classifies ranked keywords
  -> code calculates deterministic score and outcome
  -> LLM writes short explanation from verified signals only
  -> system stores user qualification result
  -> user sees free qualification page
  -> user can view sample GBP 12 report
```



![GrowthMap.module1.drawio](/Users/ptalur/greycellmatters/app1/Design/GrowthMap.module1.drawio.png)





## Free Result Contents

The free qualification result may show:

- outcome: `good_prospect`, `possible_prospect`, `weak_prospect` or `inconclusive`
- short headline
- restrained explanation
- top verified SEO signals
- limitations
- CTA to view the sample paid report

The free product may also show a generic recent-activity trust element, derived from completed qualification requests:

```text
Recent activity
- Qualification completed 3 minutes ago
- Qualification completed 11 minutes ago
```

Rules:

- Do not show submitted URL.
- Do not show business name.
- Do not show city/location.
- Do not show qualification outcome.
- Do not create a separate table for this in V1.

The free result must not show:

- conversion-path readiness findings
- rendered UX or screenshot findings
- outreach copy
- promised rankings, traffic, leads or revenue
- a manufactured reason to buy the report

## Account Model For Free V1

Use email capture as the first account model.

Chosen flow:

```text
business_url -> cheap URL precheck -> email gate -> lightweight user -> qualification result
```

Rules:

- Business URL is entered first.
- Only cheap URL/domain validation happens before email capture.
- Email is required before provider or LLM calls are made.
- A user record can be auto-created from the submitted email.
- No password is required for the first V1 free flow.
- No outbound email is required in the first V1 free flow.
- A qualification result is accessed using a generated public access token until login/magic-link support exists.
- Later paid/report-history features can add magic-link login or fuller registration.

Why:

- Fully open free checks lose feedback and allowance control.
- Running the full provider pipeline before email can waste API/LLM cost.
- Full registration adds too much friction before value is shown.
- URL-first precheck feels lighter while still gating expensive work behind email intent.
- Email capture supports follow-up, feedback and a later upgrade path.

## Module 1 Entities

### Users

Owns:

- lightweight user identity
- normalized email
- account creation or lookup
- later upgrade to magic-link/full account

Does not own:

- qualification scoring
- prospect evidence
- provider calls

### Prospects

Owns reusable public identity for the checked business.

Owns:

- normalized domain
- submitted URL history where useful
- market assumptions
- evidence cache status

Does not own:

- user allowance
- user-specific result wording
- report ownership

### Monthly Usage

Owns free usage limits.

Owns:

- monthly qualification allowance
- usage count
- allowance period

Rule:

- A qualification consumes allowance whether evidence is freshly fetched or served from cache.

### Qualification Requests

Owns each user's free check.

Owns:

- user id
- prospect id
- submitted URL
- status
- evidence version used
- deterministic score
- outcome
- user-facing result

Does not own:

- raw provider response storage
- paid report content
- token charging

### Provider Calls

Owns provider and LLM execution records.

Owns:

- provider/model name
- endpoint or stage
- request status
- request/response JSON
- actual cost when available
- started/completed timestamps
- error details

Purpose:

- debug failures
- understand cost
- make results inspectable

### Ranked Keywords, Page checks

Owns structured facts extracted from provider responses.

For free qualification, this includes:

- ranked keywords
- keyword classifications
- page/on-page checks

### Scoring

Code-owned logic.

Owns:

- demand evidence score
- SEO headroom score
- technical feasibility score
- final outcome

Rule:

- The LLM cannot calculate or change the score.

### Qualification Narrative

LLM-owned wording only.

Owns:

- short headline
- one or two explanatory sentences

Inputs:

- deterministic score
- deterministic outcome
- verified signals
- limitations

Rule:

- The LLM may explain evidence but cannot invent findings or recommend paid work.

Candidate table responsibilities:

```text
users
  lightweight user identity and normalized email

monthly_usage
  one row per user per month or equivalent allowance period

prospects
  normalized domain and reusable prospect identity

qualification_requests
  one user-owned free check and final free result

provider_calls
  DataForSEO/OpenAI calls, raw JSON, status, errors and costs

ranked_keywords
  parsed ranked keyword rows linked to prospect/provider call

page_checks
  parsed homepage/on-page facts linked to prospect/provider call
```

Open design question:

- Store keyword classifications on `ranked_keywords` if each keyword row has one current classification.
- Use a separate classification table only if we need multiple classifiers, versions or audit history.

Open design question:

- Store the deterministic score fields directly on `qualification_requests` for V1 simplicity.
- Split into a separate score table only if scoring versions become hard to reason about.

## Module 1 Relationship Sketch

![ERD](/Users/ptalur/greycellmatters/app1/Design/ERD.png)

Core boundary:

```text
prospect/domain evidence = reusable public cache
qualification request = user-owned result and allowance event
```



## Paid Module Placeholder

Paid is intentionally not the first production build.

For now, the paid surface is:

```text
free qualification result -> sample GBP 12 report
```

Later paid modules:

- billing
- token ledger
- paid report requests
- deeper evidence collection
- screenshot/rendered evidence
- opportunity candidates
- selected opportunity
- final report

Do not design checkout or token charging until the no-defensible-opportunity rule is finalized.
