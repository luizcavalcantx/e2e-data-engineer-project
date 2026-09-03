from datetime import date

import pytest
import requests
from pydantic import ValidationError

from extract_price_history import (
    build_s3_key,
    coin_ids,
    fetch_price_history,
    save_to_parquet,
    validate_and_transform,
)


def test_fetch_price_history_calls_api_for_each_coin(mocker, sample_price_history_response):
    mock_response = mocker.Mock()
    mock_response.json.return_value = sample_price_history_response
    mock_response.raise_for_status.return_value = None
    mock_get = mocker.patch("extract_price_history.requests.get", return_value=mock_response)
    mocker.patch("extract_price_history.time.sleep")  # skip the 6s rate-limit delay

    result = fetch_price_history()

    assert mock_get.call_count == len(coin_ids)
    assert [coin_id for coin_id, _ in result] == coin_ids


def test_fetch_price_history_raises_on_http_error(mocker):
    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = requests.HTTPError("500 Server Error")
    mocker.patch("extract_price_history.requests.get", return_value=mock_response)
    mocker.patch("extract_price_history.time.sleep")

    with pytest.raises(requests.HTTPError):
        fetch_price_history()


def test_fetch_price_history_respects_rate_limit(mocker, sample_price_history_response):
    mock_response = mocker.Mock()
    mock_response.json.return_value = sample_price_history_response
    mock_response.raise_for_status.return_value = None
    mocker.patch("extract_price_history.requests.get", return_value=mock_response)
    mock_sleep = mocker.patch("extract_price_history.time.sleep")

    fetch_price_history()

    assert mock_sleep.call_count == len(coin_ids)
    mock_sleep.assert_called_with(6)


def test_validate_and_transform_adds_coin_id_column(sample_price_history_response):
    df = validate_and_transform([("bitcoin", sample_price_history_response)])

    assert len(df) == 1
    assert df.iloc[0]["coin_id"] == "bitcoin"


def test_validate_and_transform_rejects_malformed_data():
    bad_data = [("bitcoin", {"prices": "not-a-list"})]  # wrong type

    with pytest.raises(ValidationError):
        validate_and_transform(bad_data)


def test_save_to_parquet_creates_file(tmp_path, monkeypatch, sample_price_history_response):
    monkeypatch.chdir(tmp_path)
    df = validate_and_transform([("bitcoin", sample_price_history_response)])
    today = date(2026, 8, 19)

    local_path = save_to_parquet(df, today)

    assert local_path == f"tmp/price_history_{today}.parquet"
    assert (tmp_path / local_path).exists()


def test_build_s3_key_format():
    today = date(2026, 8, 19)

    key = build_s3_key(today)

    assert key == f"raw/price_history/dt={today}/price_history_{today}.parquet"