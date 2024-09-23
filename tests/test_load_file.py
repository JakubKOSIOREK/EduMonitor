""" tests/test_load_file.py """

import unittest
import logging
import os
from src.logger_setup import setup_logger
from src.csv_loader import load_file

# Ustawienie poziomu logowania na CRITICAL, aby wyłączyć logi poniżej tego poziomu
logger = setup_logger()
logger.setLevel(logging.CRITICAL)

class TestLoadFile(unittest.TestCase):

    def setUp(self):
        # Tworzenie katalogu tmp, jeśli nie istnieje
        if not os.path.exists('tmp'):
            os.makedirs('tmp')

        # Tworzenie tymczasowego pliku CSV w katalogu tmp
        self.csv_path = 'tmp/sample_test.csv'
        with open(self.csv_path, 'w', encoding='cp1250') as file:
            file.write('Nagłówek1;Nagłówek2;Nagłówek3;Nagłówek4;Nagłówek5;Nagłówek6;Nagłówek7;Nagłówek8;Nagłówek9\n')
            file.write(';Kowalski;Jan;;Dział II;;;76mm Shooting;01.09.2024...01.09.2025\n')
            file.write(';Nowak;Tadeusz;;Dział X;;;Rope Splicing;15.08.2024...15.08.2025\n')

    def test_load_file(self):
        # Wczytanie danych z pliku CSV
        data = load_file(self.csv_path)
        
        # Testowanie, czy plik zawiera dane
        self.assertGreater(len(data), 0, "Plik CSV powinien zawierać dane")

    def tearDown(self):
        # Usunięcie tymczasowego pliku CSV po zakończeniu testu
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)

if __name__ == '__main__':
    unittest.main()
