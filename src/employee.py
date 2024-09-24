""" src/employee.py """

from datetime import datetime

class Employee:
    def __init__(self, nazwisko: str, imie: str, jednostka: str, nazwa_szkolenia: str, data_szkolenia: datetime, wazne_do: datetime, stanowisko: str = '', email: str = ''):
        self.nazwisko = nazwisko
        self.imie = imie
        self.jednostka = jednostka
        self.nazwa_szkolenia = nazwa_szkolenia
        self.data_szkolenia = data_szkolenia
        self.wazne_do = wazne_do
        self.stanowisko = stanowisko
        self.email = email
        self.db_url = False  # Flaga, czy pracownik istnieje w bazie danych z URL
        self.przeterminowany = False # Flaga, czy pracownik ma przeterminowane szkolenie

    def sprawdz_przeterminowanie(self, dzisiaj):
        if self.wazne_do < dzisiaj:
            self.przeterminowany = True

    def days_until_expiration(self, current_date=None):
        """
        Zwraca liczbę dni do wygaśnięcia szkolenia.
        Args:
            current_date (datetime): Opcjonalna data do porównania z terminem ważności. Jeśli brak, to używa bieżącej daty.
        Returns:
            int: Liczba dni do wygaśnięcia szkolenia.
        """
        current_date = current_date or datetime.now()
        return (self.wazne_do - current_date).days

    @property
    def is_expired(self):
        """
        Zwraca True, jeśli szkolenie pracownika jest przeterminowane.
        Returns:
            bool: True, jeśli szkolenie jest przeterminowane.
        """
        return self.days_until_expiration() < 0

    @property
    def is_soon_expiring(self):
        """
        Zwraca True, jeśli szkolenie kończy się w ciągu 30 dni.
        Returns:
            bool: True, jeśli szkolenie kończy się w ciągu 30 dni.
        """
        return 0 <= self.days_until_expiration() <= 30

    @property
    def is_valid_training(self):
        """
        Zwraca True, jeśli szkolenie jest ważne dłużej niż 30 dni.
        Returns:
            bool: True, jeśli szkolenie jest ważne dłużej niż 30 dni.
        """
        return self.days_until_expiration() > 30

    def __str__(self):
        """
        Reprezentacja tekstowa obiektu Employee.
        """
        return f"{self.nazwisko}, {self.imie} ({self.jednostka}) - Szkolenie: {self.nazwa_szkolenia} (Ważne do: {self.wazne_do.strftime('%d.%m.%Y')})"