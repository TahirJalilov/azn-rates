import requests
import cbar

from datetime import date


def test_cbar_xml():
    response = requests.get("https://cbar.az/currencies/18.11.2024.xml", timeout=30)

    assert response.status_code == 200
    assert response.text.startswith('<?xml version="1.0" encoding="UTF-8"?>')


def test_get_rates():
    date_ = date(2024, 11, 18)
    rates = cbar.get_rates(date_, currencies=["USD"])

    assert isinstance(rates, dict)
    assert rates["date"] == "18.11.2024"
    assert rates["currencies"] == {"USD": {"nominal": "1", "value": 1.7}}
