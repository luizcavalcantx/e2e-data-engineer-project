import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

bucket_name = os.getenv("S3_BUCKET_NAME")

def upload_to_s3(local_file_path: str, s3_key:str) -> None:
    """
    Upload a local file to the S3 bucket configured in .env.

    Args:
        local_file_path: path to the file on your computer (ex: extract/tmp/coins_parquet_2026-08-19.parquet)
        s3_key: path/name the file will have inside your bucket (ex: raw/coins_markets/dt=2026-08-19/coins_parquet.parquet)
    """
    s3_client.upload_file(local_file_path, bucket_name, s3_key)
    print(f"Upload done: {local_file_path} -> s3://{bucket_name}/{s3_key}")