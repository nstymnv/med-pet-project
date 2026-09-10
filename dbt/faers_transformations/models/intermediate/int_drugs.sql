{{ config(
    materialized='table',
    schema='intermediate'
) }}

WITH ranked_versions AS (

    SELECT *
    FROM {{ ref('stg_drugs') }}

    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY
            report_id,
            medicinal_product,
            active_substance,
            drug_characterization,
            drug_indication,
            drug_authorization_number
        ORDER BY version DESC
    ) = 1

)

SELECT *
FROM ranked_versions