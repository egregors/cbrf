# -*- coding: utf-8 -*-

"""
cbrf.utils
~~~~~~~~~~

:copyright: (c) 2017 by Vadim Iskuchekov (@egregors)
:license: MIT
"""
import datetime


def date_to_str(date: datetime.datetime) -> str:
    """ Convert python datetime.datetime date to str for API request

    :param date: date for format

    :return: date str in right format
    :rtype: str
    """
    return '{}'.format(date.strftime("%d/%m/%Y")) if date else ''


def str_to_date(date: str) -> datetime.datetime:
    """ Convert cbr.ru API date ste to python datetime

    :param date: date from API response

    :return: date like datetime
    :rtype: datetime
    """
    date = date.split('.')
    date.reverse()
    y, m, d = date
    return datetime.datetime(int(y), int(m), int(d))
