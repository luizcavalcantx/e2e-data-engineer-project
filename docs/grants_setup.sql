show databases;
show schemas in database CRYPTO_PIPELINE;
show warehouses;
show roles;

-- creating dbt_role
create role dbt_role;

-- grant role dbt to sysadmin
grant role dbt_role to role sysadmin;
grant role dbt_role to user dbt_user;

create user dbt_user
    password = 'dbtStrong123'
    default_role = dbt_role
    default_warehouse = crypto_pipeline_wh
    must_change_password = false;

-- grant usage database and warehouse to dbt_role
grant usage on database CRYPTO_PIPELINE to role dbt_role;
grant usage on warehouse CRYPTO_PIPELINE_WH to role dbt_role;

-- grant usage on schema raw
use database crypto_pipeline;
grant usage on schema RAW to role dbt_role;

-- grant select on all tables in schema raw
grant select on all tables in schema crypto_pipeline.raw to role dbt_role;

-- grant usage and create in staging schema 
grant usage on schema crypto_pipeline.staging to role dbt_role;
grant create table on schema crypto_pipeline.staging to role dbt_role;
grant create view on schema crypto_pipeline.staging to role dbt_role;

-- grant usage and create in mart schema 
grant usage on schema crypto_pipeline.marts to role dbt_role;
grant create table on schema crypto_pipeline.marts to role dbt_role;
grant create view on schema crypto_pipeline.marts to role dbt_role;

show grant to user dbt_user;