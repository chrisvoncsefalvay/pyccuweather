# coding=utf-8

"""
Pyccuweather
The Python Accuweather API

(c) Chris von Csefalvay, 2015.

http://www.github.com/chrisvoncsefalvay/pyccuweather/
"""


from collections import OrderedDict
from time import strptime
from uuid import uuid4


class Region(object):
    """
    An object representing an Accuweather Region.
    For a list of Accuweather regions: http://apidev.accuweather.com/developers/regions
    """
    def __init__(self, json=None, identifier=None, localized_name=None, english_name=None):

        assert json or (localized_name and english_name and identifier)

        if json:
            identifier = json["ID"]
            localized_name = json["LocalizedName"]
            english_name = json["EnglishName"]

        self.id = identifier
        self.localized_name = localized_name
        self.english_name = english_name

    def __str__(self):
        return u"<Region {0:s} ({1:s})>".format(self.english_name, self.id)


class AdministrativeArea(object):
    """
    Represents a primary administrative area.
    Countries are explained in the Accuweather documentation at http://apidev.accuweather.com/developers/administrativeareas
    """
    def __init__(self,
                 json=None,
                 identifier=None,
                 localized_name=None,
                 english_name=None,
                 level=None,
                 localized_type=None,
                 english_type=None):
        assert json or (identifier and localized_name and english_name and level and localized_type and english_type)

        if json:
            identifier = json["ID"]
            localized_name = json["LocalizedName"]
            english_name = json["EnglishName"]
            level = json["Level"]
            localized_type = json["LocalizedType"]
            english_type = json["EnglishType"]

        self.id = identifier
        self.localized_name = localized_name
        self.english_name = english_name
        self.level = level
        self.localized_type = localized_type
        self.english_type = english_type

    def __str__(self):
        return u"<{0:s} {1:s} ({2:s})>".format(self.english_type, self.english_name, self.id)


class Country(object):
    """
    Represents a Country.
    Countries are explained in the Accuweather documentation at http://apidev.accuweather.com/developers/countries
    """
    def __init__(self, json=None, identifier=None, localized_name=None, english_name=None):
        assert json or (localized_name and english_name and identifier)

        if json:
            identifier = json["ID"]
            localized_name = json["LocalizedName"]
            english_name = json["EnglishName"]

        self.id = identifier
        self.localized_name = localized_name
        self.english_name = english_name

    def __str__(self):
        return u"<Country: {0:s} ({1:s})>".format(self.english_name, self.id)


class TimeZone(object):
    """
    Represents a timezone.
    Timezones are explained in the Accuweather documentation at http://apidev.accuweather.com/developers/timeZones
    """
    def __init__(self,
                 json=None,
                 code=None,
                 name=None,
                 gmt_offset=None,
                 is_daylight_saving=None,
                 next_offset_change=None):
        assert json or (code and name and gmt_offset and is_daylight_saving and next_offset_change)

        if not json:
            assert isinstance(is_daylight_saving, bool)
            assert isinstance(gmt_offset, (float and int))
            assert isinstance(next_offset_change, str) and len(next_offset_change) == 20

        if json:
            code = json["Code"]
            name = json["Name"]
            gmt_offset = json["GmtOffset"]
            is_daylight_saving = True if json["IsDaylightSaving"] is 'true' else False
            next_offset_change = json["NextOffsetChange"]

        self.code = code
        self.name = name
        self.gmt_offset = gmt_offset
        self.is_daylight_saving = is_daylight_saving
        self.next_offset_change = strptime(next_offset_change, "%Y-%m-%dT%H:%M:%SZ")


class Location(object):
    """
    Represents a Location.
    Locations are explained in the Accuweather documentation at http://apidev.accuweather.com/developers/locations
    """
    def __init__(self,
                 json = None,
                 lkey = None,
                 lat: float=None,
                 lon: float=None,
                 localized_name: str=None,
                 english_name: str=None,
                 region: Region=None,
                 country: Country=None,
                 administrative_area: AdministrativeArea=None,
                 timezone: TimeZone=None):

        if json:
            lkey = json["Key"]
            lat = json["GeoPosition"]["Latitude"]
            lon = json["GeoPosition"]["Longitude"]
            localized_name = json["LocalizedName"]
            english_name = json["EnglishName"]
            region = json["Region"]
            country = json["Country"]
            administrative_area = json["AdministrativeArea"]
            timezone = json["TimeZone"]

        self.lkey = lkey
        self.lat = lat
        self.lon = lon
        self.localized_name = localized_name
        self.english_name = english_name
        self.region = Region(json=region)
        self.country = Country(json=country)
        self.administrative_area = AdministrativeArea(json=administrative_area)
        self.timezone = TimeZone(json=timezone)

    def __str__(self):
        return u"<Location key: {0} ({1})>".format(self.lkey, self.english_name)

    __repr__ = __str__


