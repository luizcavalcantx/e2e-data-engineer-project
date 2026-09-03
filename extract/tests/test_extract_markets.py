from datetime import date

import pytest
import requests
from pydantic import ValidationError

from extract_markets import (
    build_s3_key,
    fetch_market_data,
    save_to_parquet,
    validate_and_transform,
)


def test_fetch_market_data_success(mocker, sample_market_response):
    mock_response = mocker.Mock()
    mock_response.json.return_value = sample_market_response
    mock_response.raise_for_status.return_value = None
    mocker.patch("extract_markets.requests.get", return_value=mock_response)

    result = fetch_market_data()

    assert result == sample_market_response


def test_fetch_market_data_raises_on_http_error(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    mocker.patch("extract_markets.requests.get", return_value=mock_response)

    with pytest.raises(requests.HTTPError):
        fetch_market_data()


def test_validate_and_transform_valid_data(sample_market_response):
    df = validate_and_transform(sample_market_response)

    assert len(df) == 1
    assert df.iloc[0]["id"] == "bitcoin"


def test_validate_and_transform_rejects_malformed_data():
    # missing required fields: symbol, name, image, current_price, market_cap, total_volume
    bad_data = [{"id": "bitcoin"}]

    with pytest.raises(ValidationError):
        validate_and_transform(bad_data)


def test_save_to_parquet_creates_file(tmp_path, monkeypatch, sample_market_response):
    monkeypatch.chdir(tmp_path)  # runs the test inside a temp directory
    df = validate_and_transform(sample_market_response)
    today = date(2026, 8, 19)

    local_path = save_to_parquet(df, today)

    assert local_path == f"tmp/coins_parquet_{today}.parquet"
    assert (tmp_path / local_path).exists()


def test_build_s3_key_format():
    today = date(2026, 8, 19)

    key = build_s3_key(today)

    assert key == f"raw/coins_markets/dt={today}/coins_parquet_{today}.parquet"