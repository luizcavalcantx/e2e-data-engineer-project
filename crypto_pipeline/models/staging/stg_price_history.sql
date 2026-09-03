with source as (
    select * from {{ source('raw', 'price_history') }}
),

flattened as (
    select distinct
        coin_id,
        TO_TIMESTAMP_NTZ(f.value[0]::NUMBER, 3) as date_timestamp,
        f.value[1] as price_value,
        market_caps[f.index][1] as market_caps_value,
        total_volumes[f.index][1] as total_volume_value,
        current_timestamp() as loaded_at
    from source,
    lateral flatten(input => prices) f
),

final as (
    select *
    from flattened
    qualify row_number() over (partition by coin_id,date_timestamp order by loaded_at desc) = 1
)

select *
from final