# GrowthMap Build Log

This is the public progress log for GrowthMap.

Personal learning notes and raw session reflections are outside the public repo.

## Build Time Tracking

Purpose:

- Track roughly how many focused design/dev hours it takes to build GrowthMap as App 1.
- Count active product design, backend design, coding, debugging and learning that directly moves GrowthMap forward.
- Exclude breaks, unrelated admin, YouTube planning/recording/editing and general reading that does not affect the app.

How to update:

- Add `Start`, `Break`, `Back` and `Stop` notes during the day when practical.
- Record one `Focused time` total at the end of each build day.
- Keep totals approximate; consistency matters more than stopwatch precision.

Running total:

- Through 2026-06-28: approximately 6.5 focused hours tracked retrospectively.

## 2026-07-10

Objective:

- Verify parsed `page_checks` insertion, then wire on-page evidence persistence into the qualification flow if the smoke test passes.

Time log:

- Start: 13:00 IST
- Stop: 13:39 IST
- Focused time: approximately 0.7 hours
- Running total: approximately 16.9 hours

Completed:

- Verified `page_checks` insertion with a rollback smoke test against a saved DataForSEO `on_page` provider response.
- Wired parsed on-page evidence persistence into the qualification flow.
- Changed `checked_url` to store the actual normalized URL checked, not only the normalized domain.
- Reordered the on-page flow so the raw provider call is marked completed before parsed `page_checks` insertion.
- Hardened `extract_page_check_row` so missing `tasks`, `result`, `items` or `h1` do not crash the parser.

Verified:

- `./.venv/bin/python -m compileall app tests`
- `./.venv/bin/python -m tests.TestOnpageExtract`
- Parser edge-case import checks for empty provider structures and missing `h1`

Next:

- Resume with one full `POST /qualify/start` smoke test and confirm `provider_calls`, `ranked_keywords` and `page_checks` all persist.
- Then define the bounded LLM contract for keyword classification plus evidence summary.

## 2026-07-09

Objective:

- Tighten the on-page evidence shape before moving on to LLM classification work.

Time log:

- Focused time: approximately 4.0 hours
- Running total: approximately 16.2 hours

Completed:

- Rechecked the free-qualification design split between code-owned scoring and LLM-owned evidence interpretation.
- Updated the module design so keyword buckets are code-defined while LLM classification stays bounded to those buckets.
- Debugged local PostgreSQL startup after restart and recovered it from a stale `postmaster.pid` lock file.
- Inspected the saved DataForSEO `on_page` response shape directly from Postgres.
- Reviewed which on-page fields are meaningful for the V1 free qualification and trimmed the `page_checks` table accordingly.
- Altered the local `page_checks` table to match the narrowed V1 shape.
- Implemented `extract_page_check_row` for the current `on_page` response structure.
- Implemented repository insertion for parsed `page_checks` rows.

Decisions:

- Keep the homepage/on-page evidence slice tight and interpretable for V1.
- Do not treat DataForSEO `inbound_links_count` as backlink evidence.
- Keep `onpage_score` as optional future LLM context only, not as a deterministic product score input.
- Drop unclear or weak V1 fields such as `noindex`, `indexable` and `obvious_broken_page` from the current `page_checks` shape.

Next:

- Verify `page_checks` insertion with a rollback smoke test.
- Wire parsed on-page persistence into the qualification flow if the smoke test passes.
- Then define the bounded LLM contract for keyword classification plus evidence summary.

## 2026-07-08

Objective:

- Resume GrowthMap after travel/sickness with one focused backend slice.

Time log:

- Focused time before lunch break: approximately 1.0 hour
- Break: 13:59 IST
- Back: 15:24 IST
- Stop: 16:28 IST
- Focused time: approximately 2.1 hours
- Running total: approximately 12.2 hours

Completed:

- Reviewed service/repository transaction boundaries and provider-call evidence handling.
- Recovered local PostgreSQL after a cold shutdown and restarted it through Homebrew.
- Inspected the saved DataForSEO ranked-keywords response shape in Postgres.
- Added ranked-keyword parsing for stored DataForSEO provider responses.
- Added repository persistence for parsed ranked-keyword evidence.
- Verified parser output against a saved provider response.
- Verified ranked-keyword insert behavior with a rollback test.

Next:

- Classify parsed ranked-keyword evidence before scoring or generating a qualification result.

## 2026-07-03

Objective:

- Keep continuity during a flu/recovery day with a light backend slice and concept review.

