""" src/table_display.py """

import locale
from prettytable import PrettyTable
from src.logger_setup import setup_logger
logger = setup_logger()

# Ustawiamy lokalizację na polską, aby poprawnie sortować nazwiska
locale.setlocale(locale.LC_COLLATE, 'pl_PL.UTF-8')

class TableDisplay:
    def __init__(self):
        pass

    def display_employees_table(self, employees, group_name, table_title):
        """
        Wyświetla tabelę pracowników w konsoli przy użyciu PrettyTable.
        """
        if not employees:
            logger.info(f"Brak pracowników w grupie {group_name} - {table_title}.")
            return

        # Sortowanie po nazwisku z użyciem locale.strxfrm() dla obsługi polskich znaków
        employees = sorted(employees, key=lambda emp: locale.strxfrm(emp.nazwisko))

        print(f"\n{group_name} - {table_title} (Liczba pracowników: {len(employees)})")

        table = PrettyTable()
        table.field_names = ["Nazwisko", "Imię", "Dział", "Nazwa szkolenia", "Data szkolenia", "Ważne do"]

        table.align = "l"  # Wyrównanie wszystkich kolumn do lewej
        table.align["Dział"] = "c"  # Wyśrodkowanie dla kolumny 'Dział'
        table.border = True  # Obramowanie tabeli
        table.padding_width = 1  # Zmniejszenie paddingu

        for employee in employees:
            table.add_row([
                employee.nazwisko,
                employee.imie,
                employee.jednostka_organizacyjna,
                employee.nazwa_szkolenia,
                employee.data_szkolenia.strftime("%d.%m.%Y"),
                employee.data_waznosci.strftime("%d.%m.%Y")
            ])

        print(table)
        logger.info(f"Wyświetlono {len(employees)} pracowników dla grupy '{group_name} - {table_title}'")

    def display_group_tables(self, group, group_name):
        """
        Generuje i wyświetla tabele dla danej grupy zawodowej (aktualne szkolenie oraz wygasające).
        """
        valid_training = [emp for emp in group if emp.is_valid_training]
        soon_expiring_or_expired = [emp for emp in group if emp.is_soon_expiring or emp.is_expired]

        if valid_training:
            self.display_employees_table(valid_training, group_name, "Aktualne szkolenie")

        if soon_expiring_or_expired:
            self.display_employees_table(soon_expiring_or_expired, group_name, "Szkolenie wygaśnie w ciągu 30 dni lub już wygasło")

    def display_all_groups(self, kadra_zarzadcza, kadra_kierownicza, pracownicy):
        """
        Wyświetla tabele dla wszystkich grup zawodowych.
        """
        if kadra_zarzadcza:
            self.display_group_tables(kadra_zarzadcza, "Kadra Zarządzająca")

        if kadra_kierownicza:
            self.display_group_tables(kadra_kierownicza, "Kadra Kierownicza")

        if pracownicy:
            self.display_group_tables(pracownicy, "Pracownicy")