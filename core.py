# -*- coding: utf-8 -*-
"""
    Core cbr.py models
"""
from __future__ import unicode_literals, absolute_import

import datetime
from xml.etree.ElementTree import Element, iselement, XML

import requests

import const


class DailyValCurs(object):
    """ Set of daily rates

    <ValCurs Date="02.03.2002" name="Foreign Currency Market">
        <Valute ID="R01010">
            <NumCode>036</NumCode>
            <CharCode>AUD</CharCode>
            <Nominal>1</Nominal>
            <Name>Австралийский доллар</Name>
            <Value>16,0102</Value>
        </Valute>
        <Valute ID="R01035">
            <NumCode>826</NumCode>
            <CharCode>GBP</CharCode>
            <Nominal>1</Nominal>
            <Name>Фунт стерлингов Соединенного королевства</Name>
            <Value>43,8254</Value>
        </Valute>
        ...
    </ValCurs>
    """

    class Valute(object):
        """ Class to deserialize response like:

        <Valute ID="R01010">
            <NumCode>036</NumCode>
            <CharCode>AUD</CharCode>
            <Nominal>1</Nominal>
            <Name>Австралийский доллар</Name>
            <Value>16,0102</Value>
        </Valute>

         """

        def __init__(self, raw_xml: Element):
            """ Parse and deserialize xml

            :param raw_xml: node element
            :type raw_xml: xml.etree.ElementTree.Element
            """
            self._parse_valute_xml_data(raw_xml=raw_xml)

        def __str__(self):
            return f'[{self.id}]: {self.nominal} {self.name} = {self.value} ₽'

        def _parse_valute_xml_data(self, raw_xml: Element):
            """ Parse Valute xml

            :param raw_xml: node element
            :type raw_xml: xml.etree.ElementTree.Element

            :return: void
            """
            if not iselement(raw_xml):
                raise ValueError('"raw_xml" must be xml.etree.ElementTree.Element instance')

            self.id = raw_xml.attrib['ID']

            # TODO: Should I make all of them decimal \ int?
            self.num_code = raw_xml.find('NumCode').text
            self.char_code = raw_xml.find('CharCode').text
            self.nominal = raw_xml.find('Nominal').text
            self.name = raw_xml.find('Name').text
            self.value = raw_xml.find("Value").text

    def __init__(self, date_req=None, lang='rus'):
        raw_xml = self._get_daily_curs(date_req=date_req, lang=lang)

        if not iselement(raw_xml):
            raise ValueError('"raw_xml" must be xml.etree.ElementTree.Element instance')

        self.date = raw_xml.attrib['Date']
        self.name = raw_xml.attrib['name']

        self.valutes = list()

        for valute in raw_xml:
            self.valutes.append(self.Valute(valute))

    def __str__(self):
        return f'{self.date}, {self.name}: {len(self.valutes)} valutes'

    def _get_all_rates(self):
        return ''.join(['{}\n'.format(valute) for valute in self.valutes])

    def _get_daily_curs(self, date_req: datetime.datetime = None, lang: str = 'rus') -> Element:
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
        url = base_url + self._format_data(date_req)

        try:
            response = requests.get(url=url)
            response.encoding = 'windows-1251'

        except Exception as err:
            raise err

        tree = XML(response.text)

        return tree

    @staticmethod
    def _format_data(date: datetime.datetime) -> str:
        """ Convert python datetime.datetime date to str for API request """
        return f'{date.strftime("%d/%m/%Y")}' if date else ''

    @property
    def all_rates(self):
        # all rates from self.valutes
        return self._get_all_rates()

    def get_val_by_id(self, valute_id: str) -> Valute:
        """
        :param valute_id: currency ID (http://www.cbr.ru/scripts/XML_val.asp?d=0)
        :return: Valute or None
        """
        vals = [val for val in self.valutes if val.id == valute_id]
        return vals[0] if len(vals) > 0 else None
