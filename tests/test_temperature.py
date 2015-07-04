from unittest import TestCase
from pyccuweather.objects import Temperature
__author__ = 'CVoncsefalvay'


class TestTemperature(TestCase):


    def test_F(self):
        t_t = Temperature(value=220)
        t_u_f = Temperature(value=230, units="F")
        t_u_c = Temperature(value=-123, units="C")

        self.assertAlmostEqual(t_t.F, 428, delta=2)
        self.assertEqual(t_u_f.F, 230)
        self.assertAlmostEqual(t_u_c.F, -189.4, delta=2)

    def test_C(self):
        t_t = Temperature(value=220)
        t_u_f = Temperature(value=230, units="F")
        t_u_c = Temperature(value=-123, units="C")

        self.assertEqual(t_t.C, 220)
        self.assertAlmostEqual(t_u_f.C, 110, delta=2)
        self.assertEqual(t_u_c.C, -123)

