# coding=utf-8

"""
Pyccuweather
The Python Accuweather API

(c) Chris von Csefalvay, 2015.

http://www.github.com/chrisvoncsefalvay/pyccuweather/
"""

from pyccuweather import errors

ENDPOINT = "http://{api_type:s}.accuweather.com/"
FROOTS = {"loc_geoposition": "locations/v{version:d}/cities/geoposition/search.json",
          "loc_ip_address": "locations/v{version:d}/cities/ipaddress.json",
          "loc_search": "locations/v{version:d}/search.json",
          "loc_search_country": "locations/v{version:d}/{country_code}/search.json",
          "loc_postcode": "locations/v{version:d}/postalcodes/{country_code:s}/search.json",
          "loc_lkey": "locations/v{version:d}/{location_key:d}.json",
          "currentconditions": "currentconditions/v{version:d}/{location_key}.json",
          "currentconditions_6": "currentconditions/v{version:d}/{location_key}/historical.json",
          "currentconditions_24": "currentconditions/v{version:d}/{location_key}/historical/24.json",
          "minutecast_latlon": "forecasts/v{version:d}/minute.json",
          "forecast_1h": "forecasts/v{version:d}/hourly/1hour/{location_key}.json",
          "forecast_12h": "forecasts/v{version:d}/hourly/12hour/{location_key}.json",
          "forecast_24h": "forecasts/v{version:d}/hourly/24hour/{location_key}.json",
          "forecast_72h": "forecasts/v{version:d}/hourly/72hour/{location_key}.json",
          "forecast_120h": "forecasts/v{version:d}/hourly/120hour/{location_key}.json",
          "forecast_240h": "forecasts/v{version:d}/hourly/240hour/{location_key}.json",
          "forecast_1d": "forecasts/v{version:d}/daily/1day/{location_key}.json",
          "forecast_5d": "forecasts/v{version:d}/daily/5day/{location_key}.json",
          "forecast_10d": "forecasts/v{version:d}/daily/10day/{location_key}.json",
          "forecast_15d": "forecasts/v{version:d}/daily/15day/{location_key}.json",
          "forecast_25d": "forecasts/v{version:d}/daily/25day/{location_key}.json",
          "forecast_45d": "forecasts/v{version:d}/daily/45day/{location_key}.json",
          "airquality_current": "airquality/v{version:d}/observations/{location_key}.json",
          "airquality_yesterday": "airquality/v{version:d}/observations/1day/{location_key}.json",
          "climo_actuals_date": "climo/v{version:d}/actuals/{date:s}/{location_key}.json",
          "climo_actuals_range": "climo/v{version:d}/actuals/{location_key}.json",
          "climo_records_date": "climo/v{version:d}/records/{date:s}/{location_key}.json",
          "climo_records_range": "climo/v{version:d}/records/{location_key}.json",
          "climo_normals_date": "climo/v{version:d}/normals/{date:s}/{location_key}.json",
          "climo_normals_range": "climo/v{version:d}/normals/{location_key}.json",
          "climo_month_summary": "climo/v{version:d}/summary/{year:d}/{month:d}/{location_key}.json",
          "alarms_1d": "alarms/v{version:d}/1day/{location_key}",
          "alarms_5d": "alarms/v{version:d}/5day/{location_key}",
          "alarms_10d": "alarms/v{version:d}/10day/{location_key}",
          "alarms_15d": "alarms/v{version:d}/15day/{location_key}",
          "alarms_25d": "alarms/v{version:d}/25day/{location_key}"
          }


def froot(arg, **kwargs):
    """
    Obtains endpoint corresponding to the primary argument and formats it with the keyword arguments provided.

    :param arg: endpoint name
    :param kwargs: endpoint formatting arguments
    :return: endpoint URL suffix
    """
    try:
        assert arg in FROOTS.keys()
    except AssertionError:
        raise errors.NotImplementedOrUnknownMethod(arg)

    try:
        assert "api_type" in kwargs.keys()
    except AssertionError:
        kwargs["api_type"] = "apidev"

    try:
        assert "version" in kwargs.keys()
    except AssertionError:
        kwargs["version"] = 1

    froot_string = ENDPOINT + FROOTS[arg]
    return froot_string.format(**kwargs)
