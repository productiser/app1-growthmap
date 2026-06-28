-- SUPERSEDED GrowthMap schema proposal
-- Originally updated: 2026-06-21
-- Superseded: 2026-06-22 by the qualification-first product contract.
-- DO NOT APPLY THIS FILE.
--
-- This draft models the abandoned service/city Local Visibility flow:
-- report_requests -> local_search_runs -> local_search_results -> reports.
--
-- The replacement schema must instead model:
-- prospects/domains, free qualifications, monthly allowance usage,
-- reusable evidence, provider and LLM runs, parsed keyword/page/visual
-- evidence, opportunity candidates, paid report requests, final reports,
-- payments, and the report-token ledger.
--
-- Keep this file only as a review artifact until the replacement DDL is
-- designed manually and agreed.

-- WARNING:
  -- This schema is superseded by the 2026-06-22 qualification-first product contract.
  -- Do not apply this file.
  -- A replacement schema will be designed from Design/module-design.md.



-- ===== ACCOUNTS AND PRICING =====

CREATE TABLE account_tiers (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    description TEXT,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO account_tiers (code, name, description)
VALUES
    ('free', 'Free', 'Includes one signup token'),
    ('pay_as_you_go', 'Pay As You Go', 'User purchases report-token packs');


CREATE TABLE token_products (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    token_count INTEGER NOT NULL CHECK (token_count > 0),
    price_pence INTEGER NOT NULL CHECK (price_pence > 0),
    currency CHAR(3) NOT NULL DEFAULT 'GBP',
    display_label TEXT,
    display_order INTEGER NOT NULL DEFAULT 0,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO token_products (
    code,
    name,
    token_count,
    price_pence,
    currency,
    display_label,
    display_order
)
VALUES
    ('single', 'Single Report', 1, 1200, 'GBP', NULL, 1),
    ('starter', 'Starter Pack', 3, 3000, 'GBP', 'Most Popular', 2),
    ('value', 'Value Pack', 5, 4800, 'GBP', 'Best Value', 3);


CREATE TABLE users (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    account_tier_id BIGINT NOT NULL REFERENCES account_tiers(id),
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX users_account_tier_id_idx
    ON users(account_tier_id);


-- ===== REPORT REQUESTS =====

CREATE TABLE report_requests (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    business_name TEXT NOT NULL,
    business_url TEXT NOT NULL,
    service TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    query TEXT NOT NULL,
    location_code INTEGER,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    failure_reason TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMPTZ
);

CREATE INDEX report_requests_user_id_created_at_idx
    ON report_requests(user_id, created_at DESC);


-- One row represents one paid provider request.
CREATE TABLE local_search_runs (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    report_request_id BIGINT NOT NULL REFERENCES report_requests(id),
    provider TEXT NOT NULL DEFAULT 'dataforseo',
    endpoint TEXT NOT NULL,
    provider_task_id TEXT,
    provider_cost_usd NUMERIC(12, 6)
        CHECK (provider_cost_usd IS NULL OR provider_cost_usd >= 0),
    search_latitude NUMERIC(9, 6)
        CHECK (search_latitude IS NULL OR search_latitude BETWEEN -90 AND 90),
    search_longitude NUMERIC(9, 6)
        CHECK (search_longitude IS NULL OR search_longitude BETWEEN -180 AND 180),
    search_zoom INTEGER
        CHECK (search_zoom IS NULL OR search_zoom BETWEEN 1 AND 22),
    searched_at TIMESTAMPTZ,
    raw_response JSONB,
    status TEXT NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'completed', 'failed')),
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX local_search_runs_report_request_id_idx
    ON local_search_runs(report_request_id);


-- These are observed local-search results, not assumed competitors.
CREATE TABLE local_search_results (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    local_search_run_id BIGINT NOT NULL REFERENCES local_search_runs(id),
    business_name TEXT NOT NULL,
    position INTEGER CHECK (position IS NULL OR position > 0),
    category TEXT,
    rating NUMERIC(2, 1)
        CHECK (rating IS NULL OR rating BETWEEN 0 AND 5),
    review_count INTEGER
        CHECK (review_count IS NULL OR review_count >= 0),
    website_url TEXT,
    google_cid TEXT,
    latitude NUMERIC(9, 6)
        CHECK (latitude IS NULL OR latitude BETWEEN -90 AND 90),
    longitude NUMERIC(9, 6)
        CHECK (longitude IS NULL OR longitude BETWEEN -180 AND 180),
    is_target BOOLEAN NOT NULL DEFAULT FALSE,
    raw_result JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX local_search_results_run_position_idx
    ON local_search_results(local_search_run_id, position);

CREATE INDEX local_search_results_target_idx
    ON local_search_results(local_search_run_id, is_target);


-- One final report per request in V1.
CREATE TABLE reports (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    report_request_id BIGINT NOT NULL UNIQUE REFERENCES report_requests(id),
    primary_gap TEXT NOT NULL
        CHECK (
            primary_gap IN (
                'target_not_visible',
                'target_visible_below_competitors',
                'category_or_service_mismatch',
                'review_trust_gap',
                'no_clear_gap'
            )
        ),
    evidence_summary TEXT NOT NULL,
    actions JSONB NOT NULL,
    pitch TEXT NOT NULL,
    limitations JSONB NOT NULL,
    report_json JSONB NOT NULL,
    llm_provider TEXT,
    llm_model TEXT,
    llm_cost_usd NUMERIC(12, 6)
        CHECK (llm_cost_usd IS NULL OR llm_cost_usd >= 0),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);


-- ===== TOKENS AND PAYMENTS =====

CREATE TABLE payments (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    token_product_id BIGINT NOT NULL REFERENCES token_products(id),
    provider TEXT NOT NULL,
    provider_payment_id TEXT NOT NULL UNIQUE,
    amount_paid_pence INTEGER NOT NULL CHECK (amount_paid_pence > 0),
    currency CHAR(3) NOT NULL DEFAULT 'GBP',
    tokens_purchased INTEGER NOT NULL CHECK (tokens_purchased > 0),
    status TEXT NOT NULL
        CHECK (status IN ('pending', 'paid', 'failed', 'refunded')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    paid_at TIMESTAMPTZ
);

CREATE INDEX payments_user_id_created_at_idx
    ON payments(user_id, created_at DESC);


-- The token ledger is the source of truth for a user's balance.
-- Balance = SUM(amount) for one user.
CREATE TABLE token_ledger (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id BIGINT NOT NULL REFERENCES users(id),
    report_request_id BIGINT REFERENCES report_requests(id),
    payment_id BIGINT REFERENCES payments(id),
    amount INTEGER NOT NULL CHECK (amount <> 0),
    entry_type TEXT NOT NULL
        CHECK (
            entry_type IN (
                'signup_grant',
                'purchase',
                'report_usage',
                'refund',
                'adjustment'
            )
        ),
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CHECK (
        (entry_type = 'signup_grant' AND amount > 0)
        OR (entry_type = 'purchase' AND amount > 0)
        OR (entry_type = 'report_usage' AND amount = -1)
        OR (entry_type = 'refund' AND amount > 0)
        OR (entry_type = 'adjustment')
    ),
    CHECK (
        (entry_type = 'purchase' AND payment_id IS NOT NULL)
        OR (entry_type <> 'purchase')
    )
);

CREATE INDEX token_ledger_user_id_created_at_idx
    ON token_ledger(user_id, created_at);

CREATE UNIQUE INDEX token_ledger_one_report_charge_idx
    ON token_ledger(report_request_id)
    WHERE entry_type = 'report_usage';

CREATE UNIQUE INDEX token_ledger_one_purchase_credit_idx
    ON token_ledger(payment_id)
    WHERE entry_type = 'purchase';


-- ===== FUTURE MAP VISUAL =====

-- Search-centre coordinates are stored in local_search_runs and business
-- coordinates are stored in local_search_results so a future
-- frontend can render target and visible-business markers using Esri,
-- MapLibre, or another map provider without another DataForSEO request.


-- ===== IMPLEMENTATION RULES =====

-- 1. On signup, insert one +1 token_ledger row with entry_type='signup_grant'.
-- 2. Charge one -1 report_usage token only after a report completes successfully.
-- 3. A failed provider or LLM request must not consume a token.
-- 4. Every report lookup must verify ownership through report_requests.user_id.
-- 5. Do not use users.token_balance as the source of truth.
