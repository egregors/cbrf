from datetime import datetime

from ..utils import str_to_date
from ..models import Currency, DailyCurrencyRecord, DynamicCurrencyRecord
from .api import get_currencies_info, get_daily_rates, get_dynamic_rates


class CurrenciesInfo:
    """Full set of currencies information from https://www.cbr.ru/scripts/XML_valFull.asp"""

    def __init__(self):
        self.currencies = dict()

    async def create(self):
        raw_currencies = await get_currencies_info()
        for currency in raw_currencies:
            cur = Currency(currency)
            self.currencies[cur.id] = cur

        return self

    def __str__(self) -> str:
        return f"Currencies Info [{len(self.currencies)}]"

    def get_by_id(self, id_code: str) -> Currency or None:
        """Get currency by ID

        :param:     id_code: str, like "R01305"
        :return:    currency or None.
        """
        return self.currencies.get(id_code)


class DailyCurrenciesRates:
    """Full set of daily rates"""

    def __init__(self):
        self.date = None
        self.rates = dict()

    async def create(self, date: datetime = None, lang: str = "rus"):
        raw_daily_rates = await get_daily_rates(date_req=date, lang=lang)
        self.date = str_to_date(raw_daily_rates.attrib["Date"])

        self.rates = dict()

        for rate in raw_daily_rates:
            record = DailyCurrencyRecord(rate)
            self.rates[record.id] = record

        return self

    def __str__(self) -> str:
        return "[{}] rates for {}".format(
            len(self.rates), self.date.strftime("%d/%m/%Y")
        )

    def get_by_id(self, id_code: str) -> DailyCurrencyRecord or None:
        return self.rates.get(id_code)


class DynamicCurrenciesRates:
    """Full set of dynamic currency rates"""

    def __init__(self):
        self.date_1 = None
        self.date_2 = None
        self.id = None
        self.rates = dict()

    async def create(self, date_1: datetime, date_2: datetime, id_code: str):
        raw_dynamic_rates = await get_dynamic_rates(
            date_req1=date_1, date_req2=date_2, currency_id=id_code
        )
        self.date_1 = str_to_date(raw_dynamic_rates.attrib["DateRange1"])
        self.date_2 = str_to_date(raw_dynamic_rates.attrib["DateRange2"])
        self.id = raw_dynamic_rates.attrib["ID"]

        self.rates = dict()

        for rate in raw_dynamic_rates:
            record = DynamicCurrencyRecord(rate)
            self.rates[record.date] = record

        return self

    def __str__(self):
        return "[{}] from {} to {}".format(
            len(self.rates),
            self.date_1.strftime("%d/%m/%Y"),
            self.date_2.strftime("%d/%m/%Y"),
        )

    def get_by_date(self, date: datetime) -> DynamicCurrencyRecord or None:
        return self.rates.get(date)
