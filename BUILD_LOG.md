# GrowthMap Build Log

This is the public progress log for GrowthMap.

Personal learning notes, quiz results and raw session reflections are kept outside the public repo.

## 2026-06-28

Objective:

- Return to GrowthMap after the conference and prepare the project for public development.

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

Decisions:

- The free result is SEO-opportunity only.
- Rendered UX, conversion-path readiness, outreach copy and the full pitch-ready report stay in the paid layer.
- The LLM may classify/group keyword evidence and summarize observed signals.
- Code owns the deterministic score, outcome and final guardrails.
- Provider/API failures must not become `weak_prospect`; missing core evidence should become `inconclusive` or a limited result.

Next:

- Add MIT license.
- Add a warning to the stale `Design/DDL.sql`.
- Update `main.py` header to mark it as an early scaffold.
- Design the compact replacement schema from `Design/module-design.md`.
- Only then replace/apply DDL.

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
