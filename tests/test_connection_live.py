# coding=utf-8

from unittest import TestCase
from pyccuweather.connector import Connection
from pyccuweather.objects import *
from pyccuweather.errors import *
import yaml

class TestConnectionLive(TestCase):
    def setUp(self):
        APIKEY = yaml.load(open("config.yaml"))["apikey"]
        self.conn = Connection(API_KEY=APIKEY)

    def test_wipe_api_key(self):
        self.conn.wipe_api_key()
        assert self.conn.API_KEY is None

    def test_loc_geoposition(self):
        res = self.conn.loc_geoposition(lat=51.5, lon=-0.5)
        assert isinstance(res, Location)
        assert int(res.lkey) == 327019

        with self.assertRaises(ValueError):
            self.conn.loc_geoposition(lat=51.5, lon="potato")

    def test_out_of_range_lat(self):
        with self.assertRaises(RangeError):
            self.conn.loc_geoposition(lat=91.0, lon=-0.5)

        with self.assertRaises(RangeError):
            self.conn.loc_geoposition(lat=50.0, lon=183.1)

    def test_loc_string(self):
        with self.assertRaises(InvalidCountryCodeError):
            self.conn.loc_string(search_string="budapest", country_code="XXX")

        with self.assertRaises(NoResultsError):
            self.conn.loc_string(search_string="tqabBpmXsc")

        res = self.conn.loc_string(search_string="Ladoga", country_code="US")
        assert(isinstance(res, LocationSet))
        assert(len(res) == 5)
        assert(isinstance(res[1], Location))
        assert(res[1].lkey == '2152343')

    def test_loc_postcode(self):
        res = self.conn.loc_postcode(country_code="US", postcode=47954)
        assert isinstance(res, Location)
        assert res.lkey == '20721_PC'

        with self.assertRaises(InvalidCountryCodeError):
            self.conn.loc_postcode(country_code="USA", postcode=47954)

        with self.assertRaises(AssertionError):
            self.conn.loc_postcode(country_code="US", postcode="9999999")

    def test_loc_ip(self):
        res = self.conn.loc_ip("81.156.190.65")
        assert isinstance(res, Location)
        assert int(res.lkey) == 330732

    def test_loc_lkey(self):
        res = self.conn.loc_lkey(330732)
        assert isinstance(res, Location)
        self.assertAlmostEqual(res.lat, 50.91, delta=1)
        self.assertAlmostEqual(res.lon, -1.5, delta=1)

    def test_get_current_wx(self):
        res = self.conn.get_current_wx(330732)
        assert isinstance(res, CurrentObs)
        assert isinstance(res.observations, OrderedDict)

    def test_get_forecast(self):
        res = self.conn.get_forecast(forecast_type="12h", lkey=330732)
        assert isinstance(res, HourlyForecasts)
        assert isinstance(res.forecasts, OrderedDict)
        assert len(res.forecasts) == 12
