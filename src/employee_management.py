""" src/employee_management.py """

from datetime import datetime
from src.utility.logging_decorator import log_exceptions
from src.utility.validation import validate_date_format, is_past_date
from src.logger_setup import setup_logger
logger = setup_logger()

class EmployeeManager:
    def __init__(self, employees_json, employees_db):
        self.employees_json = employees_json
        self.employees_db = employees_db

    @log_exceptions(logger)
    def check_employee_in_db(self):
        """
        Sprawdza pracowników z JSON w bazie danych z URL i aktualizuje ich dane. 
        """
        # Sprawdzamy, czy dane z bazy danych są dostępne
        if not self.employees_db:
            logger.warning("Brak danych z bazy danych. Ustawiam flagi db_url na False dla wszystkich pracowników z JSON.")
            # Ustawienie flagi db_url na False dla wszystkich pracowników z JSON
            for employee in self.employees_json:
                employee.db_url = False
            return self.employees_json

        db_employee_data = {(emp['nazwisko'].strip().lower(), emp['imie'].strip().lower()): emp for emp in self.employees_db}

        for employee in self.employees_json:
            nazwisko_json = employee.nazwisko.strip().lower()
            imie_json = employee.imie.strip().lower()

            db_employee = db_employee_data.get((nazwisko_json, imie_json))

            logger.debug(f"Sprawdzanie: {employee.nazwisko.strip().lower()}, {employee.imie.strip().lower()}")

            if db_employee:
                nazwisko_url = db_employee['nazwisko'].strip().lower()
                imie_url = db_employee['imie'].strip().lower()
                logger.debug(f"Dopasowanie URL: Nazwisko: {nazwisko_url}, Imię: {imie_url}")
                employee.db_url = True
                employee.stanowisko = db_employee.get('stanowisko', '')
                employee.email = db_employee.get('email', '')
            else:
                logger.debug(f"Brak dopasowania w URL: Nazwisko: {nazwisko_json}, Imię: {imie_json}")
                employee.db_url = False

        return self.employees_json

    def filter_by_position(self, management_keywords=None, leadership_keywords=None):
        """
        Filtruje pracowników według stanowiska (np. kadra zarządzająca, kierownicza, itp.).
        """
        if management_keywords is None:
            management_keywords = ["kadra zarządzająca", "zarząd", "CEO", "dyrektor"]

        if leadership_keywords is None:
            leadership_keywords = ["kadra kierownicza", "kierownik"]

        kadra_zarzadcza = [emp for emp in self.employees_json if any(keyword in emp.stanowisko.lower() for keyword in management_keywords)]
        kadra_kierownicza = [emp for emp in self.employees_json if any(keyword in emp.stanowisko.lower() for keyword in leadership_keywords)]
        pracownicy = [emp for emp in self.employees_json if emp not in kadra_zarzadcza and emp not in kadra_kierownicza]

        logger.info(f"Znaleziono {len(kadra_zarzadcza)} kadry zarządzającej, {len(kadra_kierownicza)} kierowniczej, oraz {len(pracownicy)} pracowników.")
        
        return kadra_zarzadcza, kadra_kierownicza, pracownicy
