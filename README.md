# EduMonitor - Monitorowanie szkoleń pracowników

## Opis projektu
EduMonitor to narzędzie do monitorowania szkoleń pracowników, które umożliwia przetwarzanie danych z plików CSV, porównywanie ich z danymi pobranymi z zewnętrznego URL oraz wyświetlanie wyników w konsoli w formie tabel. Dodatkowo, program może generować listy pracowników do przeszkolenia w formacie HTML, obejmujące pracowników, którym kończy się szkolenie lub których szkolenie już wygasło.

## Wymagania
- Python 3.10 lub nowszy
- `prettytable` (instalacja: `pip install prettytable`)
- `urllib3` (instalacja: `pip install urllib3`)

## Instalacja
1. Sklonuj repozytorium na lokalny dysk.
2. Zainstaluj wymagane biblioteki:
   ```bash
   pip install prettytable urllib3
   ```

## Uruchamianie
Program można uruchomić, używając flagi `--csv` . Aby wyniki były wyświetlane w konsoli w formie tabeli, należy dodatkowo użyć flagi `--shell`:
   ```python
   python3 edumonitor.py --csv <ścieżka do pliku CSV> --shell
   python3 edumonitor.py --csv <ścieżka do pliku CSV> --lists-html
   python3 edumonitor.py --csv <ścieżka do pliku CSV> --lists-html --shell
   python3 edumonitor.py --csv <ścieżka do pliku CSV> --report-html
   python3 edumonitor.py --test-csv --shell
   python3 edumonitor.py --test-csv --lists-html
   python3 edumonitor.py --test-csv --report-html
   ```
Po wczytaniu pliku CSV (w formacie `cp1250`), program przetwarza dane pracowników, porównuje je z danymi pobranymi z URL (zdefiniowanego w pliku konfiguracyjnym `config/config.ini`) i wyświetla wyniki na konsoli w formie tabeli, jeśli podano flagę `--shell`.

## Flagi i opcje
- `--csv <ścieżka do pliku>`: Wczytuje dane z pliku CSV i wyświetla je po przetworzeniu oraz porównaniu z danymi z bazy URL.
- `--shell`: Wyświetla dane w konsoli w formie tabeli.
- `--lists-html`: Generuje listy pracowników do przeszkolenia w formacie HTML. Tworzy pliki HTML z pracownikami, którym kończy się szkolenie lub których szkolenie się skończyło, w katalogu `output/lists/`.
- `--test-csv`: Używa pliku CSV testowego `tests/test_files/dane_testowe.csv`, co jest przydatne do testowania bez konieczności podawania ścieżki.
- `--report-html`: Generuje raport o stanie wyszkolenia pracowników w formacie HTML, zapisując go w katalogu `output/reports/`.
- `-h / --help`: Wyświetla pomoc dotyczącą dostępnych opcji.

## Funkcjonalności
- **Wczytywanie danych z CSV**: Program przetwarza pliki CSV zawierające informacje o pracownikach i ich szkoleniach.
- **Porównanie z bazą URL**: Program pobiera dane o pracownikach z zewnętrznego URL, porównuje je z danymi z CSV, dodając informacje o stanowisku i email pracownika, jeśli istnieją w bazie danych.
- **Filtrowanie dat szkolenia**: Program automatycznie rozpoznaje daty w formacie dd.mm.rrrr...dd.mm.rrrr i klasyfikuje pracowników na podstawie daty ważności szkolenia (ważne, zbliżające się do końca, po terminie).
- **Generowanie tabel**: Program generuje tabele z podziałem na grupy zawodowe (kadra zarządzająca, kadra kierownicza, pracownicy) oraz wyświetla pracowników z aktualnym, wygasającym i już wygasłym szkoleniem.
- **Generowanie list HTML**: Program generuje listy HTML z pracownikami, którym kończy się szkolenie lub których szkolenie już wygasło. Listy są zapisywane w katalogu `output/lists/` i podzielone na grupy zawodowe.
- **Generowanie raportów HTML**: Program umożliwia generowanie raportów o stanie wyszkolenia pracowników w formacie HTML, podzielonych na grupy zawodowe. Raport zawiera liczbę pracowników z ważnymi, wygasającymi oraz przeterminowanymi szkoleniami. Raport jest generowany z timestampem w nazwie pliku i jest dostępny pod flagą `--report-html`.
- **Wyświetlanie wyników**: Program wyświetla dane w formie tabeli w konsoli (przy użyciu flagi `--shell`), pokazując m.in. informacje o tym, czy pracownik istnieje w bazie URL (`db_url = True`).
- **Mockowanie połączeń**: Podczas testowania, połączenia z URL są mockowane, co umożliwia szybkie i niezależne testowanie funkcji sieciowych.
- **Lepsza obsługa wyjątków**: Wprowadzono dekorator @log_exceptions, który automatycznie loguje wyjątki występujące podczas działania programu, ułatwiając diagnozowanie problemów.

