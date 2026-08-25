with source as (
    select * from {{ source('raw', 'price_history') }}
),

final as (
    select distinct
        coin_id,
        TO_TIMESTAMP_NTZ(f.value[0]::NUMBER, 3) as date_timestamp,
        round(f.value[1],2) as price_value,
        round(market_caps[f.index][1],2) as market_caps_value,
        round(total_volumes[f.index][1],2) as total_volume_value,
        current_timestamp() as loaded_at
    from source,
    lateral flatten(input => prices) f
)

select *
from final