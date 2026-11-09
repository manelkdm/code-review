import unittest
from example_app.calculator import divide, square_root


class CalculatorTests(unittest.TestCase):
    def test_nominal(self):
        self.assertEqual(divide(8, 2), 4)

    def test_zero(self):
        with self.assertRaisesRegex(ValueError, "division par zero"):
            divide(8, 0)

    def test_negative(self):
        self.assertEqual(divide(-8, 2), -4)

    def test_square_root(self):
        self.assertEqual(square_root(9), 3)

    def test_square_root_negative(self):
        with self.assertRaisesRegex(ValueError, "nombre négatif"):
            square_root(-1)
