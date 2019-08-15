# -*- coding: utf-8 -*-
import os

CURRENCY_CODES = {
    # http://www.cbr.ru/scripts/XML_val.asp?d=0
    'USD': 'R01235',
    'EUR': 'R01239',
}

CBRF_URL_SCHEME = os.getenv('CBRF_URL_SCHEME', 'http')
CBRF_URL_HOST = os.getenv('CBRF_URL_HOST', 'www.cbr.ru')

CBRF_URL = '{}://{}'.format(CBRF_URL_SCHEME, CBRF_URL_HOST)

CBRF_API_URLS = {
    'info': '{}/scripts/XML_valFull.asp'.format(CBRF_URL),
    'daily_rus': '{}/scripts/XML_daily.asp?'.format(CBRF_URL),
    'daily_eng': '{}/scripts/XML_daily_eng.asp?'.format(CBRF_URL),
    'dynamic': '{}/scripts/XML_dynamic.asp?'.format(CBRF_URL),
}

CBRF_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
}