Time log:

- Focused time: approximately 1.0 hour
- Running total: approximately 10.1 hours

Completed:

- Reviewed why SQL/table ownership belongs in the repository layer.
- Added type hints to repository functions for the qualification DB slice.
- Added a `DataForSeoClient` boundary for external provider calls.
- Added DataForSEO ranked-keywords and on-page request helpers.
- Added provider-call persistence helpers for `provider_calls`.
- Wired `POST /qualify/start` to collect raw DataForSEO evidence after the email-gated qualification request exists.
- Added DataForSEO status fields to the qualification response schema.
- Verified compile with the project virtual environment.
- Ran a live DataForSEO on-page smoke test.
- Ran an end-to-end local qualification smoke test for `example.com`, creating provider-call rows for ranked keywords and on-page evidence.
- Reviewed Python fundamentals behind the new code:
  - why use a class for the API client
  - what `@dataclass` does
  - what type annotations do
  - why Pydantic is better for external API boundaries than simple internal data holders
  - JSON serialization/deserialization with `dumps`, `loads`, `encode`, `decode` and `response.read()`
  - why HTTP headers are strings in code while request bodies are bytes
  - basic TCP/IP segmentation, MSS and packet fragmentation mental models

Decisions:

- Keep the DataForSEO HTTP/auth boundary out of the repository.
- Store raw provider requests and responses before parsing, scoring or classification.
- Do not parse ranked keywords, classify relevance or generate a qualification result in this slice.
- Keep tomorrow light because recovery and travel readiness matter more than forcing a heavy build session.

Next:

- Do a light code review of the new DataForSEO client and provider-call flow.
- Practise creating small classes manually until the API-client pattern feels less abstract.
- Record a video on 2026-07-04 if energy and voice are good.
- No build work planned for 2026-07-05 and 2026-07-06 due to travel.
- Pick GrowthMap back up on 2026-07-07.
- Use flight time for Claude course follow-up and passive backend engineering course listening.

## 2026-06-30

Objective:

- Add the database/repository slice behind `POST /qualify/start`.

Time log:

- Start: 17:27
- Break: 18:11
- Back: 18:34
- Stop: 19:27
- Focused time: approximately 1.6 hours
- Running total: approximately 9.1 hours

Completed:

- Started `app/qualifications/repository.py`.
- Implemented and manually tested `get_or_create_user`.
- Confirmed new user creation works.
- Confirmed existing user reuse/update works through `ON CONFLICT (email) DO UPDATE ... RETURNING id`.
- Renamed prospect market columns from inferred names to explicit `country_code` and `language_code`.
- Added `Design/2026-06-30-prospects-market-columns.sql` to migrate the existing local database.
- Implemented and manually tested `get_or_create_prospect`.
- Confirmed prospect creation/reuse works by `normalized_domain`.
- Implemented and manually tested `create_qualification_request`.
- Connected `POST /qualify/start` through user, prospect and qualification request creation.
- Added `user_id`, `prospect_id` and `qualification_id` to the start response.
- Refactored repository functions to accept a shared database connection from the service layer.
- Moved the transaction boundary to `start_qualification`, so user/prospect/request creation happens on one connection.
- Verified the app compiles and still exposes `/qualify/start`.

Decisions:

- Keep repository functions responsible for SQL only.
- Use parameterized SQL with tuple parameters, for example `(email,)`, instead of raw string values.
- Service owns the unit of work and shared database connection; repository owns individual SQL statements.
- Pass the connection into repository functions rather than passing one cursor around.

Next:

- Clean up formatting and naming in repository/service files.
- Consider using Pydantic `EmailStr` for email validation.
- Decide whether to return raw database IDs in the public response or keep them internal before frontend work.
- Next product slice: result/status endpoint by public access token.

## 2026-06-29

Objective:

- Build the first `POST /qualify/start` slice.

Time log:

- Start: 16:58
- Break:
- Back:
- Stop: 17:53
- Focused time: approximately 1.0 hour
- Running total: approximately 7.5 hours

Completed:

- Reframed the first free qualification backend action as one endpoint: `POST /qualify/start`.
- Removed the separate precheck flow from the implementation direction.
- Moved qualification HTTP handling into `app/qualifications/routes.py`.
- Added request/response schemas for starting a qualification with:
  - business URL
  - email
  - selected country
  - English as the default language
- Added service-layer validation and normalization for:
  - submitted business URL
  - normalized domain
  - normalized email
  - supported country code
