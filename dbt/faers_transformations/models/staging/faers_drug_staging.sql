with source as (
	select * from {{ source('faers_db', 'drug') }}
),

normalized as (
	select 
	safetyreportid as report_id,
	UPPER(TRIM(medicinalproduct)) as medicinal_product,
	UPPER(TRIM(active_substance)) as active_substance,
	try_cast(drugcharacterization as int) as drug_characterization,
	try_cast(drugindication as string) as drug_indication,
	try_cast(drugbatchnumb as int) as drug_batch_number,
	try_cast(administration_route as string),
	try_cast(dosage_amount as float),
	try_cast(dosage_unit as string),
	try_to_date(to_varchar(start_date), 'YYYYMMDD') as start_date,
	try_to_date(to_varchar(end_date), 'YYYYMMDD') as end_date,
	try_cast(duration as int) as duration,
	try_cast(duration_unit as int),
	try_cast(drugrecurreadministration as int) as drug_reccurence,
	try_cast(recurrence_action as string),
	try_cast(actiondrug as int) as taken_action,
	try_cast(drugadditional as int) as use_stopped_reduced,
	
from source
),

standardized as (
	select
	report_id,
	medicinal_product,
	active_substance,
	case
		when drug_characterization = 1 then "suspect"
		when drug_characterization = 2 then "concomitant"
		when drug_characterization = 3 then "interacting"
		end as drug_characterization,
	drug_indication,
	drug_batch_number,
	administration_route,
	dosage_amount,
	case
		when dosage_unit = "001" then "kg"
		when dosage_unit = "002" then "G"
		when dosage_unit = "003" then "Mg"
		when dosage_unit = "004" then "µg"
		end as dosage_unit,
	start_date,
	end_date,
	duration,
	duration_unit,
	case
		when drug_recurrence = 1 then "Yes"
		when drug_recurrence = 2 then "No"
		when drug_recurrence = 3 then "Unknown"
		end as drug_recurrence,
	recurrence_action,
	taken_action,
	case
		when use_stopped_reduced = 1 then "Yes"
		when use_stopped_reduced = 2 then "No"
		when use_stopped_reduced = 3 then "Doesn’t Apply"
		end as use_stopped_reduced
	from normalized	
),

final as (
	select
	s.* EXCLUDE administration_route AND duration_unit,
	a.administration_route,
	t.unit_name as duration_unit
	from standardized s
	left join {{ ref(administration_route_mapping) }} a
	on s.administration_route = a.administration_route_code
	left join {{ ref(time_unit_code_mapping)}} t
	on s.duration_unit = t.unit_code
)
select * from final
