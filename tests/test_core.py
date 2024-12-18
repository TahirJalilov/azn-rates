import pytest
import requests
import cbar

from datetime import date


def test_cbar_xml():
    test_date = "18.11.2024"
    r = requests.get(f"https://cbar.az/currencies/{test_date}.xml", timeout=10)

    assert r.status_code == 200
    assert r.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')


def test_get_rates():
    date_ = date(2024, 11, 18)
    rates = cbar.get_rates(date_=date_, currencies=["USD"])

    assert isinstance(rates, dict)
    assert rates["date"] == "18.11.2024"
    assert rates["currencies"] == {"USD": {"nominal": "1", "rate": 1.7}}


def test_get_rates_all_currencies():
    date_ = date(2024, 11, 18)
    rates = cbar.get_rates(date_=date_)

    assert isinstance(rates, dict)
    assert rates["date"] == "18.11.2024"
    assert "USD" in rates["currencies"]
    assert "EUR" in rates["currencies"]
    assert "GBP" in rates["currencies"]


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
            "previous_rate": 1.7814,
            "rate": 1.7815,
            "difference": 0.0001,
        }
    }


def test_get_rates_with_diff_value_error():
    with pytest.raises(ValueError, match="previous_date must be earlier than date_."):
        previous_date = date(2025, 1, 1)
        date_ = date(2024, 1, 1)
        cbar.get_rates_with_diff(previous_date, date_)


def test_convert_same_currency():
    with pytest.raises(
        ValueError, match="Source and target currencies must be different."
    ):
        cbar.convert(100, "USD", "USD")


def test_convert_from_azn():
    result = cbar.convert(100, "USD", "AZN", date(2024, 11, 18))
    assert isinstance(result, float)
    assert result == 170.0  # 1 USD = 1.7 AZN


def test_convert_to_azn():
    result = cbar.convert(100, "AZN", "USD", date(2024, 11, 18))
    assert isinstance(result, float)
    assert result == 58.8235  # 1 AZN = 1/1.7 USD


def test_convert_non_azn():
    result = cbar.convert(100, "USD", "EUR", date(2024, 11, 18))
    assert isinstance(result, float)
    assert result == 94.8714  # 1 EUR = 1.7919 AZN and 1 USD = 1.7 AZN


def test_convert_currency_not_available():
    with pytest.raises(ValueError, match="Currency XYZ is not available on .*"):
        cbar.convert(100, "XYZ", "USD", date(2024, 11, 18))


def test_convert_date_not_provided():
    result = cbar.convert(100, "USD", "EUR")
    assert isinstance(result, float)