class LocationSet(object):
    """
    Represents a set of Locations returned usually as a search result.
    """
    def __init__(self, results: list, search_expression: str, country: str=None):
        self.results = results
        self.search_expression = search_expression
        self.country = country

    def __len__(self):
        return len(self.results)

    def __getitem__(self, item):
        return self.results[item]

    def __str__(self):
        return u"<Location result set for the query '{0:s}' ({1:d} results)>".format(self.search_expression,
                                                                                     len(self.results))

    __repr__ = __str__

    def append(self, location:Location):
        """
        Appends a location to the location result set.

        :param location: Location object
        :return: void
        """
        self.results.append(location)


class Temperature(object):
    """
    Represents a temperature value.
    """
    def __init__(self, value, units="C"):
        assert units in ["C", "F"]

        self.value = value
        self.units = units

    @property
    def F(self):
        """
        Represents the Temperature in Fahrenheit.

        :return: Temperature in degrees Fahrenheit.
        """
        if self.units == "F":
            return self.value
        else:
            return (self.value * 1.8) + 32

    @property
    def C(self):
        """
        Represents the Temperature in Celsius.

        :return: Temperature in degrees Celsius.
        """
        if self.units == "C":
            return self.value
        else:
            return (self.value - 32) * (5 / 9)

    def __str__(self):
        return u"<Temperature: {0:.1f} C / {1:.1f} F>".format(self.C, self.F)

    __repr__ = __str__


class Precipitation(object):
    """
    Represents a precipitation value.
    """
    def __init__(self, value, units="mm"):
        assert units in ["mm", "in"]

        self.value = value
        self.units = units

    @property
    def mm(self):
        """
        Represents precipitation in mm.

        :return: precipitation in mm
        """
        if self.units == "mm":
            return self.value
        else:
            return self.value * 25.4

    @property
    def inch(self):
        """
        Represents precipitation in inches.

        :return: precipitation in in
        """
        if self.units == "in":
            return self.value
        else:
            return self.value / 25.4

    def __str__(self):
        return u"<Precipitation: {0:.1f} mm / {1:.1f} in>".format(self.mm, self.inch)

    __repr__ = __str__


class Snow(object):
    def __init__(self, value, units="cm"):
        assert units in ["cm", "in"]

        self.value = value
        self.units = units

    @property
    def mm(self):
        if self.units == "cm":
            return 10 * self.value
        else:
            return self.value * 25.4

    def inch(self):
        if self.units == "in":
            return self.value
        else:
            return self.value / 2.54

    def __str__(self):
        return u"<Snow: {0:.1f} mm / {1:.1f} in>".format(self.mm, self.inch)

    __repr__ = __str__


class Wind(object):
    def __init__(self, json, hdg=None):

        self.speed = json["Speed"]["Value"]
        self.units = json["Speed"]["Unit"]
        if hdg is not None:
            self.hdg = hdg
        else:
            self.hdg = json["Direction"]["Degrees"]

    def kmh(self):
        if self.units == "km/h":
            return self.speed
        else:
            return self.speed * 1.60934

    def mph(self):
        if self.units == "mi/h":
            return self.speed
        else:
            return self.speed / 1.60934

    def __str__(self):
        return u"<Wind: {0} {1:.1f} kmh / {2:.1f} mph>".format(self.hdg, self.kmh, self.mph)

    __repr__ = __str__


class AirQualityFactor(object):
    def __init__(self, aqf_dict):
        self.name = aqf_dict["Name"]
        self.value = aqf_dict["Value"]
        self.category = aqf_dict["Category"]
        self.band = aqf_dict["CategoryValue"]


    def __str__(self):
        return u"<Air quality factor {0:s}: {1:.2f} ({2:s})>".format(self.name, self.value, self.band)

    __repr__ = __str__


