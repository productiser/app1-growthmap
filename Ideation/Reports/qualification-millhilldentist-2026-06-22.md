# GrowthMap Qualification Experiment: Mill Hill Dental

Date: 2026-06-22  
Target: https://millhilldentist.co.uk/  
Market assumption: United Kingdom / English  
Status: Experimental result, not a validated customer score

## Pipeline Executed

1. DataForSEO Labs `ranked_keywords`
2. DataForSEO On-Page Instant Pages
3. Google PageSpeed Insights
4. Deterministic score
5. OpenAI inference restricted to short qualification wording

## Search Visibility Evidence

- Total ranked keywords reported: 162
- Estimated organic traffic reported: 935.06
- Returned sample size: 20 keywords
- Initially classified non-branded terms: 18
- Initially classified commercial non-branded terms: 18
- Initially classified non-branded top-10 terms: 0

Examples returned:

| Keyword | Position | Search volume | CPC | Initial classification issue |
|---|---:|---:|---:|---|
| dentistry in london | 90 | 6,600 | $12.11 | Relevant commercial |
| dentistry london | 96 | 6,600 | $12.11 | Relevant commercial |
| invisalign aligners london | 86 | 1,900 | $29.64 | Relevant commercial |
| nearby dentist | 45 | 1,900 | $7.56 | Relevant commercial |
| dental clinic in london uk | 114 | 1,300 | $8.33 | Relevant commercial |
| millway practice | 24 | 1,300 | $5.77 | Likely another business brand |
| mckennell dental practice | 44 | 1,000 | $4.76 | Another business brand |
| parkhill dental | 54 | 1,000 | $4.51 | Likely another business brand |

The experiment incorrectly treated some other-business brand terms as useful non-branded demand. Relevance classification must happen before scoring.

## On-Page Evidence

- HTTP status: 200
- HTTPS: yes
- Broken page: no
- Redirect: no
- Title: `Dentist in North London | Mill Hill Dental Practice`
- Title length: 51
- Meta description: present
- Canonical: `https://millhilldentist.co.uk/`
- H1 found: no
- Fetch duration reported: 465 ms
- `robots.txt`: normal crawling allowed, with WordPress administration paths excluded

## Technical Evidence

Google PageSpeed returned:

```text
HTTP 429 Too Many Requests
```

The qualification continued using the successful fetch and On-Page evidence.

Product implication:

> PageSpeed must be optional evidence. Provider rate limiting must not turn a prospect into a weak score or fail the whole qualification.

## Initial Experimental Score

```text
demand evidence:       30/30
SEO headroom:          32/40
technical feasibility: 24/30
total:                 86/100
classification:        good_prospect
```

This score is overstated and must not be used as a validated customer result.

Reasons:

- competitor-brand keywords inflated demand evidence
- keyword relevance was not classified before scoring
- visual experience was not measured
- PageSpeed evidence was unavailable

## LLM Output

Headline:

> Good SEO Prospect

Explanation:

> The site shows commercial non-branded keyword visibility, with sampled rankings outside the top 10 and one basic homepage on-page gap. This is based only on the submitted homepage, with UK and English search data assumed from the .co.uk domain, and does not identify missed keyword demand.

The LLM followed the supplied facts, but the facts included an overstated deterministic score. This confirms that restricting the LLM does not compensate for weak upstream classification.

## Visual Review From Supplied Screenshot

The screenshot showed problems not captured by the API-only checks:

- the navigation occupied most of the visible viewport
- links wrapped across many rows
- visual hierarchy was weak
- main page content was pushed below the navigation
- no clear treatment proposition was visible above the fold

This is a strong prospecting signal because it affects the visible user experience, but it is not proven by title/H1/PageSpeed metadata alone.

The product must distinguish:

```text
technical feasibility != good rendered experience
```

A visual or rendered-layout signal must be tested before it contributes to the qualification score.

## Actual Provider Cost

| Provider call | Cost |
|---|---:|
| DataForSEO ranked keywords | $0.012000 |
| DataForSEO On-Page | $0.000125 |
| DataForSEO total | $0.012125 |
| Google PageSpeed | No direct request charge; request rate-limited |
| OpenAI inference | Not exposed by the current SDK result capture |

## Defensible Interim Qualification

> Promising SEO prospect

> The site already appears for commercially valuable dental searches, but several relevant sampled rankings remain outside the top results. A deeper report should verify keyword relevance and the site's visibly weak page experience before recommending a pitch.

## Required Corrections

1. Classify other-company brand terms separately.
2. Score only relevant commercial and informational queries.
3. Add a tested rendered-experience signal.
4. Keep PageSpeed optional.
5. Recalculate the score after these changes.
