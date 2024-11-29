"""Core components for cbar rates."""

import requests
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from typing import Dict, List, Optional, Union


def _get_cbar_data(
    date_: date,
) -> Dict[str, Union[str, Dict[str, Dict[str, Union[float, str]]]]]:
    """Get xml file with rates from CBAR parse it and return as dictionary.

    Args:
        date_ (date): Date of the rates.

    Returns:
        dict: Parsed data including the date and currency rates.

    Raises:
      HTTPError: If a request error occurs.
    """
    request_url = "https://cbar.az/currencies/{}.xml".format(date_.strftime("%d.%m.%Y"))
    response = requests.get(request_url, timeout=10)
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
) -> Dict[str, Union[str, Dict[str, Dict[str, Union[int, float]]]]]:
    """Get exchange rates for a given date and optionally filter by currency codes.

    Args:
        date_ (Optional[date]): Date of the rates. Defaults to today's date.
        currencies (Optional[List[str]]): List of ISO 4217 currency codes
                                          (https://www.cbar.az/currency/rates?language=en) to filter results.
                                          Defaults to all available currencies.

    Returns:
        Dict: Exchange rates structured as:
            {
                "date": "18.11.2024",
                "currencies": {
                    "USD": {
                        "nominal": "1",
                        "value": 1.7
                    },
                    "EUR": {
                        "nominal": "1",
                        "value": 1.85
                    },
                }
            }
    Raises:
        TypeError: If currencies is not a list of strings.
    """
    if date_ is None:
        date_ = date.today()

    result = _get_cbar_data(date_)

    if currencies is not None:
        if not isinstance(currencies, list) or not all(
            isinstance(s, str) for s in currencies
        ):
            raise TypeError(
                "Currencies must be a list of strings (ISO 4217 currency codes)."
            )

        currencies_set = {s.upper() for s in currencies}
        result["currencies"] = {
            currency: result["currencies"].get(currency)
            for currency in currencies_set
            if currency in result["currencies"]
        }

    return result


def get_rates_with_diff(
    previous_date: Optional[date] = None,
    next_date: Optional[date] = None,
    currencies: Optional[List[str]] = None,
) -> Dict[str, Union[str, Dict[str, Dict[str, Union[int, float]]]]]:
    """Get exchange rates with difference for given dates and optionally filter by currency codes.

    Args:
        previous_date (Optional[date]): Previous date of the rates. Defaults to next_date - 1 day.
        next_date (Optional[date]): Next date of the rates. Defaults to previous_date + 1 day.
                                            If both previous_date and next_date are None, today - 1 day and today.
        currencies (Optional[List[str]]): List of ISO 4217 currency codes
                                          (https://www.cbar.az/currency/rates?language=en) to filter results.
                                          Defaults to all available currencies.

    Returns:
        Dict: Exchange rates with differences structured as:
            {
                "previous_date": "25.11.2024",
                "next_date": "26.11.2024",
                "currencies": {
                    "USD": {
                        "nominal": "1",
                        "previous_value": 1.7,
                        "next_value": 1.7,
                        "difference": 0.0,
                    },
                    "EUR": {
                        "nominal": "1",
                        "previous_value": 1.7814,
                        "next_value": 1.7815,
                        "difference": 0.0001,
                    },
                }
            }
    Raises:
        TypeError: If currencies is not a list of strings.
        ValueError: If date inputs are inconsistent.
    """

    if previous_date is None and next_date is None:
        next_date = date.today()
        previous_date = next_date - timedelta(days=1)
    elif previous_date is not None and next_date is None:
        next_date = previous_date + timedelta(days=1)
    elif previous_date is None and next_date is not None:
        previous_date = next_date - timedelta(days=1)

    if previous_date >= next_date:
        raise ValueError("previous_date must be earlier than next_date.")

    previous_result = get_rates(previous_date, currencies)
    next_result = get_rates(next_date, currencies)

    result = {
        "previous_date": previous_result["date"],
        "next_date": next_result["date"],
        "currencies": {},
    }

    for currency, data in previous_result["currencies"].items():
        previous_value = data["value"]
        next_value = next_result["currencies"][currency]["value"]
        difference = next_value - previous_value

        result["currencies"][currency] = {
            "nominal": data["nominal"],
            "previous_value": previous_value,
            "next_value": next_value,
            "difference": round(difference, 4),
        }

    return result
