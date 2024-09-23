""" tests/test_is_expired.py """

import unittest
from datetime import datetime
from src.employee_class import Employee

class TestIsExpired(unittest.TestCase):

    def test_is_expired(self):
        emp = Employee("Kowalski", "Jan", "Dział II", "76mm Shooting", datetime.now(), datetime(2023, 1, 1))
        self.assertTrue(emp.is_expired(), "Szkolenie powinno być przeterminowane")

if __name__ == '__main__':
    unittest.main()
