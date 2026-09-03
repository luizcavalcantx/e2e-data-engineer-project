"""
Check S3 bucket volume (total size, object count, and per-partition breakdown)
using boto3 and credentials from .env.

Usage:
    python check_s3_volume.py
"""

import os
from collections import defaultdict

import boto3
from dotenv import load_dotenv

load_dotenv()

BUCKET_NAME = "codeup-crypto-pipeline-luiz"
PREFIXES = [
    "raw/coins_markets/",
    "raw/coins_info/",
    "raw/price_history/",
]


def human_readable_size(size_bytes: float) -> str:
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} PB"


def summarize_prefix(s3_client, bucket: str, prefix: str) -> None:
    paginator = s3_client.get_paginator("list_objects_v2")
    total_size = 0
    total_objects = 0
    files_per_date = defaultdict(int)

    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
        for obj in page.get("Contents", []):
            total_size += obj["Size"]
            total_objects += 1

            # Extract dt=YYYY-MM-DD/ from the key, if present
            key_parts = obj["Key"].split("/")
            date_part = next((p for p in key_parts if p.startswith("dt=")), None)
            if date_part:
                files_per_date[date_part] += 1

    print(f"\n--- {prefix} ---")
    print(f"Total objects: {total_objects}")
    print(f"Total size: {human_readable_size(total_size)}")

    if files_per_date:
        print("Files per date:")
        for date_part in sorted(files_per_date):
            print(f"  {date_part}: {files_per_date[date_part]} file(s)")

    return total_size, total_objects


def main():
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name="us-east-1",
    )

    print(f"Checking bucket: {BUCKET_NAME}")

    grand_total_size = 0
    grand_total_objects = 0

    for prefix in PREFIXES:
        size, objects = summarize_prefix(s3_client, BUCKET_NAME, prefix)
        grand_total_size += size
        grand_total_objects += objects

    print("\n=== GRAND TOTAL ===")
    print(f"Total objects: {grand_total_objects}")
    print(f"Total size: {human_readable_size(grand_total_size)}")


if __name__ == "__main__":
    main()