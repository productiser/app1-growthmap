# Research Notes

## YouTube Competitor Intel

- YouTube Data API `search.list` supports query-based search over videos/channels/playlists, with filters such as `channelId`, `q`, `order`, `publishedAfter`, `regionCode`, and `type`.
- YouTube search calls have a default daily limit of 100 `search.list` calls; pagination costs additional calls.
- Existing tools validate demand: vidIQ and TubeBuddy both sell competitor/channel analytics, keyword, SEO, and content strategy features.
- API risk: YouTube search results are useful for product demos but should not be treated as a complete or stable research dataset.

## SEO Snapshot

- PageSpeed Insights API can measure page performance and provide performance, accessibility, and SEO suggestions. It can be used without an API key for trials, but a key is recommended for frequent automated use.
- Search Console API can query owned-site search traffic grouped by dimensions like country, device, page, and query, but it requires authorization and only works for properties the user can access.
- Google Indexing API is not a general SEO indexing tool; Google says it is only for job posting or livestream video pages.
- DataForSEO offers SERP data through pay-as-you-go APIs and supports use cases like rank tracking, keyword research, competitive SERP monitoring, and search visibility analysis.

## TrustMRR / Market Signal Scan

Note: TrustMRR data is useful as directional signal, not perfect truth. Some pages show inconsistent revenue fields, so use the product pattern more than the exact number.

### YouTube Comments Downloader

Source: https://trustmrr.com/startup/youtube-comments-downloader

Observed signal:

- Product: download YouTube comments into usable data with search, filters, and export formats.
- TrustMRR shows all-time revenue around $41k, MRR around $668, and 22 active subscriptions.
- Pricing model: free credits, then pay for extra credits.
- Audience: creators, marketers, data analysts.

Product lesson:

- People pay for boring data extraction when it saves manual work.
- "Export structured data" is easier to monetize than "advice."
- Credits/tokens fit this category naturally.

App 1 implication:

- YouTube comment mining is more commercially grounded than generic "rank my video" advice.
- The AI layer should turn extracted comments into insights, not be optional.

### Produce.so

Sources:

- https://trustmrr.com/startup/produce-so
- https://produce.so/

Observed signal:

- Product: AI tool for creating long-form videos and scripts for YouTube channels.
- TrustMRR shows 57 active subscriptions and estimated MRR around $23k, though the page title also shows a lower last-30-days number.
- Pricing is high: roughly $169/mo, $329/mo, and $549/mo.
- Core promise: generate long-form scripts/videos for faceless YouTube channels, copy niches, optimize retention, and save hours.

Product lesson:

- People pay much more for production workflow than for analysis alone.
- The strongest value prop is not "tell me if this is good"; it is "help me produce the asset faster."
- AI should be central: research -> brief -> script -> production-ready output.

App 1 implication:

- If staying YouTube-adjacent, the better wedge is AI research + script/content brief generation from proven patterns.
- Do not build full video generation in App 1; media rendering, TTS, subtitles, storage, and queues are too much for Grade 1.

### AEO / AI Search Visibility

Sources:

- TrustMRR related listing on Produce.so page mentioned AEO Engine as AI agents for content visibility across Google, ChatGPT, AI Overviews, Perplexity, and similar channels.
- Business Insider reports a broader AEO wave: startups helping businesses appear in AI chatbot/search answers as discovery shifts from Google-style search to answer engines.

Product lesson:

- AI visibility is a hot market because it connects directly to business distribution.
- Buyers are businesses/marketers, not only creators.
- The workflow resembles SEO, but with AI search surfaces: track visibility, compare competitors, generate content/actions to improve presence.

App 1 implication:

- A non-YouTube alternative could be a small AEO snapshot tool: "How does my brand appear in ChatGPT/Perplexity-style answers, and what content should I create?"
- This may be business-pitchable, but live multi-engine tracking can create scope risk.

## Revenue Pattern Takeaways

The stronger AI app patterns are:

1. **Data extraction + AI analysis**: pull hard-to-get data, structure it, then summarize insights.
2. **Production workflow**: turn research into a usable deliverable, not just a score.
3. **Business visibility**: help companies/creators get found in search, YouTube, or AI answers.
4. **Credits/tokens**: works best when each job has clear compute/API cost.
5. **Narrow workflow, clear output**: CSV, report, brief, script, audit, or export.

Weak pattern:

- Generic advice tools that only say "good idea / bad idea" without producing a useful artifact.

## App 1 Direction After Market Scan

Do not stay wedded to YouTube. Use YouTube only if it gives the best Grade 1 product and story.

Best YouTube-adjacent option:

- AI YouTube Research + Script Brief Generator.
- Input: niche, channel, competitor video, or comment/source URL.
- Output: audience insights, content angle, hook, title options, outline, retention beats, and script starter.

Best broader-market option:

- AI Visibility / AEO Snapshot.
- Input: business/domain/category.
- Output: current AI-search visibility assumptions, competitor comparison, content gaps, and recommended pages/questions to answer.

Current principle:

Build an AI app that produces a concrete artifact someone can use immediately.
