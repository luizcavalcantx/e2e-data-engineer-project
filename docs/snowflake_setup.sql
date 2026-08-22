-- creating database ans schemas

create database if not exists CRYPTO_PIPELINE;

use database CRYPTO_PIPELINE;

create schema if not exists RAW;
create schema if not exists STAGING;
create schema if not exists MARTS;

-- creating aws storage integrantion 
create storage integration crypto_s3_integration
    type = external_stage
    storage_provider = 'S3'
    enabled = true
    storage_aws_role_arn = 'arn:aws:iam::123456789012:role/placeholder-role'
    storage_allowed_locations = ('s3://codeup-crypto-pipeline-luiz/raw/');

describe integration crypto_s3_integration;

alter storage integration crypto_s3_integration
    set storage_aws_role_arn = 'arn:aws:iam::924285052453:role/snowflake-s3-read-policy';

-- creating external stage
use database crypto_pipeline;
use schema raw;

create stage if not exists crypto_s3_stage
    storage_integration = crypto_s3_integration
    url = 's3://codeup-crypto-pipeline-luiz/raw/'
    file_format = (type = parquet);

LIST @crypto_s3_stage;

-- creating coins_market table
create table if not exists raw.coins_markets (
    id STRING,
    symbol STRING,
    name STRING,
    image STRING,
    current_price FLOAT,
    market_cap FLOAT,
    market_cap_rank INT,
    fully_diluted_valuation FLOAT,
    total_volume FLOAT,
    high_24h FLOAT,
    low_24h FLOAT,
    price_change_24h FLOAT,
    price_change_percentage_24h FLOAT,
    market_cap_change_24h FLOAT,
    market_cap_change_percentage_24h FLOAT,
    circulating_supply FLOAT,
    total_supply FLOAT,
    max_supply FLOAT,
    ath FLOAT,
    ath_change_percentage FLOAT,
    ath_date TIMESTAMP_NTZ,
    atl FLOAT,
    atl_change_percentage FLOAT,
    atl_date TIMESTAMP_NTZ,
    roi VARIANT,
    last_updated TIMESTAMP_NTZ
);

create table if not exists raw.coin_info (
    id STRING,
    symbol STRING,
    name STRING,
    categories VARIANT,
    image VARIANT,
    links VARIANT,
    country_origin STRING,
    genesis_date DATE,
    last_updated TIMESTAMP_NTZ
);

create table if not exists raw.price_history (
    coin_id STRING,
    prices VARIANT,
    market_caps VARIANT,
    total_volumes VARIANT
);

copy into raw.coins_markets
    from @crypto_s3_stage
    pattern = '.*coins_markets.*[.]parquet'
    file_format = (type = parquet)
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

copy into raw.coin_info
    from @crypto_s3_stage
    pattern = '.*coins_info.*[.]parquet'
    file_format = (type = parquet)
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

copy into raw.price_history
    from @crypto_s3_stage
    pattern = '.*price_history.*[.]parquet'
    file_format = (type = parquet)
    MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE;

select *
from crypto_pipeline.raw.coins_markets;

select *
from crypto_pipeline.raw.coin_info;

select *
from crypto_pipeline.raw.price_history;