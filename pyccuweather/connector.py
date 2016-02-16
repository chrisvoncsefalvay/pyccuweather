# coding=utf-8

"""
Pyccuweather
The Python Accuweather API

connector.py
Basic connector object and methods

(c) Chris von Csefalvay, 2015.
"""

import requests
from pyccuweather import errors
from pyccuweather.froots import froot
from pyccuweather.objects import *
import os


class Connection(object):
    """
    Represents a connection to the Accuweather API.

    :param API_KEY: API key
    :param dev: whether the dev mode api (apidev.accuweather.com) or the production api (api.accuweather.com) is used
    :param retry: number of retries of failed operations - TODO: implement
    :raise errors.MalformattedAPIKeyError: if the API key is not a 32-character string, an error is thrown
    """

    def __init__(self, API_KEY: str=None, dev: bool=True, retry: int=3, timeout=None):

        # TODO: implement retries

        if API_KEY is None:
            try:
                self.API_KEY = os.environ["ACCUWEATHER_APIKEY"]
            except KeyError:
                raise errors.NoAPIKeyProvided()

        else:
            self.API_KEY = API_KEY

        try:
            assert isinstance(self.API_KEY, str)
            assert len(self.API_KEY) is 32
        except AssertionError:
            raise errors.MalformattedAPIKeyError()

        self.API_ROOT = "http://apidev.accuweather.com" if dev is True else "http://api.accuweather.com"
        self.API_VERSION = "v1"
        self.retries = retry
        self.timeout = timeout

    def __str__(self):
        return u"Accuweather connector to {0:s}".format(self.API_ROOT)

    def wipe_api_key(self):
        """
        Wipes API key from a Connection instance
        :return: void
        """
        self.API_KEY = None

    ########################################################
    # Location resolvers                                   #
    ########################################################

    def loc_geoposition(self, lat: float, lon: float):
        """
        Resolves location based on geoposition.

        :param lat: latitude
        :param lon: longitude
        :return: Location object
        """

        try:
            assert isinstance(lat, (int, float)) and isinstance(lon, (int, float))
        except:
            raise ValueError

        try:
            assert abs(lat) <= 90 and abs(lon) <= 180
        except:
            raise errors.RangeError(lat, lon)

        payload = {"q": u"{0:.4f},{1:.4f}".format(lat, lon),
                   "apikey": self.API_KEY}

        resp = requests.get(url=froot("loc_geoposition"),
                            params=payload).json()

        assert len(resp) > 0

        if isinstance(resp, list):
            return Location(resp[0])
        elif isinstance(resp, dict):
            return Location(resp)

    def loc_string(self, search_string: str, country_code: str=None):
        """
        Resolves a search string and an optional country code to a location.

        :param search_string: search string
        :param country_code: country code to which the search will be limited
        :return: a LocationSet of results
        """

        if country_code is not None:
            try:
                assert len(country_code) is 2
            except:
                raise errors.InvalidCountryCodeError(country_code)

            url = froot("loc_search_country", country_code=country_code)
            payload = {"q": search_string,
                       "apikey": self.API_KEY}

        else:
            url = froot("loc_search")
            payload = {"q": search_string,
                       "apikey": self.API_KEY}

        resp = requests.get(url=url,
                            params=payload, timeout=self.timeout).json()

        _result = list()
        if len(resp) > 0:
            for each in resp:
                loc = Location(lkey=each["Key"],
                               lat=each["GeoPosition"]["Latitude"],
                               lon=each["GeoPosition"]["Longitude"],
                               localized_name=each["LocalizedName"],
                               english_name=each["EnglishName"],
                               region=each["Region"],
                               country=each["Country"],
                               administrative_area=each["AdministrativeArea"],
                               timezone=each["TimeZone"]
                               )
                _result.append(loc)
        else:
            raise errors.NoResultsError(search_string)

        return (LocationSet(results=_result,
                            search_expression=search_string,
                            country=country_code))

    def loc_postcode(self, country_code: str, postcode: str):
        """
        Resolves location based on postcode. Only works in selected countries (US, Canada).

        :param country_code: Two-letter country code
        :param postcode: Postcode
        :return: Location object
        """

        try:
            assert len(country_code) is 2
        except:
            raise errors.InvalidCountryCodeError(country_code)

        url = froot("loc_postcode", country_code=country_code)
        payload = {"q": postcode,
                   "apikey": self.API_KEY}

        resp = requests.get(url=url,
                            params=payload, timeout=self.timeout).json()

        assert len(resp) > 0

        if isinstance(resp, list):
            return Location(resp[0])
        elif isinstance(resp, dict):
            return Location(resp)

    def loc_ip(self, ip_address:str):
        """
        Resolves location based on IP address.

        :param ip_address: IP address
        :return: Location object
        """

        url = froot("loc_ip_address")
        payload = {"q": ip_address,
                   "apikey": self.API_KEY}

        resp = requests.get(url=url,
                            params=payload, timeout=self.timeout).json()

        assert len(resp) > 0

        if isinstance(resp, list):
            return Location(resp[0])
        elif isinstance(resp, dict):
            return Location(resp)

    def loc_lkey(self, lkey:int):
        """
        Resolves location by Accuweather location key.

        :param lkey: Accuweather location key
        :return: Location object
        """

        assert isinstance(lkey, int)

        url = froot("loc_lkey", location_key=lkey)
        payload = {"apikey": self.API_KEY}

        resp = requests.get(url=url,
                            params=payload, timeout=self.timeout).json()

        assert len(resp) > 0

        if isinstance(resp, list):
            return Location(resp[0])
        elif isinstance(resp, dict):
            return Location(resp)

    ########################################################
    # Current conditions                                   #
    ########################################################

    def get_current_wx(self, lkey:int=None, location:Location=None, current:int=0, details:bool=True):
        """
        Get current weather conditions.

        :param lkey: Accuweather location key
        :param location: Location object
        :param current: horizon - current weather, 6 hours or 24 hours
        :param details: should details be provided?
        :return: raw observations or CurrentObs object
        """

        assert current in [0, 6, 24]
        assert lkey is not None or location is not None
        if current is 0:
            url = froot("currentconditions", location_key=lkey)
        else:
            url = froot("currentconditions_{current}".format(current=current), location_key=lkey)

        payload = {"apikey": self.API_KEY,
                   "details": "true" if details is True else "false"}

        resp = requests.get(url=url,
                            params=payload, timeout=self.timeout)

        return CurrentObs(resp.json())

    ########################################################
    # Forecasts                                            #
    ########################################################

    def get_forecast(self, forecast_type:str, lkey:int, details:bool=True, metric:bool=True):
        forecast_types = ["1h", "12h", "24h", "72h", "120h", "240h",
                          "1d", "5d", "10d", "15d", "25d", "45d"]
        assert forecast_type in forecast_types

        fkeyid = u"forecast_{0:s}".format(forecast_type)

        url = froot(fkeyid, location_key=lkey)
        payload = {"apikey": self.API_KEY,
                   "details": "true" if details == True else "false",
                   "metric": "true" if metric == True else "false"}

        resp = requests.get(url=url,
                            params=payload, timeout=self.timeout)

        if forecast_type[-1] is "h":
            return HourlyForecasts(resp.json())
        elif forecast_type[-1] is "d":
            return DailyForecasts(resp.json())

    ########################################################
    # Air quality                                          #
    ########################################################

    def get_airquality(self, lkey:int, current:bool=True):
        assert isinstance(lkey, int)

        if current:
            fkeyid = "airquality_current"
        else:
            fkeyid = "airquality_yesterday"

        url = froot(fkeyid, location_key=lkey)
        payload = {"apikey": self.API_KEY}

        return requests.get(url=url,
                            params=payload, timeout=self.timeout)

    ########################################################
    # Climo                                                #
    ########################################################

    def get_actuals(self, lkey:int, start_date:str, end_date:str=None):

        # TODO: Return object
        # (needs API access)

        if end_date:
            fkeyid = "climo_actuals_range"
            url = froot(fkeyid, location_key=lkey)
            payload = {"apikey": self.API_KEY,
                       "start": start_date,
                       "end": end_date}
        else:
            fkeyid = "climo_actuals_date"
            url = froot(fkeyid,
                        date=start_date,
                        location_key=lkey)
            payload = {"apikey": self.API_KEY}

        return requests.get(url=url,
                            params=payload, timeout=self.timeout)

    def get_records(self, lkey, start_date, end_date=None):

        # TODO: Return object
        # (needs API access)

        if end_date:
            fkeyid = "climo_records_range"
            url = froot(fkeyid, location_key=lkey)
            payload = {"apikey": self.API_KEY,
                       "start": start_date,
                       "end": end_date}
        else:
            fkeyid = "climo_records_date"
            url = froot(fkeyid,
                        date=start_date,
                        location_key=lkey)
            payload = {"apikey": self.API_KEY}

        return requests.get(url=url,
                            params=payload, timeout=self.timeout)

    def get_normals(self, lkey, start_date, end_date=None):

        # TODO: Return object
        # (needs API access)

        if end_date:
            fkeyid = "climo_normals_range"
            url = froot(fkeyid, location_key=lkey)
            payload = {"apikey": self.API_KEY,
                       "start": start_date,
                       "end": end_date}
        else:
            fkeyid = "climo_normals_date"
            url = froot(fkeyid,
                        date=start_date,
                        location_key=lkey)
            payload = {"apikey": self.API_KEY}

        return requests.get(url=url,
                            params=payload, timeout=self.timeout)

    ########################################################
    # Alerts                                               #
    ########################################################

    def get_alerts(self, lkey, forecast_range):

        # TODO: Return object
        # (needs API access)

        assert isinstance(forecast_range, int)
        fkeyid = u"alarms_{0:d}d".format(forecast_range)
        url = froot(fkeyid, location_key=lkey)
        payload = {"apikey": self.API_KEY}

        return requests.get(url=url,
                            params=payload, timeout=self.timeout)