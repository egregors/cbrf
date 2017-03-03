# -*- coding: utf-8 -*-

"""
cbrf.utils
~~~~~~~~

This module implements the cbrf wrapper API.

:copyright: (c) 2012 by Kenneth Reitz.
:license: MIT
"""
import datetime


def date_format(date: datetime.datetime) -> str:
    """ Convert python datetime.datetime date to str for API request

    :param date: date for format

    :return: date str in right format
    :rtype: str
    """
    return f'{date.strftime("%d/%m/%Y")}' if date else ''
