""" src/table_display.py """

import locale
from prettytable import PrettyTable
from src.logger_setup import setup_logger

# Ustawiamy lokalizację na polską
locale.setlocale(locale.LC_COLLATE, 'pl_PL.UTF-8')

# Inicjalizacja loggera
logger = setup_logger()

def display_employees_table(employees, group_name, table_title):
    """
    Wyświetla tabelę pracowników w konsoli przy użyciu PrettyTable.
    """
    if not employees:
        return  # Jeśli lista pracowników jest pusta, nie wyświetlaj tabeli.

    # Sortowanie po nazwisku z użyciem locale.strxfrm(), aby obsłużyć polskie znaki
    employees = sorted(employees, key=lambda emp: locale.strxfrm(emp.nazwisko))

    print(f"\n{group_name} - {table_title} (Liczba pracowników: {len(employees)})")

    table = PrettyTable()
    table.field_names = ["Nazwisko", "Imię", "Dział", "Nazwa szkolenia", "Data szkolenia", "Ważne do"]

    table.align = "l"  # Domyślne wyrównanie dla wszystkich kolumn - do lewej
    table.align["Dział"] = "c"  # Specyficzne wyśrodkowanie dla kolumny 'Dział'
    table.border = True  # Dodanie obramowania
    table.padding_width = 1  # Zmniejszenie szerokości paddingu w komórkach

    for employee in employees:
        table.add_row([
            employee.nazwisko, 
            employee.imie, 
            employee.jednostka, 
            employee.nazwa_szkolenia, 
            employee.data_szkolenia.strftime("%d.%m.%Y"),   # Konwersja na string
            employee.wazne_do.strftime("%d.%m.%Y")          # Konwersja na string
        ])

    print(table)
    logger.info(f"Wyświetlono {len(employees)} pracowników dla grupy '{group_name} - {table_title}'")


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
