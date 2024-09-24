""" src/employee_management.py """

from datetime import datetime
from src.utility.logging_decorator import log_exceptions
from src.utility.validation import validate_date_format, is_past_date
from src.logger_setup import setup_logger
logger = setup_logger()

class EmployeeManager:
    def __init__(self, employees_csv, employees_db):
        self.employees_csv = employees_csv
        self.employees_db = employees_db

    @log_exceptions(logger)
    def check_employee_in_db(self):
        """
        Sprawdza pracowników z CSV w bazie danych z URL i aktualizuje ich dane. Weryfikuje poprawność dat.
        """
        db_employee_data = {(emp['nazwisko'].lower(), emp['imie'].lower()): emp for emp in self.employees_db}
        for employee in self.employees_csv:
            # Sprawdzanie poprawności daty ważności szkolenia
            if not validate_date_format(employee.wazne_do.strftime("%d.%m.%Y")):
                logger.error(f"Błędny format daty dla pracownika: {employee.nazwisko}")
                continue

            if is_past_date(employee.wazne_do):
                employee.przeterminowany = True
                logger.warning(f"Szkolenie przeterminowane dla: {employee.nazwisko}")
                continue

            # Aktualizacja danych pracownika z bazy danych
            db_employee = db_employee_data.get((employee.nazwisko.lower(), employee.imie.lower()))
            if db_employee:
                employee.db_url = True
                employee.stanowisko = db_employee.get('stanowisko', '')
                employee.email = db_employee.get('email', '')
            else:
                employee.db_url = False

        return self.employees_csv

    def filter_by_position(self, management_keywords=None, leadership_keywords=None):
        """
        Filtruje pracowników według stanowiska.
        """
        if management_keywords is None:
            management_keywords = ["dyrektor"]
        if leadership_keywords is None:
            leadership_keywords = ["kierownik"]

        kadra_zarzadcza = [emp for emp in self.employees_csv if any(keyword in emp.stanowisko.lower() for keyword in management_keywords)]
        kadra_kierownicza = [emp for emp in self.employees_csv if any(keyword in emp.stanowisko.lower() for keyword in leadership_keywords)]
        pracownicy = [emp for emp in self.employees_csv if emp not in kadra_zarzadcza and emp not in kadra_kierownicza]

        logger.info(f"Znaleziono {len(kadra_zarzadcza)} kadry zarządzającej, {len(kadra_kierownicza)} kierowniczej, oraz {len(pracownicy)} pracowników.")
        
        return kadra_zarzadcza, kadra_kierownicza, pracownicy