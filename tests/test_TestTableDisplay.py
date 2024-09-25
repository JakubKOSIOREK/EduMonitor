""" tests/test_TestTableDisplay.py """

import unittest
from unittest import mock
from datetime import datetime
from src.table_display import TableDisplay
from src.employee import Employee  # Zakładamy, że Employee istnieje w src.employee

class TestTableDisplay(unittest.TestCase):

    @mock.patch('builtins.print')  # Mockujemy funkcję print
    @mock.patch('src.table_display.logger')  # Mockujemy logger
    def test_display_employees_table(self, mock_logger, mock_print):
        """Test wyświetlania tabeli pracowników."""

        # Przykładowi pracownicy
        employees = [
            Employee(
                nazwisko="Nowak", imie="Jan", jednostka="IT", nazwa_szkolenia="Python", 
                data_szkolenia=datetime(2023, 3, 12), wazne_do=datetime(2024, 3, 12)
            ),
            Employee(
                nazwisko="Kowalski", imie="Adam", jednostka="HR", nazwa_szkolenia="Leadership", 
                data_szkolenia=datetime(2022, 5, 15), wazne_do=datetime(2023, 5, 15)
            )
        ]

        # Instancja klasy TableDisplay
        table_display = TableDisplay()

        # Wyświetlamy tabelę
        table_display.display_employees_table(employees, "Kadra Kierownicza", "Test Table")

        # Sprawdzamy, czy dane zostały poprawnie wydrukowane
        mock_print.assert_called()  # Sprawdzenie, że print został wywołany
        mock_logger.info.assert_called_with("Wyświetlono 2 pracowników dla grupy 'Kadra Kierownicza - Test Table'")

    @mock.patch('builtins.print')  # Mockujemy funkcję print
    @mock.patch('src.table_display.logger')  # Mockujemy logger
    def test_display_employees_table_empty(self, mock_logger, mock_print):
        """Test wyświetlania tabeli pracowników dla pustej listy."""

        # Pusta lista pracowników
        employees = []

        # Instancja klasy TableDisplay
        table_display = TableDisplay()

        # Wyświetlamy tabelę
        table_display.display_employees_table(employees, "Kadra Kierownicza", "Test Table")

        # Sprawdzamy, czy logger odpowiednio zareagował na pustą listę
        mock_logger.info.assert_called_with("Brak pracowników w grupie Kadra Kierownicza - Test Table.")
        mock_print.assert_not_called()  # Sprawdzenie, że nic nie zostało wydrukowane

    @mock.patch('builtins.print')  # Mockujemy funkcję print
    @mock.patch('src.table_display.logger')  # Mockujemy logger
    def test_display_all_groups(self, mock_logger, mock_print):
        """Test wyświetlania tabeli dla wszystkich grup pracowników."""

        # Przykładowi pracownicy
        kadra_zarzadcza = [
            Employee(
                nazwisko="Wayne", imie="Bruce", jednostka="DC", nazwa_szkolenia="Security", 
                data_szkolenia=datetime(2023, 1, 1), wazne_do=datetime(2024, 1, 1)
            )
        ]
        kadra_kierownicza = [
            Employee(
                nazwisko="Stark", imie="Tony", jednostka="MR", nazwa_szkolenia="Leadership", 
                data_szkolenia=datetime(2022, 6, 15), wazne_do=datetime(2023, 6, 15)
            )
        ]
        pracownicy = [
            Employee(
                nazwisko="Rogers", imie="Steve", jednostka="HR", nazwa_szkolenia="Management", 
                data_szkolenia=datetime(2022, 7, 5), wazne_do=datetime(2023, 7, 5)
            )
        ]

        # Instancja klasy TableDisplay
        table_display = TableDisplay()

        # Wyświetlamy tabele dla wszystkich grup
        table_display.display_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy)

        # Sprawdzenie, czy print został wywołany
        mock_print.assert_called()  # Sprawdzenie, że tabele zostały wydrukowane

if __name__ == '__main__':
    unittest.main()
