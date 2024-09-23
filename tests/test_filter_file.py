""" tests/test_filter_file.py """

import unittest
import logging
from src.logger_setup import setup_logger
from src.csv_loader import filter_file

# Ustawienie poziomu logowania na CRITICAL, aby wyłączyć logi poniżej tego poziomu
logger = setup_logger()
logger.setLevel(logging.CRITICAL)

class TestFilterFile(unittest.TestCase):

    def test_filter_file(self):
        raw_data = [
            ["Nagłówek", "Nagłówek2", "Nagłówek3"],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["", "", ""],
            ["1", "Kowalski", "Jan", "", "Dział II", "", "", "76mm Shooting", "24.12.2023...24.12.2024"],
        ]
        
        employees = filter_file(raw_data)
        
        self.assertEqual(len(employees), 1)
        self.assertEqual(employees[0].nazwisko, "Kowalski")
        self.assertEqual(employees[0].imie, "Jan")
        # Konwersja obiektu datetime na ciąg znaków w formacie 'dd.mm.rrrr'
        self.assertEqual(employees[0].data_szkolenia.strftime('%d.%m.%Y'), "24.12.2023")
        self.assertEqual(employees[0].wazne_do.strftime('%d.%m.%Y'), "24.12.2024")

if __name__ == '__main__':
    unittest.main()
