import unittest
from src.drawing.market_charts.price_humaniser import format_title_price, format_scale_price


class test_title_price_humaniser(unittest.TestCase):
    def test_uses_2dp_if_lessthan_100(self):
        self.assertEqual(format_title_price(1), "1.000")
        self.assertEqual(format_title_price(9.99), "9.990")
        self.assertEqual(format_title_price(11), "11.00")
        self.assertEqual(format_title_price(11.1), "11.10")
        self.assertEqual(format_title_price(99.99), "99.99")
        self.assertEqual(format_title_price(99.999), "100.00")

    def test_uses_0dp_if_greaterthan_100(self):
        self.assertEqual(format_title_price(100.1), "100")


class test_scale_price_humaiser(unittest.TestCase):
    def test_less_than_one(self):
        self.assertEqual(format_scale_price(0.9, 0), ".900")
        self.assertEqual(format_scale_price(0.99, 0), ".990")
        self.assertEqual(format_scale_price(1.11, 0), "1.11")
        self.assertEqual(format_scale_price(0.432, 0), ".432")
        self.assertEqual(format_scale_price(0.4324, 0), ".432")

    def test_decimal(self):
        self.assertEqual(format_scale_price(1, 0), "1.00")
        self.assertEqual(format_scale_price(9.99, 0), "9.99")
        self.assertEqual(format_scale_price(11, 0), "11")
        self.assertEqual(format_scale_price(11.1, 0), "11.1")
        self.assertEqual(format_scale_price(11.11, 0), "11.1")
        self.assertEqual(format_scale_price(100.11, 0), "100")

    def test_kilo(self):
        self.assertEqual(format_scale_price(1000, 0), "1K")
        self.assertEqual(format_scale_price(1100, 0), "1.1K")
        self.assertEqual(format_scale_price(11100, 0), "11.1K")

    def test_mega(self):
        self.assertEqual(format_scale_price(1000000, 0), "1M")
        self.assertEqual(format_scale_price(1100000, 0), "1.1M")
        self.assertEqual(format_scale_price(1110000, 0), "1.11M")
        self.assertEqual(format_scale_price(1111000, 0), "1.11M")

    def test_giga(self):
        self.assertEqual(format_scale_price(1000000000, 0), "1B")
        self.assertEqual(format_scale_price(1100000000, 0), "1.1B")
        self.assertEqual(format_scale_price(1110000000, 0), "1.11B")
        self.assertEqual(format_scale_price(1111000000, 0), "1.11B")
