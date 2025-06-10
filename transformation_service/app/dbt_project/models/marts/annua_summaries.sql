
{{
    config(
        materialized='table',
        schema='analytics'
    )
}}

WITH income_agg AS (
    SELECT
        symbol,
        EXTRACT(YEAR FROM fiscaldateending::DATE) AS fiscal_year,
        SUM(totalrevenue) AS annual_revenue,
        SUM(netincome) AS annual_net_income
    FROM
        {{ source('raw_data', 'income_statement') }}
    GROUP BY
        symbol, fiscal_year
),
balance_agg AS (
    SELECT
        symbol,
        EXTRACT(YEAR FROM fiscaldateending::DATE) AS fiscal_year,
        AVG(totalassets) AS avg_total_assets
    FROM
        {{ source('raw_data', 'balance_sheet') }}
    GROUP BY
        symbol, fiscal_year
),
cash_flow_agg AS (
    SELECT
        symbol,
        EXTRACT(YEAR FROM fiscaldateending::DATE) AS fiscal_year,
        SUM(operatingcashflow) AS annual_operating_cash_flow
    FROM
        {{ source('raw_data', 'cash_flow') }}
    GROUP BY
        symbol, fiscal_year
)

SELECT
    co.symbol AS company_symbol,
    ia.fiscal_year,
    ia.annual_revenue,
    ia.annual_net_income,
    ba.avg_total_assets,
    cfa.annual_operating_cash_flow
FROM
    {{ ref('stg_alpha_vantage_company_overview') }} co
LEFT JOIN
    income_agg ia ON co.symbol = ia.symbol
LEFT JOIN
    balance_agg ba ON co.symbol = ba.symbol AND ia.fiscal_year = ba.fiscal_year
LEFT JOIN
    cash_flow_agg cfa ON co.symbol = cfa.symbol AND ia.fiscal_year = cfa.fiscal_year

WHERE
    ia.fiscal_year IS NOT NULL
ORDER BY
    company_symbol, fiscal_year