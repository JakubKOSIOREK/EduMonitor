""" src.json_loader.py """

import os
import json
from datetime import datetime
from src.config_loader import ConfigLoader
from src.logger_setup import setup_logger

class JSONLoader:
    """
    Klasa do przetwarzania danych i zapisu do pliku JSON.
    """

    def __init__(self):
        self.logger = setup_logger()
        self.config_loader = ConfigLoader()
        self.date_format = self.config_loader.get_date_format()

    def convert_to_json_structure(self, filtered_data):
        """
        Konwertuje przefiltrowane dane CSV do pożądanej struktury JSON.
        """
        json_data = []
        for row in filtered_data:
            try:
                # Rozdzielenie 'okres' na dwie daty: 'data szkolenia' i 'data ważności'
                data_szkolenia, data_waznosci = row[8].split("...")
            except ValueError:
                data_szkolenia = ''
                data_waznosci = ''

            json_data.append({
                "nazwisko": row[1],
                "imie": row[2],
                "kod": row[3],
                "jednostka_organizacyjna": row[4],
                "nazwa_szkolenia": row[7],
                "data_szkolenia": data_szkolenia.strip(),
                "data_waznosci": data_waznosci.strip()
            })
        return json_data

    def save_to_json(self, data):
        """
        Zapisuje przefiltrowane dane do pliku JSON w katalogu input/.
        """
        # Tworzenie katalogu input/ jeśli nie istnieje
        input_dir = os.path.join(os.getcwd(), 'input')
        os.makedirs(input_dir, exist_ok=True)

        # Generowanie nazwy pliku JSON z timestamp
        timestamp = datetime.now().strftime(self.date_format)
        json_filename = f"ukonczone_szkolenia-{timestamp}.json"
        json_output_path = os.path.join(input_dir, json_filename)

        try:
            with open(json_output_path, mode='w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
            self.logger.info(f"Plik został zapisany jako JSON: {json_output_path}")
        except Exception as e:
            self.logger.error(f"Błąd podczas zapisu do JSON: {e}")
