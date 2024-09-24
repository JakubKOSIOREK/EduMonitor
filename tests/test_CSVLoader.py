""" tests/test_CSVLoader.py """

import unittest
from unittest import mock
from src.csv_loader import CSVLoader
from src.employee import Employee

class TestCSVLoader(unittest.TestCase):

    @mock.patch('src.csv_loader.ConfigLoader')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="Wayne Enterprises;;;;;;Ukończone szkolenia;;;;;;\n"
                                                                        "Lp.;Nazwisko;Imię;Kod;Jednostka organizacyjna (Kod);;;Szkolenia;;;;;\n"
                                                                        "1;WAYNE;BRUCE;D001;DC;;;Security awareness;12.03.2023...12.03.2024;brak;ważne do 12.03.2024;;\n"
                                                                        "2;STARK;TONY;M045;MR;;;Security awareness;15.06.2024...15.06.2025;brak;ważne do 15.06.2025;;\n")
    def test_load_file_stream_success(self, mock_open, mock_config_loader):
        """Test poprawnego wczytywania pliku CSV"""
        loader = CSVLoader()
        result = list(loader.load_file_stream('dummy_path.csv'))

        # Sprawdzamy, czy dane zostały poprawnie wczytane (2 linie danych bez nagłówka)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][1], "WAYNE")  # Sprawdzamy dane z wiersza 1
        self.assertEqual(result[1][1], "STARK")  # Sprawdzamy dane z wiersza 2

    @mock.patch('src.csv_loader.ConfigLoader')
    @mock.patch('builtins.open', new_callable=mock.mock_open, read_data="Wayne Enterprises;;;;;;Ukończone szkolenia;;;;;;\n"
                                                                        "Lp.;Nazwisko;Imię;Kod;Jednostka organizacyjna (Kod);;;Szkolenia;;;;;\n"
                                                                        "1;WAYNE;;D001;DC;;;Security awareness;12.03.2023...12.03.2024;brak;ważne do 12.03.2024;;\n"
                                                                        "2;;TONY;M045;MR;;;Security awareness;15.06.2024...15.06.2025;brak;ważne do 15.06.2025;;\n")
    def test_load_file_stream_invalid_data(self, mock_open, mock_config_loader):
        """Test wczytywania pliku CSV z brakującymi danymi"""
        loader = CSVLoader()
        result = list(loader.load_file_stream('dummy_path.csv'))

        # Sprawdzamy, czy dane są poprawnie wczytane, ale mają brakujące pola
        self.assertEqual(len(result), 2)  # Oczekujemy 2 wierszy danych (bez nagłówka)
        self.assertEqual(result[0][2], "")  # Brak imienia dla pierwszego wiersza
        self.assertEqual(result[1][1], "")  # Brak nazwiska dla drugiego wiersza
