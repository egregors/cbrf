# -*- coding: utf-8 -*-

from datetime import datetime
from decimal import Decimal
from unittest import TestCase
from xml.etree.ElementTree import Element

from cbrf import (get_currencies_info, get_daily_rates, get_dynamic_rates)
from cbrf.models import Currency, DailyCurrencyRecord, DynamicCurrencyRecord, CurrenciesInfo, DailyCurrenciesRates, \
    DynamicCurrenciesRates


class CbrfAPITestCase(TestCase):
    def test_currencies_info(self):
        cur_inf = get_currencies_info()

        self.assertIsInstance(cur_inf, Element)
        self.assertEqual(len(cur_inf), 61)

    def test_get_daily_rate(self):
        date = datetime(2014, 10, 24)
        rates = get_daily_rates(date_req=date)

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

        self.assertEqual(c.id, 'R01010')
        self.assertEqual(c.name, 'Австралийский доллар')
        self.assertEqual(c.eng_name, 'Australian Dollar')
        self.assertEqual(c.denomination, 1)
        self.assertEqual(c.iso_num_code, 36)
        self.assertEqual(c.iso_char_code, 'AUD')

    def test_daily_currency_rate(self):
        d = DailyCurrencyRecord(get_daily_rates()[0])

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
        self.assertEqual(len(c_info.currencies), 61)

        irish_pound_id = 'R01305'
        irish_pound = c_info.get_by_id(irish_pound_id)
        self.assertEqual(irish_pound.id, irish_pound_id)
        self.assertEqual(irish_pound.iso_num_code, 372)

        bad_id = 'lol'
        self.assertIsNone(c_info.get_by_id(bad_id))

    def test_daily_currencies_rates(self):
        date = datetime(2007, 1, 20)
        daily_rates = DailyCurrenciesRates(date)

        self.assertEqual(daily_rates.date, date)
        self.assertEqual(len(daily_rates.rates), 18)

        gbp_id = 'R01035'
        gbp = daily_rates.get_by_id(gbp_id)

        self.assertEqual(gbp.id, gbp_id)
        self.assertEqual(gbp.num_code, '826')

        bad_id = 'gg wp'
        self.assertIsNone(daily_rates.get_by_id(bad_id))

    def test_dynamic_currencies_rates(self):
        date_1 = datetime(2001, 3, 2)
        date_2 = datetime(2001, 3, 14)
        id_code = 'R01235'

        dynamic_rates = DynamicCurrenciesRates(date_1, date_2, id_code)

        self.assertEqual(len(dynamic_rates.rates), 8)
        self.assertEqual(dynamic_rates.get_by_date(datetime(2001, 3, 8)).value, Decimal('28.6200'))
        self.assertIsNone(dynamic_rates.get_by_date(datetime(3000, 1, 1)), None)
