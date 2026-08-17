with source as (
	select * from {{ source('faers_db', 'reaction') }}
),

normalized as(
	select 
	safetyreportid as report_id,
	try_cast(reaction as string),
	try_cast(meddra_version as float),
	try_cast(outcome as int)
	from source
),

standardized as (
	select
	report_id,
	reaction,
	meddra_version,
	case
		when outcome = 1 then "recovered/resolved"
		when outcome = 2 then "recovering/resolving"
		when outcome = 3 then "not recovered/not resolved"
		when outcome = 4 then "recovered/resolved with sequelae"
		when outcome = 5 then "fatal"
		when outcome = 6 then "unknown"
		end as outcome
	from normalized
),

final as (
	select * from standardized
)

select * from final
