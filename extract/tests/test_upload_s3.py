def test_upload_to_s3_calls_boto3_correctly(mocker):
    mock_client = mocker.patch("upload_s3.s3_client")
    mocker.patch("upload_s3.bucket_name", "fake-bucket")

    from upload_s3 import upload_to_s3
    upload_to_s3("tmp/fake.parquet", "raw/coins_markets/dt=2026-08-19/fake.parquet")

    mock_client.upload_file.assert_called_once_with(
        "tmp/fake.parquet",
        "fake-bucket",
        "raw/coins_markets/dt=2026-08-19/fake.parquet",
    )