""" src/employee_class.py """

from datetime import datetime
from src.logger_setup import setup_logger

# Inicjalizacja loggera
logger = setup_logger()

class Employee:
    def __init__(self, nazwisko: str, imie: str, jednostka: str, nazwa_szkolenia: str, data_szkolenia: datetime, wazne_do: datetime, stanowisko: str = '', email: str = ''):
        self.nazwisko = nazwisko
        self.imie = imie
        self.jednostka = jednostka
        self.nazwa_szkolenia = nazwa_szkolenia
        self.data_szkolenia = data_szkolenia
        self.wazne_do = wazne_do
        self.db_url = False  # Flaga, czy pracownik istnieje w bazie danych z URL
        self.stanowisko = stanowisko
        self.email = email

    def days_until_expiration(self, current_date=None):
        """
        Zwraca liczbę dni do wygaśnięcia szkolenia.
        Args:
            current_date (datetime): Opcjonalna data do porównania z terminem ważności. Jeśli brak, to używa bieżącej daty.
        Returns:
            int: Liczba dni do wygaśnięcia szkolenia.
        """
        if current_date is None:
            current_date = datetime.now()
        return (self.wazne_do - current_date).days

    def is_expired(self, current_date=None):
        """
        Zwraca True, jeśli szkolenie pracownika jest przeterminowane.
        Args:
            current_date (datetime): Opcjonalna data do porównania z terminem ważności. Jeśli brak, to używa bieżącej daty.
        Returns:
            bool: True, jeśli szkolenie jest przeterminowane.
        """
        return self.days_until_expiration(current_date) < 0

    def is_soon_expiring(self, days=30, current_date=None):
        """
        Zwraca True, jeśli szkolenie kończy się w ciągu podanej liczby dni (domyślnie 30).
        Args:
            days (int): Liczba dni, w ciągu których szkolenie się kończy.
            current_date (datetime): Opcjonalna data do porównania z terminem ważności. Jeśli brak, to używa bieżącej daty.
        Returns:
            bool: True, jeśli szkolenie kończy się w ciągu podanej liczby dni.
        """
        return 0 <= self.days_until_expiration(current_date) <= days

    def is_valid_training(self, days=30, current_date=None):
        """
        Zwraca True, jeśli szkolenie jest ważne dłużej niż podana liczba dni (domyślnie 30 dni).
        Args:
            days (int): Liczba dni, powyżej której szkolenie jest uznawane za ważne.
            current_date (datetime): Opcjonalna data do porównania z terminem ważności. Jeśli brak, to używa bieżącej daty.
        Returns:
            bool: True, jeśli szkolenie jest ważne dłużej niż podana liczba dni.
        """
        return self.days_until_expiration(current_date) > days

    @classmethod
    def check_employee_in_db(cls, employees_csv, employees_db):
        """
        Sprawdza, czy pracownik z CSV istnieje w bazie danych z URL.
        Ustawia db_url = True, jeśli pracownik został znaleziony.
        
        Args:
            employees_csv (list): Lista pracowników z CSV.
            employees_db (list): Lista pracowników z bazy danych (URL).
        
        Returns:
            list: Zaktualizowana lista pracowników z CSV.
        """
        db_employee_data = {(emp['nazwisko'].lower(), emp['imie'].lower()): emp for emp in employees_db}

        for employee in employees_csv:
            db_employee = db_employee_data.get((employee.nazwisko.lower(), employee.imie.lower()))

            if db_employee:
                employee.db_url = True  # Jeśli pracownik istnieje w bazie z URL, ustaw db_url na True
                employee.stanowisko = db_employee.get('stanowisko', '')
                employee.email = db_employee.get('email', '')
                logger.debug(f"Pracownik {employee.nazwisko}, {employee.imie} został znaleziony w bazie danych.")
            else:
                employee.db_url = False
                logger.warning(f"Pracownik {employee.nazwisko}, {employee.imie} nie został znaleziony w bazie danych.")

        return employees_csv

    @staticmethod
    def filter_by_position(employees, management_keywords=None, leadership_keywords=None):
        """
        Filtruje pracowników według stanowiska.
        
        Args:
            employees (list): Lista pracowników do przefiltrowania.
            management_keywords (list): Lista słów kluczowych dla kadry zarządzającej. Domyślnie ["dyrektor"].
            leadership_keywords (list): Lista słów kluczowych dla kadry kierowniczej. Domyślnie ["kierownik"].
        
        Returns:
            tuple: Trzy listy - kadra zarządzająca, kadra kierownicza, pozostali pracownicy.
        """
        if management_keywords is None:
            management_keywords = ["dyrektor"]
        if leadership_keywords is None:
            leadership_keywords = ["kierownik"]

        kadra_zarzadcza = [emp for emp in employees if any(keyword in emp.stanowisko.lower() for keyword in management_keywords)]
        kadra_kierownicza = [emp for emp in employees if any(keyword in emp.stanowisko.lower() for keyword in leadership_keywords)]
        pracownicy = [emp for emp in employees if emp not in kadra_zarzadcza and emp not in kadra_kierownicza]
        
        logger.info(f"Znaleziono {len(kadra_zarzadcza)} osób w kadrze zarządzającej, {len(kadra_kierownicza)} osób w kadrze kierowniczej, oraz {len(pracownicy)} pracowników.")
        
        return kadra_zarzadcza, kadra_kierownicza, pracownicy
