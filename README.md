# GrowthMap

GrowthMap is App 1 in my build-in-public AI engineering series.

The product helps aspiring and early-stage SEO freelancers qualify whether a business is worth approaching, then later generate a focused, evidence-backed prospect report.

Current V1 direction:

```text
business URL
-> cheap URL/domain precheck
-> email gate
-> free SEO opportunity qualification
-> sample GBP 12 pitch-ready report
-> paid report pipeline later
```

## Status

This repository is in early build.

The current source of truth is the design documentation:

- `Design/design.md` - frozen V1 product contract
- `Design/module-design.md` - module flow, launch sequence and table responsibility map
- `BUILD_LOG.md` - public dated build log

The Python app is still being refactored toward the qualification-first flow. Some older experimental code has been archived locally and is not part of the public repo.

## What GrowthMap V1 Will Do

The first production slice will ship the free qualification flow:

- capture email and business URL
- run only cheap URL/domain validation before email capture
- require email before expensive provider or LLM calls
- auto-create or reuse a lightweight user
- normalize the prospect URL/domain
- check monthly free qualification allowance
- fetch or reuse public SEO evidence
- call DataForSEO for ranked keyword evidence
- call DataForSEO for basic on-page evidence
- call an LLM to classify/group keyword evidence and summarize observed signals
- calculate the qualification score in code
- return a restrained qualification result
- link to a sample paid report

The free result is intentionally limited to SEO opportunity. Conversion-path readiness, rendered UX checks, screenshots, outreach wording and the full pitch-ready report belong in the paid layer.

## What Is Not Included Yet

- production database schema
- checkout or token billing
- self-serve paid report generation
- dashboard/report history
- automated email sending
- deployment configuration
- polished frontend

## Tech Stack

- Python 3.12
- FastAPI
- Pydantic
- Postgres
- DataForSEO
- OpenAI API
- uv

## Local Setup

Install dependencies:

```bash
uv sync
```

Create a local `.env` file for secrets. Do not commit it:

```bash
cp .env.example .env
```

Expected environment variables will include:

```text
DATABASE_URL=
DATAFORSEO_LOGIN=
DATAFORSEO_PASSWORD=
OPENROUTER_API_KEY=
```

Laptop setup checklist with a local laptop database:

```bash
git clone git@github.com:productiser/app1-growthmap.git
cd app1-growthmap
uv sync
cp .env.example .env
createdb growthmap
psql growthmap < Design/DDL.sql
uv run python -m compileall app tests
```

Laptop setup using the Mini database over Tailscale:

```text
DATABASE_URL=postgresql://ptalur:<password>@100.78.142.13:5432/growthmap
```

The Mini's Tailscale IP is `100.78.142.13`. Keep Tailscale connected on both
machines before running the app from the laptop.

The current local development database is Postgres 16. If Postgres looks stuck
after a cold shutdown, first check whether the server is actually running before
removing any stale `postmaster.pid`.

Run the API locally:

```bash
uv run uvicorn main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

## Repository Notes

This is a learning-first public repo. Design decisions, tradeoffs and progress notes are intentionally included where useful.

Raw secrets, local scratch files, personal content planning notes, large provider downloads and archived experiments are excluded from git.

Current resume point:

- Continue the free-qualification LLM boundary.
- `parse_llm_content()` currently reads `choices[0].message.content` and calls
  `json.loads`.
- The latest stored OpenRouter response fails parsing because the model content
  is malformed JSON near line 110 / char 4755. Inspect that exact content before
  changing the prompt, parser recovery, or validation/storage behavior.
- For travel, the laptop can use the Mini's DB over Tailscale with
  `DATABASE_URL=postgresql://ptalur:<password>@100.78.142.13:5432/growthmap`.

## License

MIT License.
