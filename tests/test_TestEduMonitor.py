""" tests/test_EduMonitor.py """

import unittest
from unittest import mock
import os
import sys
import logging
from edumonitor import main
from src.logger_setup import reset_logger

class TestEduMonitor(unittest.TestCase):

    def setUp(self):
        # Resetowanie loggera przed każdym testem
        logger = logging.getLogger('EduMonitor')
        reset_logger(logger)

    @mock.patch('os.path.exists', return_value=True)  # Symulujemy, że plik istnieje
    @mock.patch('src.config_loader.ConfigLoader.get_database_url', return_value="http://example.com")  # Mockujemy URL z config
    @mock.patch('builtins.print')  # Mockujemy print, aby nie drukować nic na konsoli
    @mock.patch('src.csv_loader.CSVLoader.load_file_stream')  # Mockujemy ładowanie pliku CSV
    @mock.patch('src.csv_loader.CSVLoader.filter_file')  # Mockujemy filtrowanie pliku CSV
    @mock.patch('src.db_fetcher.fetch_employee_data_from_url')  # Mockujemy pobieranie danych z URL
    def test_flag_test_csv(self, mock_fetch_db, mock_filter_file, mock_load_file_stream, mock_print, mock_config, mock_exists):
        """Test działania flagi --test-csv"""

        # Symulacja argumentów wiersza poleceń z flagą --test-csv
        testargs = ["prog", "--test-csv"]
        with mock.patch.object(sys, 'argv', testargs):
            # Używamy assertLogs, aby przechwycić logi
            with self.assertLogs('EduMonitor', level='INFO') as log:
                main()

        # Sprawdzamy, czy logi zawierają oczekiwany komunikat
        expected_path = os.path.join('tests', 'test_files', 'dane_testowe.csv')
        self.assertIn(f"INFO:EduMonitor:Użycie testowego pliku CSV: {expected_path}", log.output)

    @mock.patch('os.path.exists', return_value=True)  # Symulujemy, że plik istnieje
    @mock.patch('src.config_loader.ConfigLoader.get_database_url', return_value="http://example.com")  # Mockujemy URL z config
    @mock.patch('builtins.print')  # Mockujemy print, aby nie drukować nic na konsoli
    def test_no_csv_or_test_csv(self, mock_print, mock_config, mock_exists):
        """Test braku flagi --csv i --test-csv"""
        
        # Symulacja argumentów wiersza poleceń bez flag --csv i --test-csv
        testargs = ["prog"]
        with mock.patch.object(sys, 'argv', testargs):
            # Używamy assertLogs, aby przechwycić logi
            with self.assertLogs('EduMonitor', level='ERROR') as log:
                main()

        # Sprawdzamy, czy logi zawierają oczekiwany komunikat
        self.assertIn("ERROR:EduMonitor:Błąd: Musisz podać ścieżkę do pliku CSV lub użyć flagi --test-csv.", log.output)

    @mock.patch('os.path.exists', return_value=True)  # Symulujemy, że plik istnieje
    @mock.patch('src.config_loader.ConfigLoader.get_database_url', return_value="http://example.com")  # Mockujemy URL z config
    @mock.patch('builtins.print')  # Mockujemy print, aby nie drukować nic na konsoli
    @mock.patch('src.csv_loader.CSVLoader.load_file_stream')  # Mockujemy ładowanie pliku CSV
    @mock.patch('src.csv_loader.CSVLoader.filter_file')  # Mockujemy filtrowanie pliku CSV
    @mock.patch('src.db_fetcher.fetch_employee_data_from_url')  # Mockujemy pobieranie danych z URL
    def test_flag_csv(self, mock_fetch_db, mock_filter_file, mock_load_file_stream, mock_print, mock_config, mock_exists):
        """Test działania flagi --csv"""
        
        # Symulacja argumentów wiersza poleceń z flagą --csv
        testargs = ["prog", "--csv", "sciezka/do/pliku.csv"]
        with mock.patch.object(sys, 'argv', testargs):
            # Używamy assertLogs, aby przechwycić logi
            with self.assertLogs('EduMonitor', level='INFO') as log:
                main()

        # Sprawdzamy, czy logi zawierają oczekiwany komunikat
        self.assertIn("INFO:EduMonitor:Program EduMonitor został uruchomiony.", log.output)

if __name__ == '__main__':
    unittest.main()
