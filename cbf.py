# -*- coding: utf-8 -*-
"""
    cbr.py
    ~~~~~~
    Wrapper for The Central Bank of the Russian Federation site API.

    CBRF site: http://www.cbr.ru/eng/
    Source: https://github.com/Egregors/cbr

    (c) @egregors 2017
"""
from __future__ import unicode_literals, absolute_import

import datetime
from xml.etree.ElementTree import Element, XML

import requests

import const


def date_format(date: datetime.datetime) -> str:
    """ Convert python datetime.datetime date to str for API request """
    return f'{date.strftime("%d/%m/%Y")}' if date else ''


def get_currencies_info():
    url = const.CBR_API_URLS['info']
    try:
        response = requests.get(url)
        response.encoding = 'windows-1251'

    except Exception as err:
        raise err

    return XML(response.text)


def get_daily_rate(date_req: datetime.datetime = None, lang: str = 'rus') -> Element:
    """ Getting currency for current day.

    see example: http://www.cbr.ru/scripts/Root.asp?PrtId=SXML

    :param date_req:
    :type date_req: datetime.datetime
    :param lang: language of API response ('eng' || 'rus')
    :type lang: str

    :return: XML tree
    """
    if lang not in ['rus', 'eng']:
        raise ValueError('"lang" must be string. "rus" or "eng"')

    base_url = const.CBR_API_URLS['daily_rus'] if lang == 'rus' else const.CBR_API_URLS['daily_eng']
    url = base_url + date_format(date_req)

    try:
        response = requests.get(url=url)
        response.encoding = 'windows-1251'

    except Exception as err:
        # TODO: Catch exceptions
        raise err

    return XML(response.text)


def get_dynamic_rates(date_req1: datetime.datetime,
                      date_req2: datetime.datetime,
                      val_nm_rq: str) -> Element:
    """

    :param date_req1: begin date
    :type date_req1: datetime.datetime
    :param date_req2: end date
    :type date_req2: datetime.datetime
    :param val_nm_rq: currency code (http://www.cbr.ru/scripts/XML_val.asp?d=0)
    :type val_nm_rq: str

    :return: XML tree
    """
    url = const.CBR_API_URLS['dynamic'] + \
          f'date_req1={date_format(date_req1)}&' \
          f'date_req2={date_format(date_req2)}&' \
          f'VAL_NM_RQ={val_nm_rq}'

    try:
        response = requests.get(url=url)
        response.encoding = 'windows-1251'

    except Exception as err:
        raise err

    return XML(response.text)


if __name__ == '__main__':
    # TODO: CLI for all this stuff
    pass
