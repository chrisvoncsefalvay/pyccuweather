# coding=utf-8

"""
Pyccuweather
The Python Accuweather API

(c) Chris von Csefalvay, 2015.

http://www.github.com/chrisvoncsefalvay/pyccuweather/
"""


class MalformattedAPIKeyError(BaseException):
    """
    Raised when the API key looks malformatted (wrong type or length). Does not actually check the API key for validity!"
    """
    def __str__(self):
        return "Malformatted API key: your API key must be a 32-character hexadecimal string."


class RangeError(BaseException):
    """
    Raised when the coordinates provided are out of range.
    """
    def __str__(self):
        return "Coordinates out of range."


class NoLocationError(BaseException):
    """
    Raised when the coordinates do not resolve to a particular location.
    """
    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __str__(self):
        return u"The coordinates {0:s} do not resolve to a correct location.".format(self.lat, self.lon)


class UnauthorisedError(BaseException):
    """
    Raised when the connection was not authorised.
    """
    def __str__(self):
        return "The server returned a HTTP1.1 403/Forbidden response."


class APIConnectionError(BaseException):
    """
    Raised when no connection to the Accuweather servers could be established.
    """
    def __str__(self):
        return u"Could not connect. You can check your connection by pinging Accuweather."


class APIError(BaseException):
    """
    Raised when the Accuweather servers returned a HTTP error code.
    """
    def __init__(self, status_code):
        self.status_code = status_code

    def __str__(self):
        return u"The Accuweather API returned an error: {0:s}".format(self.status_code)


class NotImplementedOrUnknownMethod(BaseException):
    """
    The method called has not been implemented yet or is an altogether non-existent method.
    """
    def __init__(self, API_method):
        self.API_method = API_method

    def __str__(self):
        return (u"The {0:s} method is not implemented in this client. "
                u"There's a chance this is because it does not exist.".format(self.API_method))


class InvalidCountryCodeError(BaseException):
    """
    Raised when a country code is provided that does not exist.
    Valid country codes are listed by Accuweather under http://apidev.accuweather.com/developers/countries
    """
    def __init__(self, country_code):
        self.country_code = country_code

    def __str__(self):
        return(u"The country code {0:s} could not be resolved.\n"
               u"For a list of valid two-letter country codes, please go to:\n"
               u"http://apidev.accuweather.com/developers/countries".format(self.country_code))


class MalformattedLocationKeyError(BaseException):
    """
    The location key is malformatted. This is raised when a primary (non-POI) location key is entered that does not fit
    the formal specifications.
    """

    def __str__(self):
        return(u"Malformatted location key: the location key must be an integer number and must be "
               u"entered as such.")

class NoResultsError(BaseException):
    """
    Yielded when a query has no results.
    """

    def __init__(self, query):
        self.query = query

    def __str__(self):
        return u"Your query for '{0:s}' yielded no results.".format(self.query)