## Przykład działania
Po uruchomieniu programu:
   ```python
   python3 edumonitor.py --csv <ścieżka do pliku CSV> --shell
   ```

```sql
+----------+----------+------------------+-----------------+----------------------+--------+-----------------------------------------------+------------------------------+
| Nazwisko |   Imię   |    Jednostka     | Nazwa szkolenia |    Data szkolenia    | db_url |                   Stanowisko                  |            Email             |
+----------+----------+------------------+-----------------+----------------------+--------+-----------------------------------------------+------------------------------+
|  WAYNE   |  BRUCE   |      Batman      |       brak      | Ważne do 24.12.2022  |  True  |    Wiceprezes Zarządu Dyrektor ds. Rozwoju    |   bruce.wayne@company.com    |
|  STORM   |  ORORO   |      Storm       |       brak      | Ważne do 26.05.2023  |  True  |                                               |   ororo.storm@company.com    |
|  WILSON  |   WADE   |     Deadpool     |       brak      | Ważne do 19.01.2024  | False  |                                               |                              |
|  QUILL   |  PETER   |    Star-Lord     |       brak      | Ważne do 24.02.2024  |  True  |                                               |   peter.quill@company.com    |
| RICHARDS |   REED   | Mister Fantastic |       brak      | Ważne do 09.04.2024  |  True  |           Z-ca Dyrektora ds. Rozwoju          |  reed.richards@company.com   |
| GRAYSON  |   DICK   |    Nightwing     |       brak      | Ważne do 11.01.2023  |  True  |            Dyrektor ds.Operacyjnych           |   dick.grayson@company.com   |
+----------+----------+------------------+-----------------+----------------------+--------+-----------------------------------------------+------------------------------+
```

## Plik konfiguracyjny
W projekcie znajduje się przykładowy plik konfiguracyjny `config/config_example.ini`. Skopiuj ten plik, zmień nazwę na `config.ini`, a następnie dostosuj go do swoich potrzeb, wprowadzając odpowiednie ścieżki oraz URL do pobierania danych:
```ini
# config/config.ini
# main configuration file
#
[DEFAULT]
LOG = logs/edumonitor.log
DATE_FORMAT = %d.%m.%Y
#
# Możliwe wartości: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL_CONSOLE = WARNING
LOG_LEVEL_FILE = INFO
#
#
[OUTPUT]
LISTS_DIR = output/lists/
#
[DATABASE]
# URL do pobierania danych o pracownikach
URL = https://example.com/data
#
VERIFY_SSL = True
```
## Testowanie
Projekt zawiera testy jednostkowe, które sprawdzają poprawność wczytywania danych z plików CSV oraz JSON, a także funkcji porównujących dane pracowników. Aby uruchomić testy, użyj następującego polecenia:

```bash
python3 -m unittest discover -s tests
```

**Testy obejmują:**
- Wczytywanie danych z plików CSV (`CSVLoader.load_file_stream()`).
- Filtrowanie i walidację danych z CSV (`CSVLoader.filter_file()`).
- Porównanie danych z pliku CSV z bazą danych z URL (`EmployeeManager.check_employee_in_db()`).
- Generowanie raportów HTML (`HTMLReportGenerator`).
- Obsługa wyjątków i logowania błędów (`fetch_employee_data_from_url()`).
- Wyświetlanie danych w konsoli (`TableDisplay`).

Testy są mockowane, co umożliwia symulowanie odpowiedzi z URL i unikanie rzeczywistych połączeń podczas testów.

## Logowanie
Poziom logowania można ustawić na dwa sposoby:
1. **Z pliku konfiguracyjnego**: 
   - **LOG_LEVEL_CONSOLE**: Ustawia poziom logowania dla wyjścia na konsolę. Możliwe wartości to `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.
   - **LOG_LEVEL_FILE**: Ustawia poziom logowania dla zapisu do pliku logów.
2. **Za pomocą zmiennych środowiskowych**: Możesz ustawić poziomy logowania dla konsoli i pliku, ustawiając odpowiednie zmienne środowiskowe:
   ```bash
   export LOG_LEVEL_CONSOLE=DEBUG
   export LOG_LEVEL_FILE=INFO
   ```
Jeśli zmienne środowiskowe są ustawione, mają one pierwszeństwo nad wartościami z pliku konfiguracyjnego.
Podczas testów jednostkowych logger jest mockowany, co pozwala na wyciszenie niepotrzebnych komunikatów w trakcie testowania. Dzięki temu testy przebiegają szybciej, a wyjście na konsolę jest czystsze.
## Dokumentacja

Szczegółowy opis działania programu, przepływu danych oraz struktury projektu znajdziesz w [docs/data_flow.pdf](docs/data_flow.md).

## Licencja
Projekt jest dostępny na licencji [MIT](LICENCE.md).
