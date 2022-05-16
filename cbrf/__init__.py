"""
cbrf.py
~~~~~~~
Wrapper for The Central Bank of the Russian Federation site API.

CBRF site:  https://www.cbr.ru/eng/
Source:     https://github.com/egregors/cbr

:copyright: (c) 2017 by Vadim Iskuchekov (@egregors)
:license: MIT
"""

__title__ = "cbrf"
__version__ = "0.5.0"

from .api import get_currencies_info, get_daily_rates, get_dynamic_rates

__all__ = [
    "get_currencies_info",
    "get_daily_rates",
    "get_dynamic_rates",
]
