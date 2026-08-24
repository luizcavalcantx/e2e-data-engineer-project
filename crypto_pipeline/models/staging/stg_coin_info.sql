with source as (
    select *
    from {{ source('raw', 'coin_info') }}
),

final as (
    select
        id as coin_id,
        symbol as symbol,
        name as name,
        categories[0]::STRING as first_category,
        links:homepage[0]::STRING as homepage_link,
        COUNTRY_ORIGIN as country_region,
        GENESIS_DATE as creation_date,
        LAST_UPDATED as last_updated,
        current_timestamp() as loaded_at
    from source
)

select *
from final