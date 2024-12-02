import pytest
import requests
import cbar

from datetime import date


def test_cbar_xml():
    r = requests.get("https://cbar.az/currencies/18.11.2024.xml", timeout=10)

    assert r.status_code == 200
    assert r.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')


def test_get_rates():
    date_ = date(2024, 11, 18)
    rates = cbar.get_rates(date_=date_, currencies=["USD"])

    assert isinstance(rates, dict)
    assert rates["date"] == "18.11.2024"
    assert rates["currencies"] == {"USD": {"nominal": "1", "value": 1.7}}


def test_get_rates_type_error():
    with pytest.raises(
        TypeError,
        match="Currencies must be a list of strings \(ISO 4217 currency codes\).",
    ):
        cbar.get_rates(currencies=1)


def test_get_rates_with_diff():
    previous_date = date(2024, 11, 25)
    date_ = date(2024, 11, 26)
    rates = cbar.get_rates_with_diff(
        previous_date=previous_date, date_=date_, currencies=["EUR"]
    )

    assert isinstance(rates, dict)
    assert rates["previous_date"] == "25.11.2024"
    assert rates["date"] == "26.11.2024"
    assert rates["currencies"] == {
        "EUR": {
            "nominal": "1",
            "previous_value": 1.7814,
            "value": 1.7815,
            "difference": 0.0001,
        }
    }


def test_get_rates_with_diff_value_error():
    with pytest.raises(
        ValueError, match="previous_date must be earlier than date_."
    ):
        previous_date = date(2025, 1, 1)
        date_ = date(2024, 1, 1)
        cbar.get_rates_with_diff(previous_date, date_)
