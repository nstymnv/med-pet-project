{{ config(
    materialized='table',
    schema='intermediate'
) }}

WITH ranked_versions AS (

    SELECT *
    FROM {{ ref('stg_demographics') }}

    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY report_id, version
        ORDER BY version DESC
    ) = 1

),

deduplicated AS (

    SELECT
        report_id,
        MAX(version) AS version,

        MAX_BY(
            age_group,
            IFF(age_group IS NOT NULL, version, NULL)
        ) AS age_group,

        MAX_BY(
            onset_age,
            IFF(onset_age IS NOT NULL, version, NULL)
        ) AS onset_age,

        MAX_BY(
            age_unit,
            IFF(age_unit IS NOT NULL, version, NULL)
        ) AS age_unit,

        MAX_BY(
            sex,
            IFF(sex IS NOT NULL, version, NULL)
        ) AS sex,

        MAX_BY(
            weight_kg,
            IFF(weight_kg IS NOT NULL, version, NULL)
        ) AS weight_kg

    FROM ranked_versions

    GROUP BY report_id

)

SELECT *
FROM deduplicated