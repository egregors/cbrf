# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from xml.etree.ElementTree import Element, iselement


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

    def __init__(self, raw_xml: Element):

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


class DynamicValCurs(object):
    """ Set of dynamics records

    <ValCurs ID="R01235" DateRange1="02.03.2001" DateRange2="14.03.2001" name="Foreign Currency Market Dynamic">
        <Record Date="02.03.2001" Id="R01235">
            <Nominal>1</Nominal>
            <Value>28,6200</Value>
        </Record>
        <Record Date="03.03.2001" Id="R01235">
            <Nominal>1</Nominal>
            <Value>28,6500</Value>
        </Record>
    </ValCurs>

    """

    class Record(object):
        """ Class to deserialize response like:

        <Record Date="02.03.2001" Id="R01235">
            <Nominal>1</Nominal>
            <Value>28,6200</Value>
        </Record>

        """

        def __init__(self, raw_xml: Element):
            """ Parse and deserialize xml

            :param raw_xml: node element
            :type raw_xml: xml.etree.ElementTree.Element
            """
            self._parse_record_xml_data(raw_xml)

        def __str__(self):
            return f'[{self.date}]: {self.value}'

        def _parse_record_xml_data(self, raw_xml: Element):
            """ Parse Valute xml

            :param raw_xml: node element
            :type raw_xml: xml.etree.ElementTree.Element

            :return: void
            """
            if not iselement(raw_xml):
                raise ValueError('"raw_xml" must be xml.etree.ElementTree.Element instance')

            self.id = raw_xml.attrib['Id']
            self.date = raw_xml.attrib['Date']

            self.nominal = raw_xml.find('Nominal').text
            self.value = raw_xml.find("Value").text

    def __init__(self, raw_xml: Element):

        if not iselement(raw_xml):
            raise ValueError('"raw_xml" must be xml.etree.ElementTree.Element instance')

        self.id = raw_xml.attrib['ID']
        self.date_range_1 = raw_xml.attrib['DateRange1']
        self.date_range_2 = raw_xml.attrib['DateRange2']
        self.name = raw_xml.attrib['name']

        self.records = list()
        for record in raw_xml:
            self.records.append(self.Record(record))

    def __str__(self):
        return f'[{self.date_range_1}:{self.date_range_2}] {self.name}: {len(self.records)}'

    def _get_all_records(self):
        return ''.join(['{}\n'.format(record) for record in self.records])

    @property
    def all_records(self):
        return self._get_all_records()
