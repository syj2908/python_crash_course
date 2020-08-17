from city_functions import city_function
import unittest

class StingTestCase(unittest.TestCase):
    def test_city_country(self):
        city_country = city_function("santiago", "chile")
        self.assertEqual(city_country, "santiago,chile")
unittest.main()