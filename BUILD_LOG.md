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

## 2026-09-02

Objective:

- Recovery/travel continuity check-in before moving development from the mini to a laptop.
- Preserve the current GrowthMap state in git without starting a new sprint.

Completed:

- Reconfirmed the current resume point: the free-qualification LLM provider call is stored, token/cost accounting is wired, and the next backend slice is parsing/validating the LLM content.
- Confirmed local Postgres is accepting connections on `localhost:5432`.
- Added laptop setup notes and a placeholder `.env.example` so the repo can be cloned and bootstrapped away from the mini.
- Documented the Mini DB over Tailscale option using Mini Tailscale IP `100.78.142.13`.
- Tightened Mini Postgres Tailscale DB access to `growthmap`/`ptalur` over `100.64.0.0/10` with password auth, then verified `select 1` through `100.78.142.13`.
- Kept the zero-byte local `usage` scratch file out of git.

Verified:

- `./.venv/bin/python -m compileall app tests`
- `pg_isready -h localhost -p 5432`
- DB `select 1` through localhost app `DATABASE_URL`
- DB `select 1` through Mini Tailscale IP `100.78.142.13`

Next:

- On the laptop, clone the repo, run `uv sync`, copy `.env.example` to `.env`, create the `growthmap` database, and apply `Design/DDL.sql`.
- If using the Mini database while travelling, keep Tailscale connected and set laptop `DATABASE_URL` to the Mini DB at `100.78.142.13`.
- Resume GrowthMap from `parse_llm_content()`: inspect the malformed `choices[0].message.content` JSON before deciding between prompt/schema hardening, parser error handling, or validation/storage.
- Keep the first resumed session as a small continuity slice, not a broad refactor.

## 2026-07-26

Objective:

- Recovery-aware progress session after a difficult week, continuing into next week.
- Keep the build slice small: tighten the stored OpenRouter `qualification_inference` usage fields before response parsing.
- Prepare one separate short video from the current backend lesson; video planning/recording is not counted as focused GrowthMap build time.

Time log:

- Start: 13:42 IST
- Stop: 14:40 IST
- Back: 15:45 IST
- Stop: 19:13 IST due to home-move interruption
- Focused time: approximately 1.0 hour for the earlier verified backend slice; later resumed block was interrupted and not finalized as focused build time

Completed:

- Review the current LLM provider-call response shape.
- Codex added a small token-accounting cleanup before the user clarified backend coding should stay user-led unless explicitly delegated.
- Confirmed `LLMInferenceResponse.cost` already reads OpenRouter cost from `response_json["usage"]["cost"]`.
- Added `LLMInferenceResponse.input_tokens` and `LLMInferenceResponse.output_tokens` for `usage.prompt_tokens` and `usage.completion_tokens`.
- Updated provider-call completion persistence so `input_tokens` and `output_tokens` can be stored on `provider_calls`.
- Added a plain module test for OpenRouter usage-field extraction.
- User ran a begin/end DB smoke check with `provider_calls.id = 10` and confirmed `status`, raw `response_json->'usage'`, `cost_amount`, `input_tokens` and `output_tokens` are all present.
- Resumed LLM content parsing and clarified the response-shape concept: Postgres JSONB becomes the outer Python dict, while `choices[0].message.content` is a JSON-looking string that still needs `json.loads`.

Verified:

- `./.venv/bin/python -m compileall app tests`
- `./.venv/bin/python -m tests.TestLLMInferenceClient`
- User DB smoke check for `provider_calls.id = 10`

Next:

- Resume by inspecting the malformed LLM content string around `json.loads(content_str)` failure: `JSONDecodeError: Expecting ',' delimiter: line 110 column 3 (char 4755)`.
- After the malformed-content issue is understood, decide whether to harden the prompt, add parser error handling, or use a more constrained response format before validation/storage.
- Use APP1.9 as the short-video recording target: raw HTTP first, provider-call logging, and code-owned persistence around LLM responses.

## 2026-07-24

Objective:

- Mini session during house-move constraints.
- Tighten the stored OpenRouter provider-call cost/token handling before moving to response parsing.

Time log:

- Start: 18:43 IST

Next:

