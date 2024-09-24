""" tests/test_EmployeeManager.py """
import unittest
from src.employee_management import EmployeeManager
from src.employee import Employee

class TestEmployeeManager(unittest.TestCase):

    def test_check_employee_in_db(self):
        """Test porównania danych z CSV i bazy danych."""
        
        # Dane z bazy danych
        db_employees = [
            {'nazwisko': 'Nowak', 'imie': 'Jan', 'stanowisko': 'Kierownik', 'email': 'jan.nowak@example.com'},
        ]
        
        # Dane z CSV
        csv_employee = Employee(
            nazwisko="Nowak", 
            imie="Jan", 
            jednostka="HR",  
            stanowisko="Pracownik",  
            nazwa_szkolenia="Security awareness", 
            data_szkolenia="12.03.2023", 
            wazne_do="12.03.2024"
        )
        
        # Tworzymy EmployeeManager z danymi CSV i bazy danych
        manager = EmployeeManager(employees_csv=[csv_employee], employees_db=db_employees)
        
        # Sprawdzamy pracowników w bazie
        manager.check_employee_in_db()

        # Sprawdzamy, czy flaga `db_url` została ustawiona na `True`
        self.assertEqual(csv_employee.db_url, True)

    def test_set_db_url_false(self):
        """Test ustawiania flagi db_url na False, gdy baza danych jest niedostępna."""
        
        # Symulacja braku danych w bazie
        db_employees = []
        
        csv_employee = Employee(
            nazwisko="Nowak", 
            imie="Jan", 
            jednostka="HR", 
            stanowisko="Kierownik", 
            nazwa_szkolenia="Security awareness", 
            data_szkolenia="12.03.2023", 
            wazne_do="12.03.2024"
        )
        
        manager = EmployeeManager(employees_csv=[csv_employee], employees_db=db_employees)
        manager.check_employee_in_db()

        # Sprawdzamy, czy flaga db_url została ustawiona na False
        self.assertFalse(csv_employee.db_url)

    def test_filter_by_position(self):
        """Test filtrowania pracowników według stanowiska."""
        
        # Tworzenie przykładowej listy pracowników
        employees = [
            Employee(
                nazwisko="Nowak", 
                imie="Jan", 
                jednostka="IT", 
                stanowisko="Kierownik", 
                nazwa_szkolenia="Security awareness", 
                data_szkolenia="12.03.2023", 
                wazne_do="12.03.2024"
            ),
            Employee(
                nazwisko="Kowalski", 
                imie="Adam", 
                jednostka="HR", 
                stanowisko="Pracownik", 
                nazwa_szkolenia="Safety training", 
                data_szkolenia="15.06.2024", 
                wazne_do="15.06.2025"
            ),
            Employee(
                nazwisko="Zieliński", 
                imie="Piotr", 
                jednostka="Finanse", 
                stanowisko="Kadra zarządzająca", 
                nazwa_szkolenia="Management", 
                data_szkolenia="10.02.2023", 
                wazne_do="10.02.2024"
            )
        ]
        
        manager = EmployeeManager(employees_csv=employees, employees_db=[])
        
        # Filtrujemy pracowników według stanowiska
        kadra_zarzadcza, kadra_kierownicza, pracownicy = manager.filter_by_position()
        
        # Sprawdzamy poprawność filtracji
        self.assertEqual(len(kadra_kierownicza), 1)
        self.assertEqual(kadra_kierownicza[0].nazwisko, "Nowak")

        self.assertEqual(len(kadra_zarzadcza), 1)
        self.assertEqual(kadra_zarzadcza[0].nazwisko, "Zieliński")

if __name__ == '__main__':
    unittest.main()
