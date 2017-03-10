# -*- coding: utf-8 -*-
"""
cbrf.models
~~~~~~~~

This module implements the cbrf wrapper API.

:copyright: (c) 2012 by Kenneth Reitz.
:license: MIT
"""
from __future__ import unicode_literals, absolute_import

from decimal import Decimal
from xml.etree.ElementTree import Element


class Currency(object):
    """ Class to deserialize response like:

    http://www.cbr.ru/scripts/XML_valFull.asp

    <Item ID="R01500">
        <Name>Молдавский лей</Name>
        <EngName>Moldova Lei</EngName>
        <Nominal>10</Nominal>
        <ParentCode>R01500</ParentCode>
        <ISO_Num_Code>498</ISO_Num_Code>
        <ISO_Char_Code>MDL</ISO_Char_Code>
    </Item>

    """

    def __init__(self, elem: Element):
        if elem:
            self._parse_currency_xml(elem)

    def __str__(self):
        return f'[{self.id}]: {self.name}/{self.eng_name}'

    def _parse_currency_xml(self, elem: Element):
        self.id = elem.attrib['ID']
        self.name = elem.find('Name').text
        self.eng_name = elem.find('EngName').text
        self.denomination = int(elem.find('Nominal').text)
        self.iso_num_code = int(elem.find('ISO_Num_Code').text)
        self.iso_char_code = elem.find('ISO_Char_Code').text


class DailyCurrencyRate(object):
    """ Class to deserialize response like:

    http://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002

    <Valute ID="R01010">
        <NumCode>036</NumCode>
        <CharCode>AUD</CharCode>
        <Nominal>1</Nominal>
        <Name>Австралийский доллар</Name>
        <Value>16,0102</Value>
    </Valute>

    """

    def __init__(self, elem: Element):
        if elem:
            self._parse_daily_currency_rate_xml(elem)

    def __str__(self):
        return f'[{self.id}]: {self.value}₽ за {self.denomination} {self.name}'

    def _parse_daily_currency_rate_xml(self, elem: Element):
        self.id = elem.attrib['ID']
        self.num_code = elem.find('NumCode').text
        self.char_code = elem.find('CharCode').text
        self.denomination = int(elem.find('Nominal').text)
        self.name = elem.find('Name').text
        self.value = Decimal(elem.find('Value').text.replace(',', '.'))
