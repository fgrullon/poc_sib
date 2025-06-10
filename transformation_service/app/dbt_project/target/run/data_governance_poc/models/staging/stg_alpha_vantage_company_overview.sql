
  create view "datagovernance_db"."analytics_curated_data"."stg_alpha_vantage_company_overview__dbt_tmp"
    
    
  as (
    

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
  );