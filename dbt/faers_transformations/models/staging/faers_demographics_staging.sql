{{ config(
	materialized='table',
	schema='staging'
) }}

with source as (
	select *
	from { source('faers_db', 'demographics') }}
),

normalized as (
	select 
	safetyreportid as report_id,
	try_cast(age_group as int) as age_group,
	try_cast(onset_age as int) as onset_age,
	try_cast(onset_age_unit as int) as age_unit_code,
	try_cast(sex as int) as sex_code,
	try_cast(weight as float) as weight_kg,

from source
),

standardized as (
	select
	report_id,
	case
		when age_group = 1 then "neonate"
		when age_group = 2 then "infant"
		when age_group = 3 then "child"
		when age_group = 4 then "adolescent"
		when age_group = 5 then "adult"
		when age_group = 6 then "elderly"
		end as age_group,
	onset_age,
	age_unit_code,
	case
		when sex_code = 0 then "unknown"
		when sex_code = 1 then "male"
		when sex_code = 2 then "female"
		end as sex_code,
	weight_kg
	
	from normalized
),

final as (
	select 
	s.* EXCLUDE age_unit_code,
	t.unit_name as age_unit
	from standardized s
	left join {{ ref('time_unit_code_mapping') }} t
	on t.unit_code = s.age_unit_code
),

select * from final
