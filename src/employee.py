""" src/employee.py """

from datetime import datetime

class Employee:
    def __init__(self, nazwisko: str, imie: str, kod: str, jednostka_organizacyjna: str, nazwa_szkolenia: str, data_szkolenia: str, data_waznosci: str, db_url=False, stanowisko='', email=''):
        self.nazwisko = nazwisko
        self.imie = imie
        self.kod = kod
        self.jednostka_organizacyjna = jednostka_organizacyjna
        self.nazwa_szkolenia = nazwa_szkolenia
        self.data_szkolenia = datetime.strptime(data_szkolenia, "%d.%m.%Y") if data_szkolenia else None
        self.data_waznosci = datetime.strptime(data_waznosci, "%d.%m.%Y") if data_waznosci else None
        self.db_url = db_url
        self.stanowisko = stanowisko
        self.email = email
        self.przeterminowany = False

    def days_until_expiration(self, current_date=None):
        """
        Zwraca liczbę dni do wygaśnięcia szkolenia.
        Args:
            current_date (datetime): Opcjonalna data do porównania z terminem ważności. Jeśli brak, to używa bieżącej daty.
        Returns:
            int: Liczba dni do wygaśnięcia szkolenia.
        """
        if self.data_waznosci:
            current_date = current_date or datetime.now()
            return (self.data_waznosci - current_date).days
        return None

    @property
    def is_expired(self):
        """
        Zwraca True, jeśli szkolenie pracownika jest przeterminowane.
        Returns:
            bool: True, jeśli szkolenie jest przeterminowane.
        """
        days = self.days_until_expiration()
        return days is not None and days < 0

    @property
    def is_soon_expiring(self):
        """
        Zwraca True, jeśli szkolenie kończy się w ciągu 30 dni.
        Returns:
            bool: True, jeśli szkolenie kończy się w ciągu 30 dni.
        """
        days = self.days_until_expiration()
        return days is not None and 0 <= days <= 30
    
    @property
    def is_valid_training(self):
        """
        Zwraca True, jeśli szkolenie jest ważne dłużej niż 30 dni.
        Returns:
            bool: True, jeśli szkolenie jest ważne dłużej niż 30 dni.
        """
        days = self.days_until_expiration()
        return days is not None and days > 30

    def __str__(self):
        """
        Reprezentacja tekstowa obiektu Employee.
        """
        return f"{self.nazwisko}, {self.imie} ({self.jednostka_organizacyjna}) - Szkolenie: {self.nazwa_szkolenia} (Ważne do: {self.data_waznosci.strftime('%d.%m.%Y') if self.data_waznosci else 'N/A'})"
