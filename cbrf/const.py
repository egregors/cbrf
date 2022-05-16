import os

CURRENCY_CODES = {
    # https://www.cbr.ru/scripts/XML_val.asp?d=0
    "USD": "R01235",
    "EUR": "R01239",
}

CBRF_URL_SCHEME = os.getenv("CBRF_URL_SCHEME", "https")
CBRF_URL_HOST = os.getenv("CBRF_URL_HOST", "www.cbr.ru")

CBRF_URL = f"{CBRF_URL_SCHEME}://{CBRF_URL_HOST}"

CBRF_API_URLS = {
    "info": f"{CBRF_URL}/scripts/XML_valFull.asp",
    "daily_rus": f"{CBRF_URL}/scripts/XML_daily.asp?",
    "daily_eng": f"{CBRF_URL}/scripts/XML_daily_eng.asp?",
    "dynamic": f"{CBRF_URL}/scripts/XML_dynamic.asp?",
}

CBRF_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0"
}
