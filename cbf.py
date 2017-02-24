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
from xml.etree import ElementTree

import requests

import const
from . import exceptions


# from . import exceptions


class ValCurs(object):
    """ Doc string """
    pass


def _format_data(date: datetime.datetime) -> str:
    """ Convert python datetime.datetime date to str for API request """
    return f'{date.strftime("%d/%m/%Y")}' if date else ''


def get_daily(date_req: datetime.datetime = None, lang: str = 'rus') -> str:
    """ Getting currency for current day.

    see example: http://www.cbr.ru/scripts/Root.asp?PrtId=SXML

    :param date_req:
    :type date_req: datetime.datetime
    :param lang: language of API response ('eng' || 'rus')
    :type lang: str

    :return:
    """
    if lang not in ['rus', 'eng']:
        raise ValueError('"lang" must be string. "rus" or "eng"')

    base_url = const.CBR_API_URLS['daily_rus'] if lang == 'rus' else const.CBR_API_URLS['daily_eng']
    url = base_url + _format_data(date_req)

    try:
        response = requests.get(url=url)
        response.encoding = 'windows-1251'

    except Exception as err:
        raise err

    tree = ElementTree.XML(response.text)

    return tree


if __name__ == '__main__':
    # TODO: CLI for all this stuff
    raise exceptions.NotImplementedException()
