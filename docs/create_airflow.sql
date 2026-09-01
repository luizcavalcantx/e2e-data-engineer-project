use database crypto_pipeline;

create role airflow_role;
grant role airflow_role to role sysadmin;

create user airflow_loader
    password = 'airflowStrong123'
    default_role = airflow_role
    default_warehouse = crypto_pipeline_wh
    must_change_password = false;

grant role airflow_role to user airflow_loader;

grant usage on database crypto_pipeline to role airflow_role;
grant usage on schema crypto_pipeline.RAW to role airflow_role;
grant usage on warehouse crypto_pipeline_wh to role airflow_role;
grant usage on stage raw.crypto_s3_stage to role airflow_role;

grant INSERT on all tables in schema crypto_pipeline.raw to role airflow_role;
grant INSERT on future tables in schema crypto_pipeline.raw to role airflow_role;