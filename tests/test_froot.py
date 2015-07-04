from unittest import TestCase
from pyccuweather.froots import froot
from pyccuweather import errors

__author__ = 'CVoncsefalvay'


class TestFroot(TestCase):

    def test_froot(self):
        with self.assertRaises(errors.NotImplementedOrUnknownMethod):
            froot("120dforecast")