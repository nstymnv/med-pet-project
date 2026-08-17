with source as (
	select * from {{ source('faers_db', 'reports') }}
),

normalized as(
	select
	safetyreportid as report_id,
	version,
	try_to_date(to_varchar(receiptdate, 'YYYYMMDD') as receipt_date,
	try_to_date(to_varchar(transmissiondate), 'YYYYMMDD') as transmission_date,
	country as source_country,
	occurcountry as occurrence_country,
	reporttype as report_type,
	try_cast(serious as int) as serious,
	try_cast(congenital_anomaly as int) as congenital_anomaly,
	try_cast(death as int) as death,
	try_cast(disabling as int) as disabling,
	try_cast(hospitalization as int) as hospitalization,
	try_cast(lifethreatening as int) as lifethreatening,
	try_cast(other_serious as int) as other_serious,
	try_cast(fulfillexpeditecriteria as int) as fulfill_expedite_criteria,
	try_cast(duplicate as int) as duplicate,
	duplicate_numb,
	duplicate_source,
	authoritynumb as authority_number,
	companynumb as company_number
from source 
),

standardized as(
	select
	report_id,
	version,
	receipt_date,
	transmission_date,
	source_country,
	occurence_country,
	report_type,
	case
		when serious = 1 then "yes"
		when serious = 2 then "no",
	congenital_anomaly,
	death,
	disabling,
	hospitalization,
	lifethreatening,
	other_serious,
	fulfill_expedit_criteria,
	duplicate,
	duplicate_numb,
	duplicate_source,
	authority_number,
	company_number
	from normalized
).

final as (
	select
	s.* EXCLUDE source_country AND occurence_country,
	c.country_code as source_country,
	c.country_code as occurence_country
	from standardized s
	left join country_mapping c
	on c.country_code = s.source_country
	left join country_mapping c
	on c.country_cod = s.occurence_country
)
select * from final