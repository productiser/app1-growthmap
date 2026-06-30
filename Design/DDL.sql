-- GrowthMap Module 1 schema
-- Created: 2026-06-28
-- Status: Review draft for the free qualification module.
--
-- This schema replaces the older local-visibility/report-token draft.
-- It models only the first production slice:
-- business URL precheck -> email gate -> free SEO prospect qualification.
--
-- Paid reports, checkout, token ledger, dashboard history, browser capture,
-- opportunity candidates and final paid-report generation are intentionally
-- not included yet.


-- ===== USERS AND FREE ALLOWANCE =====

CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    email TEXT NOT NULL UNIQUE,
    display_name TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- One row per user per allowance month.
-- period_month should be stored as the first day of the month, for example
-- 2026-06-01.
CREATE TABLE monthly_usage (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    period_month DATE NOT NULL,
    free_qualification_used_count INTEGER NOT NULL DEFAULT 0
        CHECK (free_qualification_used_count >= 0),
    free_qualification_limit INTEGER NOT NULL DEFAULT 3
        CHECK (free_qualification_limit >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, period_month)
);

CREATE INDEX monthly_usage_user_period_idx
    ON monthly_usage(user_id, period_month);


-- ===== REUSABLE PROSPECT IDENTITY =====

-- A prospect is the reusable domain identity being checked.
-- It is not owned by one user or one request.
CREATE TABLE prospects (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    normalized_domain TEXT NOT NULL UNIQUE,
    first_submitted_url TEXT NOT NULL,
    country_code TEXT NOT NULL,
    language_code TEXT NOT NULL,
    first_seen_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX prospects_normalized_domain_idx
    ON prospects(normalized_domain);


-- ===== USER-OWNED QUALIFICATION REQUESTS =====

-- A qualification request is made by one user and linked to one prospect.
-- The prospect may be newly created or reused by normalized domain.
CREATE TABLE qualification_requests (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    prospect_id BIGINT NOT NULL REFERENCES prospects(id),
    -- Used to fetch the result page before full login/session support exists.
    public_access_token TEXT NOT NULL UNIQUE,
    submitted_url TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'running',
                'completed',
                'failed'
            )
        ),
    outcome TEXT
        CHECK (
            outcome IS NULL
            OR outcome IN (
                'good_prospect',
                'possible_prospect',
                'weak_prospect',
                'inconclusive'
            )
        ),
    demand_score NUMERIC(5, 2)
        CHECK (demand_score IS NULL OR demand_score BETWEEN 0 AND 100),
    seo_headroom_score NUMERIC(5, 2)
        CHECK (seo_headroom_score IS NULL OR seo_headroom_score BETWEEN 0 AND 100),
    technical_feasibility_score NUMERIC(5, 2)
        CHECK (
            technical_feasibility_score IS NULL
            OR technical_feasibility_score BETWEEN 0 AND 100
        ),
    total_score NUMERIC(5, 2)
        CHECK (total_score IS NULL OR total_score BETWEEN 0 AND 100),
    headline TEXT,
    explanation TEXT,
    verified_signals JSONB,
    limitations JSONB,
    used_cached_evidence BOOLEAN NOT NULL DEFAULT FALSE,
    failure_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ
);

CREATE INDEX qualification_requests_user_created_idx
    ON qualification_requests(user_id, created_at DESC);

CREATE INDEX qualification_requests_prospect_created_idx
    ON qualification_requests(prospect_id, created_at DESC);

CREATE INDEX qualification_requests_status_idx
    ON qualification_requests(status);

CREATE INDEX qualification_requests_public_access_token_idx
    ON qualification_requests(public_access_token);


-- ===== EXTERNAL PROVIDER CALLS =====

