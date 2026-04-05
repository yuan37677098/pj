import unittest
from leap_year import is_leap_year


class TestIsLeapYear(unittest.TestCase):
    
    def test_divisible_by_400(self):
        self.assertTrue(is_leap_year(2000))
        self.assertTrue(is_leap_year(1600))
        self.assertTrue(is_leap_year(2400))
    
    def test_divisible_by_4_not_by_100(self):
        self.assertTrue(is_leap_year(2004))
        self.assertTrue(is_leap_year(2024))
        self.assertTrue(is_leap_year(2020))
        self.assertTrue(is_leap_year(1996))
    
    def test_divisible_by_100_not_by_400(self):
        self.assertFalse(is_leap_year(1900))
        self.assertFalse(is_leap_year(2100))
        self.assertFalse(is_leap_year(1800))
        self.assertFalse(is_leap_year(2200))
    
    def test_not_divisible_by_4(self):
        self.assertFalse(is_leap_year(2023))
        self.assertFalse(is_leap_year(2021))
        self.assertFalse(is_leap_year(1999))
        self.assertFalse(is_leap_year(2001))
    
    def test_edge_cases(self):
        self.assertTrue(is_leap_year(4))
        self.assertFalse(is_leap_year(1))
        self.assertFalse(is_leap_year(100))
        self.assertTrue(is_leap_year(400))


if __name__ == "__main__":
    unittest.main()
