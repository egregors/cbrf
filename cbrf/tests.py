# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from xml.etree.ElementTree import Element

from cbrf import (get_currencies_info, get_daily_rate, get_dynamic_rates)
from cbrf.models import Currency, DailyCurrencyRecord, DynamicCurrencyRecord, CurrenciesInfo


class CbrfAPITestCase(TestCase):
    def test_currencies_info(self):
        cur_inf = get_currencies_info()

        self.assertIsInstance(cur_inf, Element)
        self.assertEqual(len(cur_inf), 60)

    def test_get_daily_rate(self):
        date = datetime(2014, 10, 24)
        rates = get_daily_rate(date_req=date)

        aud = rates[0]

        self.assertEqual(aud.attrib['ID'], 'R01010')
        self.assertEqual(aud.find('Value').text, '36,4126')

    def test_get_dynamic_rates(self):
        date_1 = datetime(2001, 3, 2)
        date_2 = datetime(2001, 3, 14)

        rates = get_dynamic_rates(date_req1=date_1, date_req2=date_2, currency_id='R01235')

        self.assertEqual(len(rates), 8)
        self.assertEqual(rates[0].find('Nominal').text, '1')
        self.assertEqual(rates[0].find('Value').text, '28,6200')


class CbrfModelsTestCase(TestCase):
    def test_currency_model(self):
        c = Currency(get_currencies_info()[0])

        self.assertEqual(c.id, 'R01500')
        self.assertEqual(c.name, 'Молдавский лей')
        self.assertEqual(c.eng_name, 'Moldova Lei')
        self.assertEqual(c.denomination, 10)
        self.assertEqual(c.iso_num_code, 498)
        self.assertEqual(c.iso_char_code, 'MDL')

    def test_daily_currency_rate(self):
        d = DailyCurrencyRecord(get_daily_rate()[0])

        self.assertEqual(d.id, 'R01010')
        self.assertEqual(d.num_code, '036')
        self.assertEqual(d.char_code, 'AUD')
        self.assertEqual(d.denomination, 1)
        self.assertEqual(d.name, 'Австралийский доллар')

    def test_dynamic_currency_rate(self):
        date_1 = datetime(2001, 3, 2)
        date_2 = datetime(2001, 3, 14)
        d = DynamicCurrencyRecord(get_dynamic_rates(date_req1=date_1, date_req2=date_2, currency_id='R01235')[0])

        self.assertEqual(d.denomination, 1)
        self.assertEqual(d.value, Decimal('28.6200'))

    def test_correncies_info(self):
        c_info = CurrenciesInfo()
        self.assertEqual(len(c_info.currencies), 60)

        irish_pound_id = 'R01305'
        irish_pound = c_info.get_by_id(irish_pound_id)
        self.assertEqual(irish_pound.id, irish_pound_id)
        self.assertEqual(irish_pound.iso_num_code, 372)