- Added a backend-supported market mapping for `GB`, `US`, `CA`, `AU` and `IN`, including English language and DataForSEO location codes.
- Added public access token generation for the qualification shell.
- Added basic qualification-start logging.
- Verified the FastAPI route list includes `/qualify/start`.
- Verified a valid request returns `200`.
- Verified an unsupported country returns `400`.

Decisions:

- The frontend can show a progressive form locally, but the backend should receive one submit call.
- V1 should not infer market from TLD, LLM or page fetch.
- V1 should ask the user to choose from supported English-language countries.
- Supported countries for now are `GB`, `US`, `CA`, `AU` and `IN`.
- The frontend should send product-level country codes; the backend owns provider-specific DataForSEO location-code mapping.
- The endpoint does not yet write to Postgres, call DataForSEO, call an LLM or calculate a score.

Next:

- Add the database/repository slice for `POST /qualify/start`:
  - create or reuse `users`
  - create or reuse `prospects`
  - create `qualification_requests`
  - persist the generated public access token

## 2026-06-28

Objective:

- Return to GrowthMap after the conference and prepare the project for public development.

Time log:

- Focused time: approximately 6.5 hours, estimated retrospectively from session notes.
- Running total: approximately 6.5 hours.

Completed:

- Confirmed the V1 launch sequence:
  - free qualification live first
  - sample GBP 12 paid report visible second
  - paid pipeline later
- Added `Design/module-design.md` as the implementation design layer.
- Chose email capture with lightweight account creation for the free qualification flow.
- Confirmed no outbound email is needed for the first free version.
- Defined the free qualification external-call shape:
  - DataForSEO ranked keyword evidence
  - DataForSEO on-page/page evidence
  - one LLM evidence interpretation call
  - code-owned scoring and final qualification assembly
- Cleaned the repo for a future public GitHub push:
  - removed credential scratch file
  - reduced raw sample data
  - moved experimental scripts into ignored archive
  - created a public README
- Split public build tracking from private learning tracking.
- Designed the Module 1 ERD for the free qualification flow.
- Replaced the stale DDL with the seven-table Module 1 schema.
- Applied the new schema locally to the `growthmap` database.
- Connected and pushed the cleaned public repo to GitHub.
- Chose a two-video split:
  - APP1.3: product flow to database schema
  - APP1.4: first free qualification endpoint
- Started the new `app/` package structure:
  - root `main.py` is now a compatibility wrapper
  - real app code starts under `app/`
  - qualification precheck code is partially started

Decisions:

- The free result is SEO-opportunity only.
- Rendered UX, conversion-path readiness, outreach copy and the full pitch-ready report stay in the paid layer.
- The LLM may classify/group keyword evidence and summarize observed signals.
- Code owns the deterministic score, outcome and final guardrails.
- Provider/API failures must not become `weak_prospect`; missing core evidence should become `inconclusive` or a limited result.
- Do not run expensive DataForSEO/LLM calls before email intent.
- The first endpoint is `POST /qualify/precheck` and should be stateless.

Next:

- Finish `POST /qualify/precheck`.
- Record APP1.3 as a short database-design walkthrough.
- Record APP1.4 tomorrow around the first endpoint flow.

## 2026-06-22

Objective:

- Validate the qualification-first GrowthMap direction and paid report value.

Completed:

- Froze GrowthMap V1 as SEO Opportunity plus Conversion-Path Readiness.
- Validated the Mill Hill Dental free qualification experiment.
- Built and reviewed the Mill Hill Dental paid-report experiment.
- Accepted the paid report shape as useful enough to test commercially.
- Marked the old schema draft as unsafe to apply without replacement.

Key artifacts:

- `Ideation/Reports/qualification-millhilldentist-2026-06-22.md`
- `Ideation/Reports/paid-pipeline-millhilldentist-2026-06-22.json`
- `Ideation/Reports/paid-report-millhilldentist-2026-06-22.md`

## 2026-06-14 to 2026-06-17

Objective:

- Build the first FastAPI/Postgres/DataForSEO learning slices.

Completed:

- Built the first FastAPI endpoint scaffold.
- Practised Pydantic request/response models.
- Inserted request data into Postgres.
- Used `RETURNING id` to read inserted row IDs.
- Made the first DataForSEO calls.
- Learned the initial provider response shape and Basic Auth flow.

These early slices are historical learning context. The product direction has since been superseded by the qualification-first V1 contract in `Design/design.md`.
