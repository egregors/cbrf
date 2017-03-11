# cbrf

_Wrapper for The Central Bank of the Russian Federation site API_

[![Build Status](https://travis-ci.org/Egregors/cbrf.svg?branch=master)](https://travis-ci.org/Egregors/cbrf)

[Site](http://www.cbr.ru/) and [API](http://www.cbr.ru/scripts/Root.asp?PrtId=SXML)
 of The Central Bank of the Russian Federation.
 
## Installation

Clone this repo and install from the source:
```
    git clone https://github.com/Egregors/cbrf.git
    cd cbrf
    pip install -e .
```

## How to use

### API

To get raw XML answers you should use `cbrf.api` methods:

```
>>> import cbrf

>>> cbrf.get_currencies_info()
<Element 'Valuta' at 0x10b91f688>

>>> cbrf.get_daily_rate()
<Element 'ValCurs' at 0x10b82b9a8>

>>> date_1 = datetime(2001, 3, 2)
>>> date_2 = datetime(2001, 3, 14)
>>> get_dynamic_rates(date_req1=date_1, date_req2=date_2, currency_id='R01235')
<Element 'ValCurs' at 0x1107017c8>
```

### Models

Also you can user base models for work with API (see examples in the tests).

### Tests

To run tests:

```
pytest cbrf/tests.py 
```
> You should install `pytest` first

## Contributing

Bug reports, bug fixes, and new features are always welcome. 
Please open issues, and submit pull requests for any new code.