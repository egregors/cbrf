# -*- coding: utf-8 -*-

CURRENCY_CODES = {
    # http://www.cbr.ru/scripts/XML_val.asp?d=0
    'USD': 'R01235',
    'EUR': 'R01239',
}

CBRF_API_URLS = {
    'info': 'http://www.cbr.ru/scripts/XML_valFull.asp',
    'daily_rus': 'http://www.cbr.ru/scripts/XML_daily.asp?',
    'daily_eng': 'http://www.cbr.ru/scripts/XML_daily_eng.asp?',
    'dynamic': 'http://www.cbr.ru/scripts/XML_dynamic.asp?',
}

CBRF_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
}
