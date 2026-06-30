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

## 2026-06-30

Objective:

- Add the database/repository slice behind `POST /qualify/start`.

Time log:

- Start: 17:27
- Break: 18:11
- Back: 18:34
- Stop:
- Focused time:
- Running total:

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
- Verified the app compiles and still exposes `/qualify/start`.

Decisions:

- Keep repository functions responsible for SQL only.
- Use parameterized SQL with tuple parameters, for example `(email,)`, instead of raw string values.

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
