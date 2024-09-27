# EduMonitor - Monitorowanie szkoleń pracowników

## Opis projektu
EduMonitor to narzędzie do monitorowania szkoleń pracowników, które umożliwia przetwarzanie danych z plików CSV, porównywanie ich z danymi pobranymi z zewnętrznego URL oraz wyświetlanie wyników w konsoli w formie tabel. Program obsługuje również generowanie raportów i list pracowników w formacie HTML, dotyczących szkoleń, które wkrótce wygasną lub już wygasły.

Dodatkowo program umożliwia generowanie osobnych list w formacie HTML dla różnych grup zawodowych, takich jak:

- Kadra zarządzająca
- Kadra kierownicza
- Pracownicy

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
Program można uruchomić, używając flagi `--csv`, która wczytuje dane z pliku CSV i przetwarza je. Aby dodatkowo wyświetlić wyniki w konsoli w formie tabeli, należy użyć flagi `--shell`. Przykłady użycia:
   ```python
   python3 edumonitor.py --csv <ścieżka do pliku CSV>
   python3 edumonitor.py --csv <ścieżka do pliku CSV> --shell
   python3 edumonitor.py --shell
   ```

## Flagi i opcje
- `--csv <ścieżka do pliku>`: Wczytuje dane z pliku CSV, przetwarza je oraz porównuje z danymi z bazy URL. Dane po przetworzeniu są zapisywane do pliku JSON w katalogu `input/`.
- `--shell`: Wyświetla dane w konsoli w formie tabeli, po przetworzeniu pliku CSV i porównaniu z danymi z bazy URL.
- `--generate-training-lists`: Generuje osobne listy w formacie HTML dla różnych grup zawodowych (kadra zarządzająca, kadra kierownicza, pracownicy), zapisując je w katalogu `output/lists/`.
- `--generate-training-report`: Generuje raport o stanie wyszkolenia pracowników w formacie HTML, zawierający podsumowanie liczby pracowników z ważnymi, wygasającymi i przeterminowanymi szkoleniami. Raport jest zapisywany w katalogu `output/reports/`.
- `-h / --help`: Wyświetla pomoc dotyczącą dostępnych opcji.

## Funkcjonalności
- **Wczytywanie i porównanie danych**: Program wczytuje pliki CSV zawierające informacje o pracownikach i ich szkoleniach, a następnie zapisuje te dane do formatu JSON. W trakcie przetwarzania, dane pracowników są automatycznie porównywane z danymi pobranymi z zewnętrznego URL, co umożliwia uzupełnienie informacji o stanowisku i adresie email pracownika, jeśli są one dostępne w bazie URL.
- **Generowanie tabel**: Program generuje tabele z podziałem na grupy zawodowe (kadra zarządzająca, kadra kierownicza, pracownicy) oraz wyświetla pracowników z aktualnym, wygasającym i już wygasłym szkoleniem, jeśli użyto flagi `--shell`.
- **Generowanie list w formacie HTML**: Program generuje osobne listy w formacie HTML dla trzech grup zawodowych:
   - Kadra zarządzająca
   - Kadra kierownicza
   - Pracownicy
   
   Listy są zapisywane w katalogu `output/lists/`.

- **Generowanie raportu o stanie wyszkolenia pracowników**: Program generuje raport HTML zawierający liczbę pracowników z ważnymi, wygasającymi oraz przeterminowanymi szkoleniami, podzieloną na trzy grupy: kadra zarządzająca, kadra kierownicza, pracownicy. Raport jest zapisywany w katalogu `output/reports/`.

## Przykład działania

1. Konwersja danych z pliku CSV:
   ```python
   python3 edumonitor.py --csv <ścieżka do pliku CSV> --shell
   ```

2. Wyświetlanie danych w konsoli:
   ```python
   python3 edumonitor.py --shell
   ```

   ```sql
   Pracownicy - Szkolenie wygaśnie w ciągu 30 dni lub już wygasło (Liczba pracowników: 1)
   +--------------+----------+-------+--------------------+----------------+------------+
   | Nazwisko     | Imię     | Dział | Nazwa szkolenia    | Data szkolenia | Ważne do   |
   +--------------+----------+-------+--------------------+----------------+------------+
   | WAYNE        | BRUCE    |   DC  | Security awareness | 26.06.2023     | 24.06.2024 |
   +--------------+----------+-------+--------------------+----------------+------------+
   ```

3. Generowanie list pracowników w formacie HTML:
   ```python
   python3 edumonitor.py --generate-training-lists
   ```

   Po uruchomieniu polecenia program wygeneruje trzy osobne listy:

   - kadra_zarzadzajaca_lista.html
   - kadra_kierownicza_lista.html
   - pracownicy_lista.html

4. Generowanie raportu o stanie wyszkolenia pracowników:
   ```python
   python3 edumonitor.py --generate-training-report
   ```
   Po uruchomieniu polecenia raport zostanie zapisany w katalogu `output/reports/` pod nazwą `raport_wyszkolenia_<data>.html`.

## Plik konfiguracyjny
W projekcie znajduje się przykładowy plik konfiguracyjny `config/config_example.ini`. Skopiuj ten plik, zmień nazwę na `config.ini`, a następnie dostosuj go do swoich potrzeb, wprowadzając odpowiednie ścieżki oraz URL do pobierania danych:
```ini
# config/config.ini
# main configuration file
#
[DEFAULT]
LOG = logs/edumonitor.log
DATE_FORMAT = %Y-%m-%d
#
# Możliwe wartości: DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_LEVEL_CONSOLE = WARNING
LOG_LEVEL_FILE = INFO
#
#
[OUTPUT]
HTML_LISTS = output/lists/
HTML_REPORTS = output/reports/
#
[DATABASE]
# URL do pobierania danych o pracownikach
URL = https://example.com/data
VERIFY_SSL = True
```

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
