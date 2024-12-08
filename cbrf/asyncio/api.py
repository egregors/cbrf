import logging
from datetime import datetime
from xml.etree.ElementTree import XML, Element

import aiohttp

from .. import const, utils

logger = logging.getLogger(__name__)


async def get_currencies_info() -> Element:
    """Get META information about currencies

    url: https://www.cbr.ru/scripts/XML_val.asp

    :return:    `Element <Element 'Valuta'>` object
    :rtype:     ElementTree.Element
    """
    logger.debug("Performing get_currencies_info")
    logger.debug("Request to %s", const.CBRF_API_URLS["info"])
    async with aiohttp.ClientSession() as client:
        async with client.get(
            const.CBRF_API_URLS["info"], headers=const.CBRF_HEADERS, ssl=False
        ) as response:
            text = await response.text()
    logger.debug("Resp: %s", response.status)
    logger.debug("Body: %s", text)

    return XML(text)


async def get_daily_rates(date_req: datetime = None, lang: str = "rus") -> Element:
    """Getting currency for current day.

    see example: https://www.cbr.ru/scripts/Root.asp?PrtId=SXML

    :param date_req:
    :type date_req:     datetime
    :param lang:        language of API response ('eng' || 'rus')
    :type lang:         str

    :return:            `Element <Element 'ValCurs'>` object
    :rtype:             ElementTree.Element
    """
    logger.debug("Performing get_daily_rates")
    if lang not in ["rus", "eng"]:
        raise ValueError('"lang" must be string. "rus" or "eng"')

    base_url = (
        const.CBRF_API_URLS["daily_rus"]
        if lang == "rus"
        else const.CBRF_API_URLS["daily_eng"]
    )

    url = base_url + "date_req=" + utils.date_to_str(date_req) if date_req else base_url
    logger.debug("Request to %s | %s : %s", url, lang, date_req)
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=const.CBRF_HEADERS, ssl=False) as response:
            text = await response.text()
    logger.debug("Resp: %s", response.status)
    logger.debug("Body: %s", text)

    return XML(text)


async def get_dynamic_rates(
    date_req1: datetime, date_req2: datetime, currency_id: str
) -> Element:
    """Getting currency for time period.

    :param date_req1:       begin date
    :type date_req1:        datetime
    :param date_req2:       end date
    :type date_req2:        datetime
    :param currency_id:     currency code (https://www.cbr.ru/scripts/XML_val.asp?d=0)
    :type currency_id:      str

    :return:                `Element <Element 'ValCurs'>` object
    :rtype:                 ElementTree.Element
    """
    logger.debug("Performing get_dynamic_rates")
    url = const.CBRF_API_URLS[
        "dynamic"
    ] + "date_req1={}&date_req2={}&VAL_NM_RQ={}".format(
        utils.date_to_str(date_req1), utils.date_to_str(date_req2), currency_id
    )

    logger.debug(
        "Request to %s | %s between %s and %s", url, currency_id, date_req1, date_req2
    )
    async with aiohttp.ClientSession() as client:
        async with client.get(url, headers=const.CBRF_HEADERS, ssl=False) as response:
            text = await response.text()
    logger.debug("Resp: %s", response.status)
    logger.debug("Body: %s", text)

    return XML(text)