- Update `LLMInferenceResponse.cost` to read cost from `response_json["usage"]["cost"]`.
- Consider adding token extraction from `usage.prompt_tokens` and `usage.completion_tokens`.
- Re-run compile/import checks and decide whether the DB update helper needs token fields today or tomorrow.

## 2026-07-22

Objective:

- Continue the bounded `qualification_inference` provider-call persistence slice.
- Use the next hour for code-first GrowthMap work after publishing APP1.8 separately.

Time log:

- Non-focused YouTube work: APP1.8 short published; not counted in GrowthMap focused build time.
- Start: 16:13 IST
- Stop: 17:09 IST
- Focused time: approximately 0.9 hours

Completed:

- Added a live smoke script for `qualification_inference` provider-call persistence.
- Recovered local Postgres from a stale `postmaster.pid` restart issue.
- Ran the live OpenRouter inference path and confirmed `provider_calls.id = 7` was stored with `status = completed`, request JSON and response JSON.
- Found and fixed the smoke-test DB-read issue where Postgres `NUMERIC` values returned as Python `Decimal` were not JSON serializable.
- Inspected the stored OpenRouter wrapper enough to confirm the actual model content is nested under `choices[0].message.content`.

Verified:

- `uv run python -m compileall app tests`
- Latest `provider_calls` row for `stage = 'qualification_inference'` has request and response JSON stored.

Next:

- Update `LLMInferenceResponse.cost` to read OpenRouter cost from `response_json["usage"]["cost"]` instead of a top-level `cost`.
- Consider storing `input_tokens` and `output_tokens` from `usage.prompt_tokens` and `usage.completion_tokens`.
- Then decide whether to parse the LLM response content next or first clean up return shapes and error handling.

## 2026-07-21

Objective:

- Continue wiring the bounded `qualification_inference` LLM/provider-call slice.

Time log:

- Focused time: approximately 0.75 hours

Completed:

- Worked on the code path for saving the `qualification_inference` LLM request/response through the provider-call boundary.
- Did not update Codex live during the session.

Next:

- Review the current diff, then compile/import-check before deciding on a live LLM smoke test.

## 2026-07-18

Objective:

- Resume after a long-ish gap and make progress on the bounded qualification LLM/provider-call slice.
- Keep a separate small YouTube recording block if the explanation is clear enough.

Time log:

- Non-focused check-in: 18:22 IST
- Start: 19:27 IST
- Stop: 20:09 IST
- Focused time: approximately 0.7 hours

Completed:

- Start with a short cumulative quiz.
- Reviewed the class method boundary for `LLMInferenceClient`.
- Fixed the public `run_qualification_inference` client method so the service calls a clear method and the client calls `_post` internally.
- Fixed the mistaken explicit `self` argument inside the client payload builder call.

Verified:

- `./.venv/bin/python -m compileall app tests`
- `./.venv/bin/python -c "from app.qualifications.service import run_qualification_inference; from app.qualifications.llm_inference_client import LLMInferenceClient; print('imports ok')"`

Next:

- Save the `qualification_inference` LLM request/response in `provider_calls`.
- Then decide whether to run a live LLM smoke test.
- Plan one small YouTube recording block separately from focused build time.

## 2026-07-14

Objective:

- Resume after family-commitment break and plan the bounded provider LLM call for keyword classification plus evidence summary.
- Record a short video if the plan is clear enough to explain cleanly.

Time log:

- Start: 16:40 IST
- Break: approximately 3 hours during the session
- Stop: 19:40 IST
- Focused time: not finalized; exclude the 3-hour break from any later total

Session reminder:

- End each coding day by checking in the finished slice or explicitly noting why it is not ready to check in.

Completed:

- Planned the `qualification_inference` LLM contract.
- Added the initial LLM inference client structure and system prompt.
- Updated the module design so the LLM can recommend `weak_prospect` or `possible_prospect` with advisory confidence while code still validates and persists deliberately.

Verified:

- `./.venv/bin/python -m compileall app tests`
- `./.venv/bin/python -c "from app.qualifications.service import run_qualification_inference; print('imports ok')"`

Next:

- Save the `qualification_inference` provider call, fix the live client call boundary, and test the LLM response path properly.

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
