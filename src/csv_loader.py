""" src/csv_loader.py """

import csv
import re
from datetime import datetime
from src.employee import Employee
from src.config_loader import ConfigLoader
from src.utility.logging_decorator import log_exceptions
from src.logger_setup import setup_logger
logger = setup_logger()

import csv
import logging

class CSVLoader:
    """Klasa do wczytywania i filtrowania danych z pliku CSV."""

    def __init__(self, csv_path, expected_columns=13, encoding='cp1250'):
        self.csv_path = csv_path
        self.expected_columns = expected_columns  # Oczekiwana liczba kolumn
        self.encoding = encoding
        self.logger = logging.getLogger('EduMonitor')

    def load_and_filter_data(self):
        """
        Wczytuje dane z pliku CSV i filtruje je.
        Zwraca listę przefiltrowanych wierszy.
        """
        filtered_data = []
        try:
            with open(self.csv_path, mode='r', encoding=self.encoding) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=';')
                for row in csv_reader:
                    # Filtrowanie danych: sprawdzamy, czy wiersz jest poprawny
                    if self.is_valid_row(row):
                        filtered_data.append(row)
                    else:
                        self.logger.warning(f"Pominięto wiersz: {row}")
            return filtered_data
        except Exception as e:
            self.logger.error(f"Błąd podczas wczytywania pliku CSV: {e}")
            return []

    def is_valid_row(self, row):
        """
        Sprawdza, czy wiersz jest poprawny.
        Pomijamy wiersze, w których:
        - Pierwsza kolumna jest pusta LUB zawiera 'Lp.'.
        - Kolumny 2 (Nazwisko) i 3 (Imię) są puste ORAZ dwie ostatnie kolumny są puste.
        """
        # Sprawdzamy, czy liczba kolumn w wierszu jest zgodna z oczekiwaną
        if len(row) != self.expected_columns:
            self.logger.warning(f"Niepoprawna liczba kolumn: {len(row)} zamiast {self.expected_columns}. Wiersz: {row}")
            return False

        # Pomijamy wiersze, w których pierwsza kolumna jest pusta lub zawiera 'Lp.'
        if not row[0].strip() or row[0].strip().lower() == 'lp.':
            return False

        # Pomijamy wiersze, w których kolumny 2 i 3 są puste oraz dwie ostatnie kolumny są puste
        if (not row[1].strip() or not row[2].strip()) and (not row[-1].strip() and not row[-2].strip()):
            return False

        return True
