# CBAR Rates
Python library to work with AZN (Azerbaijani manat) official rates based on [CBAR](https://cbar.az/currency/rates?language=en) (The Central Bank of the Republic of Azerbaijan)

## Installation

```bash
$ pip install cbar-rates --upgrade
```
## Example

```python
from datetime import date
import cbar

rates_date = date.today()
currencies = ["USD"]

rates = cbar.get_rates(rates_date, currencies)

print(rates)

>>> {'date': '11.11.2024', 'currencies': {'USD': {'nominal': '1', 'value': 1.7}}}
```
All available currency codes can be found on the [CBAR website](https://www.cbar.az/currency/rates?language=en)
