""" src/csv_loader.py """

import csv
import re
from datetime import datetime
from src.employee import Employee
from src.config_loader import ConfigLoader
from src.utility.logging_decorator import log_exceptions
from src.logger_setup import setup_logger
logger = setup_logger()

class CSVLoader:
    """Loader do wczytywania i filtrowania plików CSV."""

    @log_exceptions(logger)
    def __init__(self, date_format=None):
        self.config_loader = ConfigLoader()
        self.date_format = date_format or self.config_loader.get_date_format()

    def load_file_stream(self, csv_file):
        logger.info(f"Rozpoczęto strumieniowe wczytywanie pliku CSV: {csv_file}")
        try:
            with open(csv_file, mode='r', encoding='cp1250') as file:
                for row in csv.reader(file, delimiter=';'):
                    if len(row) > 1 and row[0].isdigit():  # Sprawdzamy, czy wiersz zaczyna się od numeru wiersza
                        yield row
        except FileNotFoundError:
            logger.error(f"Plik {csv_file} nie został znaleziony.")  # Ten logger musi być wywoływany
        except Exception as e:
            logger.error(f"Błąd podczas otwierania pliku {csv_file}: {e}")

    def filter_file(self, raw_data):
        employees = []
        rejected_rows = 0

        # Wzorzec do sprawdzania poprawności daty (przykładowy regex do dat w formacie dd.mm.yyyy)
        date_pattern = re.compile(r"\d{2}\.\d{2}\.\d{4}")

        for i, row in enumerate(raw_data):
            if i < 7:  # Pomijanie nagłówków
                logger.debug(f"Pomijanie nagłówka: {row}")
                continue
            try:
                # Weryfikacja wiersza, czy spełnia minimalne wymagania
                if len(row) <= 7 or row[1] == '' or not date_pattern.match(row[8]):
                    logger.warning(f"Niepoprawny wiersz, zbyt mało kolumn, brak nazwiska lub błędny format daty: {row}")
                    continue

                # Odczytywanie i walidowanie dat
                nazwisko = row[1]
                imie = row[2]
                jednostka = row[4]
                nazwa_szkolenia = row[7]
                okres_szkolenia = row[8]

                # Walidacja i rozdzielenie zakresu dat
                daty = okres_szkolenia.split('...')
                if len(daty) != 2 or not date_pattern.match(daty[0].strip()) or not date_pattern.match(daty[1].strip()):
                    #logger.error(f"Błędny format okresu szkolenia dla {nazwisko}, {imie}: {okres_szkolenia}")
                    raise ValueError(f"Błędny format okresu szkolenia dla {nazwisko}, {imie}: {okres_szkolenia}")

                # Parsowanie dat
                data_szkolenia = datetime.strptime(daty[0].strip(), self.date_format)
                wazne_do = datetime.strptime(daty[1].strip(), self.date_format)

                employee = Employee(nazwisko, imie, jednostka, nazwa_szkolenia, data_szkolenia, wazne_do)
                employees.append(employee)

            except ValueError as e:
                logger.error(f"Błąd formatu daty dla {nazwisko}, {imie}: {e}")
                rejected_rows += 1

        logger.info(f"Zakończono filtrowanie danych. Wczytano {len(employees)} poprawnych pracowników, odrzucono {rejected_rows} wierszy.")
        return employees

    def _parse_training_dates(self, okres_szkolenia):
        """Wydobywa daty z okresu szkolenia i waliduje format."""
        daty = okres_szkolenia.split('...')
        if len(daty) != 2:
            raise ValueError(f"Błędny format okresu szkolenia: {okres_szkolenia}")

        data_szkolenia = datetime.strptime(daty[0].strip(), self.date_format)
        wazne_do = datetime.strptime(daty[1].strip(), self.date_format)
        return data_szkolenia, wazne_do