{{ config(
    materialized='table',
    schema='intermediate'
) }}

WITH ranked_versions AS (

    SELECT *
    FROM {{ ref('stg_reports') }}

    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY report_id, version
        ORDER BY transmission_date DESC
    ) = 1

),

deduplicated AS (

    SELECT

        report_id,
        MAX(version) AS version,
        MAX_BY(receipt_date, version) AS receipt_date,
        MAX_BY(transmission_date, version) AS transmission_date,
		
        MAX_BY(
            source_country,
            IFF(source_country IS NOT NULL, version, NULL)
        ) AS source_country,

        MAX_BY(
            occurrence_country,
            IFF(occurrence_country IS NOT NULL, version, NULL)
        ) AS occurrence_country,

        MAX_BY(
            report_type,
            IFF(report_type IS NOT NULL, version, NULL)
        ) AS report_type,

        MAX_BY(
            serious,
            IFF(serious IS NOT NULL, version, NULL)
        ) AS serious,

        MAX_BY(
            congenital_anomaly,
            IFF(congenital_anomaly IS NOT NULL, version, NULL)
        ) AS congenital_anomaly,

        MAX_BY(
            death,
            IFF(death IS NOT NULL, version, NULL)
        ) AS death,

        MAX_BY(
            disabling,
            IFF(disabling IS NOT NULL, version, NULL)
        ) AS disabling,

        MAX_BY(
            hospitalization,
            IFF(hospitalization IS NOT NULL, version, NULL)
        ) AS hospitalization,

        MAX_BY(
            lifethreatening,
            IFF(lifethreatening IS NOT NULL, version, NULL)
        ) AS lifethreatening,

        MAX_BY(
            other_serious,
            IFF(other_serious IS NOT NULL, version, NULL)
        ) AS other_serious,

        MAX_BY(
            fulfill_expedite_criteria,
            IFF(fulfill_expedite_criteria IS NOT NULL, version, NULL)
        ) AS fulfill_expedite_criteria,

        MAX_BY(
            duplicate_flag,
            IFF(duplicate_flag IS NOT NULL, version, NULL)
        ) AS duplicate_flag,

        MAX_BY(
            duplicate_numb,
            IFF(duplicate_numb IS NOT NULL, version, NULL)
        ) AS duplicate_numb,

        MAX_BY(
            duplicate_source,
            IFF(duplicate_source IS NOT NULL, version, NULL)
        ) AS duplicate_source,

        MAX_BY(
            authority_number,
            IFF(authority_number IS NOT NULL, version, NULL)
        ) AS authority_number,

        MAX_BY(
            company_number,
            IFF(company_number IS NOT NULL, version, NULL)
        ) AS company_number

    FROM ranked_versions

    GROUP BY report_id

)

SELECT *
FROM deduplicated