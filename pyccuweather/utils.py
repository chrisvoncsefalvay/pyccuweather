# coding=utf-8

"""
Pyccuweather
The Python Accuweather API

(c) Chris von Csefalvay, 2015.

http://www.github.com/chrisvoncsefalvay/pyccuweather/
"""

import json
from time import gmtime
from datetime import date


def wloads(content):
    """
    Decodes incoming JSON with UTF-8.

    :param content: JSON formatted content
    :return: JSON formatted content loaded as object and decoded with UTF-8.
    """
    return json.loads(content.decode('utf-8'))


def get_woy(epochdate):
    """
    Converts an epoch date into week of year.

    :param epochdate: Epoch date
    :return: week of year
    """
    _time = gmtime(epochdate)
    return date(_time.tm_year, _time.tm_mon, _time.tm_mday).isocalendar()[1]
