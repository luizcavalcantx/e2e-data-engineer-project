import requests
import pytest
from datetime import date
from pydantic import ValidationError

from extract_coin_info import (
    fetch_coin_info,
    validate_and_transform,
    save_to_parquet,
    build_s3_key,
    coin_ids,
)


def test_fetch_coin_info_calls_api_for_each_coin(mocker, sample_coin_info_response):
    mock_response = mocker.Mock()
    mock_response.json.return_value = sample_coin_info_response
    mock_response.raise_for_status.return_value = None
    mock_get = mocker.patch("extract_coin_info.requests.get", return_value=mock_response)
    mocker.patch("extract_coin_info.time.sleep")  # skip the 6s rate-limit delay

    result = fetch_coin_info()

    assert mock_get.call_count == len(coin_ids)
    assert len(result) == len(coin_ids)


def test_fetch_coin_info_raises_on_http_error(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    mocker.patch("extract_coin_info.requests.get", return_value=mock_response)
    mocker.patch("extract_coin_info.time.sleep")

    with pytest.raises(requests.HTTPError):
        fetch_coin_info()


def test_fetch_coin_info_respects_rate_limit(mocker, sample_coin_info_response):
    mock_response = mocker.Mock()
    mock_response.json.return_value = sample_coin_info_response
    mock_response.raise_for_status.return_value = None
    mocker.patch("extract_coin_info.requests.get", return_value=mock_response)
    mock_sleep = mocker.patch("extract_coin_info.time.sleep")

    fetch_coin_info()

    assert mock_sleep.call_count == len(coin_ids)
    mock_sleep.assert_called_with(6)


def test_validate_and_transform_valid_data(sample_coin_info_response):
    df = validate_and_transform([sample_coin_info_response])

    assert len(df) == 1
    assert df.iloc[0]["id"] == "bitcoin"


def test_validate_and_transform_rejects_malformed_data():
    # missing required fields: symbol, name, links, image
    bad_data = [{"id": "bitcoin"}]

    with pytest.raises(ValidationError):
        validate_and_transform(bad_data)


def test_save_to_parquet_creates_file(tmp_path, monkeypatch, sample_coin_info_response):
    monkeypatch.chdir(tmp_path)
    df = validate_and_transform([sample_coin_info_response])
    today = date(2026, 8, 19)

    local_path = save_to_parquet(df, today)

    assert local_path == f"tmp/coins_info_{today}.parquet"
    assert (tmp_path / local_path).exists()


def test_build_s3_key_format():
    today = date(2026, 8, 19)

    key = build_s3_key(today)

    assert key == f"raw/coins_info/dt={today}/coins_info_{today}.parquet"