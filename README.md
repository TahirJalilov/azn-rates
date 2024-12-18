# CBAR Rates

[![PyPI - Version](https://img.shields.io/pypi/v/cbar-rates)](https://pypi.org/project/cbar-rates)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cbar-rates)](https://pypi.org/project/cbar-rates)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/cbar-rates)](https://pypistats.org/packages/cbar-rates)
[![License](https://img.shields.io/pypi/l/cbar-rates)](LICENSE.md)

A Python library to work with Azerbaijani manat (AZN) official exchange rates based on [CBAR](https://cbar.az/currency/rates?language=en) (The Central Bank of the Republic of Azerbaijan).

## Features

- Retrieve official CBAR exchange rates for the Azerbaijani manat (AZN).
- Compare exchange rates between two dates and calculate differences.
- Filter results by specific currency codes (e.g., USD, EUR).

## Requirements

- Python 3.7 or higher
- `requests` library

## Installation

Install the library using pip:

```bash
pip install cbar-rates --upgrade
```

For isolated installations, use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install cbar-rates
```

## Examples

### Usage of `get_rates()`

```python
from datetime import date
import cbar

rates_date = date.today()
currencies = ["USD", "EUR"]

rates = cbar.get_rates(rates_date, currencies)

print(rates)
# Output:
{
    "date": "18.11.2024",
    "currencies": {
        "USD": {
            "nominal": "1",
            "rate": 1.7
        },
        "EUR": {
            "nominal": "1",
            "rate": 1.7919
        },
    }
}
```

### Usage of `get_rates_with_diff()`

```python
from datetime import date
import cbar

previous_date = date(2024, 11, 25)
date_ = date(2024, 11, 26)
currencies = ["USD", "EUR"]

rates = cbar.get_rates_with_diff(previous_date, date_, currencies)

print(rates)
# Output:
{
    "previous_date": "25.11.2024",
    "date": "26.11.2024",
    "currencies": {
        "USD": {
            "nominal": "1",
            "previous_rate": 1.7,
            "rate": 1.7,
            "difference": 0.0,
        },
        "EUR": {
            "nominal": "1",
            "previous_rate": 1.7814,
            "rate": 1.7815,
            "difference": 0.0001,
        },
    }
}
```

### Usage of `convert()`

```python
from datetime import date
import cbar

amount = 100
from_currency = "USD"
to_currency = "AZN"
conversion_date = date(2024, 11, 25)

converted_amount = cbar.convert(amount, from_currency, to_currency, conversion_date)

print(converted_amount)
# Output:
170.0  # 1 USD = 1.7 AZN
```

You can find all available currency codes on the [CBAR website](https://www.cbar.az/currency/rates?language=en)

## License

This project is licensed under the [MIT License](https://github.com/TahirJalilov/cbar-rates/blob/main/LICENSE.md).
