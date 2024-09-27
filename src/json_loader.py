""" src.json_loader.py """

import os
import json
from datetime import datetime
from src.config_loader import ConfigLoader
from src.employee import Employee
from src.logger_setup import setup_logger

class JSONLoader:
    """
    Klasa do przetwarzania danych z plików JSON.
    """

    def __init__(self, input_dir='input'):
        self.logger = setup_logger()
        self.config_loader = ConfigLoader()
        self.date_format = self.config_loader.get_date_format()
        self.input_dir = input_dir

    def convert_to_json_structure(self, filtered_data):
        """
        Konwertuje przefiltrowane dane CSV do struktury obiektów Employee.
        """
        employees = []
        for row in filtered_data:
            try:
                self.logger.debug(f"Konwertowanie wiersza CSV na JSON: {row}")
                data_szkolenia, data_waznosci = row[8].split("...")
            except ValueError:
                data_szkolenia = ''
                data_waznosci = ''

            employee = Employee(
                nazwisko=row[1],
                imie=row[2],
                kod=row[3],
                jednostka_organizacyjna=row[4],
                nazwa_szkolenia=row[7],
                data_szkolenia=data_szkolenia.strip(),
                data_waznosci=data_waznosci.strip()
            )

            self.logger.debug(f"Pracownik z CSV (JSON): {employee}")
            employees.append(employee)


            '''employees.append(Employee(
                nazwisko=row[1],
                imie=row[2],
                kod=row[3],
                jednostka_organizacyjna=row[4],
                nazwa_szkolenia=row[7],
                data_szkolenia=data_szkolenia.strip(),
                data_waznosci=data_waznosci.strip()
            ))'''


        return employees

    def save_to_json(self, employees):
        """
        Zapisuje listę obiektów Employee do pliku JSON w katalogu input/.
        """
        input_dir = os.path.join(os.getcwd(), 'input')
        os.makedirs(input_dir, exist_ok=True)

        timestamp = datetime.now().strftime(self.date_format)
        json_filename = f"ukonczone_szkolenia_{timestamp}.json"
        json_output_path = os.path.join(input_dir, json_filename)

        # Konwersja obiektów Employee do formatu JSON
        data = [{
            "nazwisko": emp.nazwisko,
            "imie": emp.imie,
            "kod": emp.kod,
            "jednostka_organizacyjna": emp.jednostka_organizacyjna,
            "nazwa_szkolenia": emp.nazwa_szkolenia,
            "data_szkolenia": emp.data_szkolenia.strftime("%d.%m.%Y") if emp.data_szkolenia else "",
            "data_waznosci": emp.data_waznosci.strftime("%d.%m.%Y") if emp.data_waznosci else "",
            "db_url": emp.db_url,
            "stanowisko": emp.stanowisko,
            "email": emp.email
        } for emp in employees]

        for emp in employees:
            self.logger.debug(emp)

        try:
            with open(json_output_path, mode='w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            self.logger.info(f"Plik został zapisany jako JSON: {json_output_path}")
        except Exception as e:
            self.logger.error(f"Błąd podczas zapisu do JSON: {e}")

    def find_latest_json_file(self):
        """
        Znajduje najnowszy plik JSON w katalogu input/ na podstawie timestamp w nazwie pliku.
        Zwraca pełną ścieżkę do pliku JSON.
        """
        json_files = [f for f in os.listdir(self.input_dir) if f.endswith('.json')]
        if not json_files:
            self.logger.warning("Brak plików JSON w katalogu input/")
            return None

        # Sortowanie po dacie, aby znaleźć najnowszy plik JSON (plik powinien zawierać timestamp w nazwie)
        json_files.sort(reverse=True, key=lambda f: datetime.strptime(f.split('_')[-1].replace('.json', ''), self.date_format))

        latest_json = os.path.join(self.input_dir, json_files[0])
        self.logger.info(f"Znaleziono najnowszy plik JSON: {latest_json}")
        return latest_json

    def load_employees_from_json(self):
        """
        Ładuje dane z najnowszego pliku JSON i zwraca listę obiektów Employee.
        """
        latest_json = self.find_latest_json_file()
        if latest_json:
            try:
                with open(latest_json, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)
                    employees = [Employee(**entry) for entry in data]
                    self.logger.info(f"Załadowano dane z pliku {latest_json}")
                    return employees
            except Exception as e:
                self.logger.error(f"Błąd podczas ładowania danych z pliku JSON: {e}")
                return None
        return None