class AirQuality(object):
    def __init__(self, aqf_dict):
        for each in aqf_dict:
            aqi = AirQualityFactor(each)
            exec("self.%s = aqi" % each["Name"].lower())


class Ceiling(object):
    def __init__(self, json):
        self.value = json["Value"]
        self.units = json["Unit"]

    @property
    def km(self):
        if self.units == "km":
            return self.value
        else:
            return self.value * 0.0003048

    @property
    def m(self):
        if self.units == "km":
            return self.value * 1000
        else:
            return self.value * 0.3048

    @property
    def ft(self):
        if self.units == "ft":
            return self.value
        else:
            return self.value * 3280.8399

    def __str__(self):
        return u"<Ceiling at {0:s}m (approximately FL {1:s})>".format(self.m, int(round(self.ft / 100, -1)))

    __repr__ = __str__

class Hemiurnal(object):
    def __init__(self, json):
        self.id = uuid4()
        # Verbals
        self.synopsis = json["LongPhrase"]
        self.phrase = json["ShortPhrase"]
        # Precipitation
        self.snow = Snow(value=json["Snow"]["Value"],
                         units=json["Snow"]["Unit"])
        self.wind = Wind(json["Wind"])
        self.rain = Precipitation(value=json["Rain"]["Value"],
                                  units=json["Rain"]["Unit"])
        self.ice = Precipitation(value=json["Ice"]["Value"],
                                 units=json["Ice"]["Unit"])
        self.total_liquid = Precipitation(value=json["Ice"]["Value"],
                                          units=json["Ice"]["Unit"])
        self.h_precipitation = json["HoursOfPrecipitation"]
        self.h_rain = json["HoursOfRain"]
        # Cloud cover
        self.cloud_cover = json["CloudCover"]
        # Probabilities
        self.p_rain = json["RainProbability"]
        self.p_snow = json["SnowProbability"]
        self.p_ice = json["IceProbability"]
        self.p_thunderstorm = json["ThunderstormProbability"]
        self.p_precipitation = json["PrecipitationProbability"]
        # Wind
        if "WindGust" in json.keys():
            self.wind_gust = Wind(json["WindGust"])
        else:
            self.wind_gust = None
        self.raw = json

    def __str__(self):
        return u"<Hemiurnal observation {0:s}>".format(self.id)

class DegreeDay(object):
    def __init__(self, aqf_dict):
        self.cooling = Temperature(value=aqf_dict["Cooling"]["Value"], units=aqf_dict["Cooling"]["Unit"])
        self.warming = Temperature(value=aqf_dict["Warming"]["Value"], units=aqf_dict["Warming"]["Unit"])


class DailyForecast(object):
    def __init__(self, json):
        # Dates
        self.epoch_date = json["EpochDate"]
        self.date = json["Date"]
        # Temperatures
        self.temp_min = Temperature(value=json["Temperature"]["Minimum"]["Value"],
                                    units=json["Temperature"]["Minimum"]["Unit"])
        self.temp_max = Temperature(value=json["Temperature"]["Maximum"]["Value"],
                                    units=json["Temperature"]["Maximum"]["Unit"])
        self.realfeel_temp_min = Temperature(value=json["RealFeelTemperature"]["Minimum"]["Value"],
                                             units=json["RealFeelTemperature"]["Minimum"]["Unit"])
        self.realfeel_temp_max = Temperature(value=json["RealFeelTemperature"]["Maximum"]["Value"],
                                             units=json["RealFeelTemperature"]["Maximum"]["Unit"])
        self.realfeel_shade_temp_min = Temperature(value=json["RealFeelTemperatureShade"]["Minimum"]["Value"],
                                                   units=json["RealFeelTemperatureShade"]["Minimum"]["Unit"])
        self.realfeel_shade_temp_max = Temperature(value=json["RealFeelTemperatureShade"]["Maximum"]["Value"],
                                                   units=json["RealFeelTemperatureShade"]["Maximum"]["Unit"])
        # Sunshine hours
        self.hours_of_sun = json["HoursOfSun"]
        # Hemiurnals
        self.day = Hemiurnal(json["Day"])
        self.night = Hemiurnal(json["Night"])
        self.raw = json

    def __str__(self):
        return u"<Daily forecast for {0:s}>".format(self.date)

    __repr__ = __str__

