# -*- coding: utf-8 -*-

#           ___    ___   __ __
#    /  /  /__    /__ ) (__/__)
#   /__/  /___)  /        /
#       )

"""
cbrf.py
~~~~~~~
Wrapper for The Central Bank of the Russian Federation site API.

CBRF site: http://www.cbr.ru/eng/
Source: https://github.com/Egregors/cbr

:copyright: (c) 2017 by Vadim Iskuchekov (@egregors)
:license: MIT
"""

__title__ = 'cbrf'
__version__ = '0.4.2'

from .api import get_currencies_info, get_daily_rates, get_dynamic_rates
