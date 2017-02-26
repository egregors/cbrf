# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

CURRENCY_CODES = {
    # http://www.cbr.ru/scripts/XML_val.asp?d=0
    'USD': 'R01235',
    'EUR': 'R01239',
}

CBR_API_URLS = {
    'info': 'http://www.cbr.ru/scripts/XML_val.asp',
    'daily_rus': 'http://www.cbr.ru/scripts/XML_daily.asp?',
    'daily_eng': 'http://www.cbr.ru/scripts/XML_daily_eng.asp?',
    'dynamic': 'http://www.cbr.ru/scripts/XML_dynamic.asp?',
}
