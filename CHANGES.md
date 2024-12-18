cbar-rates
=====

v1.3.0 (2024-12-18)
-----
* Added `convert` function to convert an amount from one currency to another for a given date.
* Implemented error handling for unavailable source or target currencies.

v1.2.0 (2024-12-02)
-----
* Ensured that the order of currencies in the "currencies" dictionary matches the order specified in the input currencies list by using `OrderedDict`.

v1.1.0 (2024-12-01)
-----
* Added functionality to retrieve CBAR rates with the difference between values for two different dates.

v1.0.1 (2024-11-25)
-----
* Refactored type hints for better clarity and consistency.
* Added validation to raise TypeError if currencies is not a list of strings.

v1.0.0 (2024-11-24)
-----
* Initial release.
