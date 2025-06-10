

SELECT
    symbol,
    name,
    LOWER(REPLACE(sector, ' ', '_')) AS sector,
    LOWER(REPLACE(industry, ' ', '_')) AS industry,
    country,
    currency,
    CAST(latestquarter AS DATE) AS latest_quarter,
    marketcapitalization AS market_capitalization,
    eps,
    revenuettm AS revenue_ttm,
    _load_timestamp AS loaded_at
FROM
"datagovernance_db"."raw_data"."company_overview"