class HourlyForecast(object):
    def __init__(self, json):

        # Dates and times
        self.epoch_datetime = json["EpochDateTime"]
        self.datetime = json["DateTime"]
        # Temperatures
        self.temperature = Temperature(value=json["Temperature"]["Value"],
                                       units=json["Temperature"]["Unit"])
        self.realfeel_temperature = Temperature(value=json["Temperature"]["Value"],
                                                units=json["Temperature"]["Unit"])
        # Cloud cover and ceiling
        self.cloud_cover = json["CloudCover"]
        self.ceiling = Ceiling(json["Ceiling"])
        # Wind
        self.wind = Wind(json["Wind"])

        if "WindGust" in json.keys():
            if "Direction" in json["WindGust"].keys():
                self.wind_gust = Wind(json["WindGust"])
            else:
                self.wind_gust = Wind(json["WindGust"], hdg=self.wind.hdg)
        else:
            self.wind_gust = None
        # rH% and dew point
        self.rh = json["RelativeHumidity"]
        self.dewpoint = Temperature(value=json["DewPoint"]["Value"],
                                    units=json["DewPoint"]["Unit"])
        self.wet_bulb_temperature = Temperature(value=json["WetBulbTemperature"]["Value"],
                                                units=json["WetBulbTemperature"]["Unit"])
        # UV index
        self.uv_index = json["UVIndex"]
        self.uv_index_text = json["UVIndexText"]
        # Precipitation
        self.rain = Precipitation(value=json["Rain"]["Value"],
                                  units=json["Rain"]["Unit"])
        self.total_liquid = Precipitation(value=json["TotalLiquid"]["Value"],
                                          units=json["TotalLiquid"]["Unit"])
        self.ice = Precipitation(value=json["Ice"]["Value"],
                                 units=json["Ice"]["Unit"])
        self.snow = Snow(value=json["Snow"]["Value"],
                         units=json["Snow"]["Unit"])
        # Probabilities
        self.p_snow = json["SnowProbability"]
        self.p_ice = json["IceProbability"]
        self.p_rain = json["RainProbability"]
        self.p_precipitation = json["PrecipitationProbability"]
        # Accuweather
        self.link = json["Link"]
        self.mobile_link = json["MobileLink"]
        self.raw = json

    def __str__(self):
        return u"<Hourly forecast for {0:s}>".format(self.datetime)

    __repr__ = __str__



class DailyForecasts(object):
    def __init__(self, json):
        self.effective_date = json["Headline"]["EffectiveDate"]
        self.effective_epoch_date = json["Headline"]["EffectiveEpochDate"]
        self.end_date = json["Headline"]["EndDate"]
        self.end_epoch_date = json["Headline"]["EndEpochDate"]
        self.severity = json["Headline"]["Severity"]
        self.synopsis = json["Headline"]["Text"]
        self.link = json["Headline"]["Link"]
        self.mobile_link = json["Headline"]["MobileLink"]

        self.forecasts = OrderedDict()
        for each in json["DailyForecasts"]:
            k = each["Date"][0:10]
            v = DailyForecast(each)
            self.forecasts[k] = v
        self.raw = json

    def __str__(self):
        return "<Daily forecasts from %s to %s>" % (self.effective_date, self.end_date)

    __repr__ = __str__

class HourlyForecasts(object):
    def __init__(self, json):
        self.forecasts = OrderedDict()
        for each in json:
            k = each["DateTime"]
            v = HourlyForecast(each)
            self.forecasts[k] = v
        self.raw = json

    def __str__(self):
        return "<Hourly forecasts from %s>" % self.forecasts[0]

    __repr__ = __str__


class Observation(object):
    def __init__(self, json):
        # Date and time
        self.date_time = json["LocalObservationDateTime"]
        self.epoch_time = json["EpochTime"]
        self.synopsis = json["WeatherText"]
        self.temperature = Temperature(value=json["Temperature"]["Metric"]["Value"],
                                       units=json["Temperature"]["Metric"]["Unit"])
        self.link = json["Link"]
        self.mobile_link = json["MobileLink"]
        self.raw = json

    def __str__(self):
        return "<Synoptic observation at %s>" % self.date_time

    __repr__ = __str__



class CurrentObs(object):
    def __init__(self, json):
        self.observations = OrderedDict()
        for each in json:
            k = each["LocalObservationDateTime"]
            v = each
            self.observations[k] = v
        self.raw = json

    def __str__(self):
        return "<Current observations from %s>" % self.observations[0]
    __repr__ = __str__
