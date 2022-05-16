# cbrf

_Wrapper for The Central Bank of the Russian Federation site API_

[![Build Status](https://github.com/egregors/cbrf/actions/workflows/python-package.yml/badge.svg)](https://github.com/egregors/cbrf/actions)
[![PyPI version](https://badge.fury.io/py/cbrf.svg)](https://badge.fury.io/py/cbrf)

[Site](https://www.cbr.ru/) and [API](https://www.cbr.ru/scripts/Root.asp?PrtId=SXML)
of The Central Bank of the Russian Federation.

## Installation

Stable version:

```
    pip install cbrf
```

Dev version:

```
    git clone https://github.com/Egregors/cbrf.git
    cd cbrf
    pip install -e .
```

## Settings

For using with your own hostname set environment variables, for example

```
export CBRF_URL_SCHEME=https
export CBRF_URL_HOST=www.my-own-cbr.ru
```

## How to use

### API

To get raw XML answers you should use `cbrf.api` methods:

```
>>> import cbrf

>>> cbrf.get_currencies_info()
<Element 'Valuta' at 0x10b91f688>

>>> cbrf.get_daily_rates()
<Element 'ValCurs' at 0x10b82b9a8>

>>> date_1 = datetime(2001, 3, 2)
>>> date_2 = datetime(2001, 3, 14)
>>> get_dynamic_rates(date_req1=date_1, date_req2=date_2, currency_id='R01235')
<Element 'ValCurs' at 0x1107017c8>
```

### Models

You can use base models for work with API (see examples in the tests).

`CurrenciesInfo`

```
>>> from cbrf.models import CurrenciesInfo

>>> c_info = CurrenciesInfo()
>>> c_info.get_by_id("R01305").name
'Ирландский фунт'
>>> c_info.get_by_id("R01305").eng_name
'Irish Pound'
```

`DailyCurrenciesRates`

```
>>> from cbrf.models import DailyCurrenciesRates

>>> daily = DailyCurrenciesRates()
>>> daily.date
datetime.datetime(2017, 3, 11, 0, 0)
>>> daily.get_by_id('R01035').name
'Фунт стерлингов Соединенного королевства'
>>> daily.get_by_id('R01035').value
Decimal('72.0143')
```

`DynamicCurrenciesRates`

```
>>> from cbrf.models import DynamicCurrenciesRates

>>> date_1 = datetime(2001, 3, 2)
... date_2 = datetime(2001, 3, 14)
... id_code = 'R01235'
>>> dynamic_rates = DynamicCurrenciesRates(date_1, date_2, id_code)
>>> dynamic_rates.get_by_date(datetime(2001, 3, 8)).value
Decimal('28.6200')
```

Also, you can show `DEBUG` info, by setting logger level to DEBUG in your code:
```python
import logging

logging.basicConfig(level=logging.DEBUG)
```

### Linting & Tests

To run lint & tests:

```shell
make lint
make tests
```

> You should install `pytest` first

## Contributing

Bug reports, bug fixes, and new features are always welcome.
Please open issues, and submit pull requests for any new code.
