""" src/csv_loader.py """

import csv
from datetime import datetime
from src.employee_class import Employee
from src.logger_setup import setup_logger
from src.config_loader import get_date_format

# Inicjalizacja loggera
logger = setup_logger()

def load_file(csv_file):
    """
    Wczytuje dane z pliku CSV i zwraca surowe dane.
    
    Args:
        csv_file (str): Ścieżka do pliku CSV.
    
    Returns:
        list: Lista wierszy z pliku CSV.
    
    Logi:
        Informacje o wczytywaniu pliku, liczbie wierszy oraz liczbie odrzuconych wierszy.
    """
    logger.info(f"Rozpoczęto wczytywanie pliku CSV: {csv_file}")
    try:
        with open(csv_file, mode='r', encoding='cp1250') as file:
            reader = csv.reader(file, delimiter=';')
            data = list(reader)
            logger.info(f"Plik {csv_file} wczytano poprawnie. Liczba wierszy: {len(data)}")
    except FileNotFoundError:
        logger.error(f"Plik {csv_file} nie został znaleziony.")
        return []
    except Exception as e:
        logger.error(f"Błąd podczas otwierania pliku {csv_file}: {e}")
        return []

    return data

def filter_file(raw_data):
    """
    Filtruje surowe dane CSV, tworzy obiekty klasy Employee, konwertuje daty na obiekty datetime.
    
    Args:
        raw_data (list): Surowe dane z pliku CSV.
    
    Returns:
        list: Lista obiektów klasy Employee.
    
    Raises:
        ValueError: Jeśli format daty w polu 'okres_szkolenia' jest niepoprawny.
        KeyError: Jeśli wiersz nie zawiera wystarczającej liczby kolumn.
    
    Logi:
        Błędy formatowania daty oraz puste pola są logowane z poziomem ERROR.
        Informacje o liczbie poprawnych i odrzuconych rekordów.
    """
    employees = []
    date_format = get_date_format()
    rejected_rows = 0  # Licznik odrzuconych wierszy

    # Pomijanie pierwszych 7 wierszy (nagłówki)
    filtered_data = raw_data[7:]
    
    for row in filtered_data:
        try:
            # Sprawdzenie, czy wiersz zawiera odpowiednią liczbę kolumn
            if len(row) <= 7 or row[1] == '':
                logger.warning(f"Niepoprawny wiersz, zbyt mało kolumn lub brak nazwiska: {row}")
                continue

            nazwisko = row[1]
            imie = row[2]
            jednostka = row[4]
            nazwa_szkolenia = row[7]
            okres_szkolenia = row[8]
            
            # Wydobycie obu dat z okresu szkolenia
            daty = okres_szkolenia.split('...')
            if len(daty) != 2:
                raise ValueError(f"Błędny format okresu szkolenia dla {nazwisko}, {imie}: {okres_szkolenia}")
            
            # Konwersja dat na obiekty datetime przy użyciu formatu z pliku konfiguracyjnego
            data_szkolenia = datetime.strptime(daty[0].strip(), date_format)
            wazne_do = datetime.strptime(daty[1].strip(), date_format)
            logger.debug(f"Data szkolenia: {data_szkolenia}, Ważne do: {wazne_do}")
            
            # Tworzenie obiektu Employee
            employee = Employee(nazwisko, imie, jednostka, nazwa_szkolenia, data_szkolenia, wazne_do)
            employees.append(employee)
            logger.debug(f"Dodano pracownika: {nazwisko}, {imie}, {jednostka}")
        
        except ValueError as e:
            logger.error(f"Błąd formatu daty dla {nazwisko}, {imie}: {e}")
            rejected_rows += 1
        except KeyError as e:
            logger.error(f"Błąd w wierszu danych: {e}")
            rejected_rows += 1
    
    logger.info(f"Zakończono filtrowanie danych. Wczytano {len(employees)} poprawnych pracowników, odrzucono {rejected_rows} wierszy.")
    return employees
