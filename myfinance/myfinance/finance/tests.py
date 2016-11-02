from datetime import date, timedelta
from decimal import Decimal

from django.test import TestCase

from finance.Charge import Charge

# Create your tests here.
class ChargeTestCase(TestCase):

    def test_init(self):
        charge = Charge(9.0, date.today())
        self.assertIsInstance(charge, Charge)

    def test_values(self):
        values = [9.0, 9.234543, -9.0, -9.34234, 9, -9]
        value_answers = [9.0, 9.23, -9.0, -9.34, 9.0, -9.0]
        for i, charge_sum in enumerate(values):
            charge = Charge(charge_sum, date.today())
            self.assertEqual(charge.value, round(Decimal(value_answers[i]), 2))

    def test_value_property(self):
        charge = Charge(9.0, date.today())
        with self.assertRaises(AttributeError):
            charge.value = 4
        with self.assertRaises(AttributeError):
            del charge.value

    def test_date_property(self):
        charge = Charge(9.0, date.today())
        with self.assertRaises(AttributeError):
            charge.date = date.today()
        with self.assertRaises(AttributeError):
            del charge.date

    def test_future_charge_off(self):
        with self.assertRaises(ValueError):
            charge = Charge(-100.00, date.today() + timedelta(days=5))
