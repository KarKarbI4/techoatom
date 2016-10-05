import unittest

from main import Charge

class TestCharge(unittest.TestCase):

    def test_init(self):
        charge = Charge(9.0)
        self.assertIsInstance(charge, Charge)

    def test_values(self):
        charges = [9.0, 9.234543, -9.0, -9.34234, 9, -9]
        charges_answers = [9.0, 9.23, -9.0, -9.34, 9.0, -9.0]
        for i, charge_sum in enumerate(charges):
            charge = Charge(charge_sum)
            self.assertEqual(charge.value, charges_answers[i])

    def test_setter(self):
        charge = Charge(9.0)
        with self.assertRaises(AttributeError):
            charge.value = 4

if __name__ == '__main__':
    unittest.main()