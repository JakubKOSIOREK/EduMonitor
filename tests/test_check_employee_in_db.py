""" tests/test_check_employee_in_db.py """

import unittest
import logging
from src.logger_setup import setup_logger
from src.employee_class import Employee
from src.employee_class import Employee

# Ustawienie poziomu logowania na CRITICAL, aby wyłączyć logi poniżej tego poziomu
logger = setup_logger()
logger.setLevel(logging.CRITICAL)

class TestCheckEmployeeInDb(unittest.TestCase):

    def test_check_employee_in_db(self):
        employees_csv = [Employee("Kowalski", "Jan", "Dział II", "76mm Shooting", "2024-09-01", "2024-12-01")]
        employees_db = [{"nazwisko": "Kowalski", "imie": "Jan", "stanowisko": "Specjalista", "email": "jan.k@example.com"}]
        
        updated_employees = Employee.check_employee_in_db(employees_csv, employees_db)
        
        self.assertTrue(updated_employees[0].db_url)
        self.assertEqual(updated_employees[0].stanowisko, "Specjalista")
        self.assertEqual(updated_employees[0].email, "jan.k@example.com")

if __name__ == '__main__':
    unittest.main()
