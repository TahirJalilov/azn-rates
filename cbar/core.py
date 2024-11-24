"""Core components for cbar rates."""

import requests
import xml.etree.ElementTree as ET
from datetime import date
from typing import Dict, List, Optional

__all__ = ["get_rates"]


def _get_cbar_data(date_: date) -> Dict:
    """Get xml file with rates from CBAR parse it and return as dictionary.

    Args:
        date_: Date of the rates.

    Returns:
        Dict with all rates.

    Raises:
      HTTPError: If any error status occurred.
    """
    request_url = "https://cbar.az/currencies/{}.xml".format(date_.strftime("%d.%m.%Y"))
    response = requests.get(request_url, timeout=30)
    response.raise_for_status()
    tree = ET.fromstring(response.text)
    currencies = {}
    for currency in tree.iter("Valute"):
        currencies[currency.get("Code")] = {
            "nominal": currency.find("Nominal").text,
            "value": float(currency.find("Value").text),
        }

    cbar_data = {"date": tree.attrib.get("Date"), "currencies": currencies}

    return cbar_data


def get_rates(
    date_: Optional[date] = None, currencies: Optional[List[str]] = None
) -> Dict:
    """Get rates by date and return dictionary.

    Args:
        date_: Date of the rates. If not specified date.today() is used.
        currencies: A list of ISO 4217 currency codes (https://www.cbar.az/currency/rates?language=en).
                    If not specified returns all currencies.

    Returns:
        Dict with rates.
        example:
        {
            "date": "18.11.2024",
            "currencies": {
                "USD": {
                    "nominal": "1",
                    "value": 1.7
                },
            }
        }
    """
    if date_ is None:
        date_ = date.today()

    result = _get_cbar_data(date_)

    if currencies is not None:
        currencies_set = {s.upper() for s in currencies}
        result["currencies"] = {
            currency: result["currencies"][currency] for currency in currencies_set
        }

    return result
