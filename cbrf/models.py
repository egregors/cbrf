import datetime
from decimal import Decimal
from xml.etree.ElementTree import Element

from cbrf import get_currencies_info, get_daily_rates, get_dynamic_rates
from cbrf.utils import str_to_date


class Currency:
    """Class to deserialize response like:

    https://www.cbr.ru/scripts/XML_valFull.asp

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
        if elem is not None and len(elem) > 0:
            self._parse_currency_xml(elem)

    def __str__(self) -> str:
        return f"[{self.id}]: {self.name}/{self.eng_name}"

    def _parse_currency_xml(self, elem: Element):
        self.id = elem.attrib["ID"]
        self.name = elem.findtext("Name")
        self.eng_name = elem.findtext("EngName")
        self.denomination = int(elem.findtext("Nominal"))
        _iso_num_code = elem.findtext("ISO_Num_Code")
        self.iso_num_code = (
            int(_iso_num_code)
            if _iso_num_code is not None and len(_iso_num_code) > 0
            else None
        )
        self.iso_char_code = elem.findtext("ISO_Char_Code")


class DailyCurrencyRecord:
    """Class to deserialize response like:

    https://www.cbr.ru/scripts/XML_daily.asp?date_req=02/03/2002

        <Valute ID="R01010">
            <NumCode>036</NumCode>
            <CharCode>AUD</CharCode>
            <Nominal>1</Nominal>
            <Name>Австралийский доллар</Name>
            <Value>16,0102</Value>
        </Valute>
    """

    def __init__(self, elem: Element):
        if elem is not None and len(elem) > 0:
            self._parse_daily_currency_record_xml(elem)

    def __str__(self) -> str:
        return f"[{self.id}]: {self.value}₽ за {self.denomination} {self.name}"

    def _parse_daily_currency_record_xml(self, elem: Element):
        self.id = elem.attrib["ID"]
        self.num_code = elem.findtext("NumCode")
        self.char_code = elem.findtext("CharCode")
        self.denomination = int(elem.findtext("Nominal"))
        self.name = elem.findtext("Name")
        self.value = Decimal(elem.findtext("Value").replace(",", "."))


class DynamicCurrencyRecord:
    """Class to deserialize response like:

    https://www.cbr.ru/scripts/XML_dynamic.asp?date_req1=02/03/2001&date_req2=14/03/2001&VAL_NM_RQ=R01235

        <Record Date="02.03.2001" Id="R01235">
            <Nominal>1</Nominal>
            <Value>28,6200</Value>
        </Record>
    """

    def __init__(self, elem: Element):
        if elem is not None and len(elem) > 0:
            self._parse_dynamic_currency_record(elem)

    def __str__(self):
        return f"[{self.id} | {self.date}]: {self.value}"

    def _parse_dynamic_currency_record(self, elem: Element):
        self.id = elem.attrib["Id"]
        self.date = str_to_date(elem.attrib["Date"])
        self.denomination = int(elem.findtext("Nominal"))
        self.value = Decimal(elem.findtext("Value").replace(",", "."))


class CurrenciesInfo:
    """Full set of currencies information from https://www.cbr.ru/scripts/XML_valFull.asp"""

    def __init__(self):
        self._raw_currencies = get_currencies_info()
        self.currencies = dict()
        for currency in self._raw_currencies:
            cur = Currency(currency)
            self.currencies[cur.id] = cur

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

    def __init__(self, date: datetime.datetime = None, lang: str = "rus"):
        self._raw_daily_rates = get_daily_rates(date_req=date, lang=lang)
        self.date = str_to_date(self._raw_daily_rates.attrib["Date"])

        self.rates = dict()

        for rate in self._raw_daily_rates:
            record = DailyCurrencyRecord(rate)
            self.rates[record.id] = record

    def __str__(self) -> str:
        return "[{}] rates for {}".format(
            len(self.rates), self.date.strftime("%d/%m/%Y")
        )

    def get_by_id(self, id_code: str) -> DailyCurrencyRecord or None:
        return self.rates.get(id_code)


class DynamicCurrenciesRates:
    """Full set of dynamic currency rates"""

    def __init__(
        self, date_1: datetime.datetime, date_2: datetime.datetime, id_code: str
    ):
        self._raw_dynamic_rates = get_dynamic_rates(
            date_req1=date_1, date_req2=date_2, currency_id=id_code
        )
        self.date_1 = str_to_date(self._raw_dynamic_rates.attrib["DateRange1"])
        self.date_2 = str_to_date(self._raw_dynamic_rates.attrib["DateRange2"])
        self.id = self._raw_dynamic_rates.attrib["ID"]

        self.rates = dict()

        for rate in self._raw_dynamic_rates:
            record = DynamicCurrencyRecord(rate)
            self.rates[record.date] = record

    def __str__(self):
        return "[{}] from {} to {}".format(
            len(self.rates),
            self.date_1.strftime("%d/%m/%Y"),
            self.date_2.strftime("%d/%m/%Y"),
        )

    def get_by_date(self, date: datetime.datetime) -> DynamicCurrencyRecord or None:
        return self.rates.get(date)
