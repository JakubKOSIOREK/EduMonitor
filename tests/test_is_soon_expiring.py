""" tests/test_is_soon_expiring.py """

import unittest
from datetime import datetime, timedelta
from src.employee_class import Employee

class TestIsSoonExpiring(unittest.TestCase):

    def test_is_soon_expiring(self):
        emp = Employee("Kowalski", "Jan", "Dział II", "76mm Shooting", datetime.now(), datetime.now() + timedelta(days=15))
        self.assertTrue(emp.is_soon_expiring(), "Szkolenie powinno wygasać w ciągu 30 dni")

if __name__ == '__main__':
    unittest.main()