-- Provider calls include DataForSEO and OpenAI calls.
-- Each call is about one prospect and is triggered by one qualification request.
CREATE TABLE provider_calls (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    qualification_request_id BIGINT NOT NULL REFERENCES qualification_requests(id),
    prospect_id BIGINT NOT NULL REFERENCES prospects(id),
    provider TEXT NOT NULL,
    stage TEXT NOT NULL,
    endpoint TEXT,
    model TEXT,
    provider_task_id TEXT,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (
            status IN (
                'pending',
                'running',
                'completed',
                'failed'
            )
        ),
    request_json JSONB,
    response_json JSONB,
    cost_amount NUMERIC(12, 6)
        CHECK (cost_amount IS NULL OR cost_amount >= 0),
    cost_currency CHAR(3),
    input_tokens INTEGER
        CHECK (input_tokens IS NULL OR input_tokens >= 0),
    output_tokens INTEGER
        CHECK (output_tokens IS NULL OR output_tokens >= 0),
    error_message TEXT,
    started_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX provider_calls_qualification_request_idx
    ON provider_calls(qualification_request_id, stage);

CREATE INDEX provider_calls_prospect_idx
    ON provider_calls(prospect_id, stage);

CREATE INDEX provider_calls_status_idx
    ON provider_calls(status);


-- ===== PARSED SEO EVIDENCE =====

-- Parsed ranked-keyword rows are public evidence about the prospect.
-- They also point back to the provider call that produced them.
CREATE TABLE ranked_keywords (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    prospect_id BIGINT NOT NULL REFERENCES prospects(id),
    provider_call_id BIGINT NOT NULL REFERENCES provider_calls(id),
    keyword TEXT NOT NULL,
    ranking_url TEXT,
    ranking_position INTEGER
        CHECK (ranking_position IS NULL OR ranking_position > 0),
    search_volume INTEGER
        CHECK (search_volume IS NULL OR search_volume >= 0),
    cpc NUMERIC(12, 4)
        CHECK (cpc IS NULL OR cpc >= 0),
    competition NUMERIC(8, 4)
        CHECK (competition IS NULL OR competition >= 0),
    classification TEXT,
    classification_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX ranked_keywords_prospect_idx
    ON ranked_keywords(prospect_id);

CREATE INDEX ranked_keywords_provider_call_idx
    ON ranked_keywords(provider_call_id);

CREATE INDEX ranked_keywords_classification_idx
    ON ranked_keywords(classification);


-- Parsed on-page/page-check rows are public evidence about the prospect.
-- Free V1 usually checks the submitted page or homepage.
CREATE TABLE page_checks (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    prospect_id BIGINT NOT NULL REFERENCES prospects(id),
    provider_call_id BIGINT NOT NULL REFERENCES provider_calls(id),
    checked_url TEXT NOT NULL,
    final_url TEXT,
    http_status INTEGER
        CHECK (http_status IS NULL OR http_status BETWEEN 100 AND 599),
    https_enabled BOOLEAN,
    title TEXT,
    meta_description TEXT,
    h1 TEXT,
    canonical_url TEXT,
    indexable BOOLEAN,
    noindex BOOLEAN,
    redirected BOOLEAN,
    obvious_broken_page BOOLEAN,
    fetch_duration_ms INTEGER
        CHECK (fetch_duration_ms IS NULL OR fetch_duration_ms >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX page_checks_prospect_idx
    ON page_checks(prospect_id);

CREATE INDEX page_checks_provider_call_idx
    ON page_checks(provider_call_id);

CREATE INDEX page_checks_checked_url_idx
    ON page_checks(checked_url);


-- ===== REVIEW NOTES =====

-- Core relationships:
--
-- users 1:N qualification_requests
-- users 1:N monthly_usage
--
-- prospects 1:N qualification_requests
-- prospects 1:N provider_calls
-- prospects 1:N ranked_keywords
-- prospects 1:N page_checks
--
-- qualification_requests 1:N provider_calls
--
-- provider_calls 1:N ranked_keywords
-- provider_calls 1:N page_checks
--
-- Provider-call costs are stored on provider_calls.
-- Qualification-level cost is calculated by summing provider_calls for one
-- qualification_request_id.
--
-- Monthly free allowance is stored in monthly_usage, not on users, because
-- usage resets by month.
--
-- A generic recent-activity UI can be derived from completed qualification
-- requests, for example "Qualification completed 3 minutes ago".
-- Do not expose URL, business name, location or outcome in that public element.
-- No separate table is needed for this in V1.
