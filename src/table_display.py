""" src/table_display.py """

from prettytable import PrettyTable
from src.logger_setup import setup_logger

# Inicjalizacja loggera
logger = setup_logger()

def display_employees_table(employees, group_name, table_title):
    """
    Wyświetla tabelę pracowników w konsoli przy użyciu PrettyTable.
    
    Args:
        employees (list): Lista pracowników do wyświetlenia.
        group_name (str): Nazwa grupy zawodowej.
        table_title (str): Tytuł tabeli wyświetlany nad tabelą.
    """
    if not employees:
        return  # Jeśli lista pracowników jest pusta, nie wyświetlaj tabeli.

    print(f"\n{group_name} - {table_title}")  # Wyświetlanie tytułu tabeli

    table = PrettyTable()
    table.field_names = ["Nazwisko", "Imię", "Jednostka", "Nazwa szkolenia", "Data szkolenia", "Ważne do", "Z bazy URL", "Stanowisko", "Email"]
    
    for employee in employees:
        table.add_row([
            employee.nazwisko, 
            employee.imie, 
            employee.jednostka, 
            employee.nazwa_szkolenia, 
            employee.data_szkolenia.strftime("%d.%m.%Y"),   # Konwersja na string
            employee.wazne_do.strftime("%d.%m.%Y"),         # Konwersja na string
            employee.db_url,                                # True/False, czy pracownik istnieje w bazie URL
            employee.stanowisko,                            # Dodajemy stanowisko
            employee.email                                  # Dodajemy email
        ])
    
    print(table)
    logger.info(f"Dane pracowników z grupy '{group_name} - {table_title}' zostały wyświetlone.")


def display_group_tables(group, group_name):
    """
    Generuje i wyświetla tabele dla danej grupy zawodowej (aktualne szkolenie oraz wygaśnie w 30 dni/wygasło).
    
    Args:
        group (list): Lista pracowników do wyświetlenia.
        group_name (str): Nazwa grupy zawodowej.
    """
    valid_training = [emp for emp in group if emp.is_valid_training()]
    soon_expiring_or_expired = [emp for emp in group if emp.is_soon_expiring() or emp.is_expired()]

    if valid_training:
        display_employees_table(valid_training, group_name, "Aktualne szkolenie")

    if soon_expiring_or_expired:
        display_employees_table(soon_expiring_or_expired, group_name, "Szkolenie wygaśnie w ciągu 30 dni lub już wygasło")


def display_all_groups(kadra_zarzadcza, kadra_kierownicza, pracownicy):
    """
    Wyświetla tabele dla wszystkich grup zawodowych.
    
    Args:
        kadra_zarzadcza (list): Lista pracowników w kadrze zarządzającej.
        kadra_kierownicza (list): Lista pracowników w kadrze kierowniczej.
        pracownicy (list): Lista pozostałych pracowników.
    """
    if kadra_zarzadcza:
        display_group_tables(kadra_zarzadcza, "Kadra Zarządzająca")
    
    if kadra_kierownicza:
        display_group_tables(kadra_kierownicza, "Kadra Kierownicza")
    
    if pracownicy:
        display_group_tables(pracownicy, "Pracownicy")
