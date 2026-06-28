# App 1 Ideation

Purpose: choose and scope App 1 for the Jun 14-Jun 30, 2026 build window.

Grade 1 target: FastAPI, HTTP, Postgres, Pydantic, and external API integration.

Current decision:

- App 1 is **LocalGap by Dorian Audits**: a local business discoverability tool with a competitor comparison frame.
- It shows where a business is missing local search/AI visibility compared with similar businesses in the same city.
- The first MVP is SEO/local search first, with GEO/AI visibility treated as an expansion or light beta panel.

Decision rule:

Choose scope that gives the best mix of business value, API feasibility, Grade 1 learning depth, and controllable delivery by Jun 30.

Product-shape question:

- Start as a web app/API with a backend-first MVP.
- Use the comparison report as the core artifact: target business vs visible local competitors.
- Implement token accounting in App 1; defer real payment checkout to a bridge project or later sprint.
- For each app:

   Build the smallest artifact that someone can use, send, sell, or make a decision from.

   Then move on unless demand pulls you back.
