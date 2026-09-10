{{ config(
    materialized='table',
    schema='intermediate'
) }}

WITH ranked_versions AS (

    SELECT *
    FROM {{ ref('stg_reaction') }}

    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY
            report_id,
            reaction,
            meddra_version
        ORDER BY version DESC
    ) = 1

),

deduplicated AS (

    SELECT *

    FROM ranked_versions

)

SELECT *
FROM deduplicated