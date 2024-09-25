""" tests/test_HTMLReportGenerator.py """

import unittest
from unittest import mock
from datetime import datetime
from src.html_generator import HTMLReportGenerator
from src.employee import Employee  # Zakładamy, że Employee istnieje w src.employee

class TestHTMLReportGenerator(unittest.TestCase):

    @mock.patch('builtins.open', new_callable=mock.mock_open)  # Mockujemy otwieranie pliku
    @mock.patch('src.html_generator.os.path.join', return_value='output/test_report.html')  # Mockujemy os.path.join
    @mock.patch('src.html_generator.Template.render')  # Mockujemy renderowanie szablonu
    def test_generate_training_report(self, mock_render, mock_path_join, mock_open):
        """Test generowania raportu HTML o stanie szkoleń."""
        
        # Przykładowi pracownicy
        employees = [
            Employee(
                nazwisko="Wayne", imie="Bruce", jednostka="DC", nazwa_szkolenia="Security awareness",
                data_szkolenia=datetime(2023, 3, 12), wazne_do=datetime(2024, 3, 12)
            ),
            Employee(
                nazwisko="Stark", imie="Tony", jednostka="MR", nazwa_szkolenia="Security awareness",
                data_szkolenia=datetime(2024, 6, 15), wazne_do=datetime(2025, 6, 15)
            ),
            Employee(
                nazwisko="Rogers", imie="Steve", jednostka="DC", nazwa_szkolenia="Security awareness",
                data_szkolenia=datetime(2023, 7, 5), wazne_do=datetime(2025, 7, 5)
            )
        ]
        
        # Instancja klasy HTMLReportGenerator
        report_generator = HTMLReportGenerator()

        # Generowanie raportu
        report_generator.generate_training_report(employees)

        # Sprawdzenie, czy plik został zapisany poprawnie
        mock_open.assert_any_call('output/test_report.html', 'w', encoding='utf-8')

        # Sprawdzenie, czy metoda render została wywołana z odpowiednimi danymi
        mock_render.assert_called_once_with(
            valid_training=2,  # Wszyscy pracownicy mają ważne szkolenia
            soon_expiring=0,  # Żaden z pracowników nie ma szkolenia kończącego się w ciągu 30 dni
            expired=1,  # Żaden z pracowników nie ma przeterminowanego szkolenia
            employees=employees,
            current_date=datetime.now().strftime("%d.%m.%Y")
        )

    @mock.patch('builtins.open', new_callable=mock.mock_open)  # Mockujemy otwieranie pliku
    @mock.patch('src.html_generator.os.path.join', return_value='output/employee_list.html')  # Mockujemy os.path.join
    @mock.patch('src.html_generator.Template.render')  # Mockujemy renderowanie szablonu
    def test_generate_employee_list(self, mock_render, mock_path_join, mock_open):
        """Test generowania listy pracowników w formacie HTML."""

        # Przykładowi pracownicy
        employees = [
            Employee(
                nazwisko="Wayne", imie="Bruce", jednostka="DC", nazwa_szkolenia="Security awareness",
                data_szkolenia=datetime(2023, 3, 12), wazne_do=datetime(2024, 3, 12)
            ),
            Employee(
                nazwisko="Stark", imie="Tony", jednostka="MR", nazwa_szkolenia="Security awareness",
                data_szkolenia=datetime(2024, 6, 15), wazne_do=datetime(2025, 6, 15)
            )
        ]
        
        # Instancja klasy HTMLReportGenerator
        report_generator = HTMLReportGenerator()

        # Generowanie listy pracowników
        report_generator.generate_employee_list("Kadra kierownicza", employees)

        # Sprawdzenie, czy plik został zapisany poprawnie
        mock_open.assert_any_call('output/employee_list.html', 'w', encoding='utf-8')

        # Sprawdzenie, czy metoda render została wywołana z odpowiednimi danymi
        mock_render.assert_called_once_with(
            group_name="Kadra kierownicza",
            employees=employees
        )

if __name__ == '__main__':
    unittest.main()
