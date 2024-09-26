# Przepływ danych w projekcie EduMonitor

## Ogólny przepływ danych

1. **Odczyt plików CSV i przetwarzanie danych:**
    - Użytkownik uruchamia program z flagą `--csv`, podając ścieżkę do pliku CSV.
    - Moduł `csv_loader.py` wczytuje dane z pliku CSV, przetwarzając je na listę obiektów klasy `Employee`. 
    - Wiersze są walidowane pod kątem poprawności danych (np. liczba kolumn, brakujące informacje), a niepoprawne wiersze są pomijane.
    - Przetworzone dane są konwertowane na obiekty klasy `Employee` i zapisywane do pliku JSON w katalogu `input/`.

2. **Pobieranie danych z zewnętrznego źródła (URL):**
    - Moduł `db_fetcher.py` pobiera dane pracowników z zewnętrznego API, którego adres URL jest zdefiniowany w pliku konfiguracyjnym `config/config.ini`.
    - Dane pobrane z URL zawierają takie informacje jak: `nazwisko`, `imie`, `stanowisko`, `email`.
    - Weryfikacja certyfikatu SSL może być pominięta na podstawie ustawień w pliku konfiguracyjnym.

3. **Porównanie danych z CSV z bazą danych URL:**
    - Moduł `employee_management.py` porównuje dane z CSV z danymi pobranymi z URL. 
    - Porównanie jest wykonywane na podstawie `nazwiska` i `imienia`.
    - W przypadku zgodności danych z obu źródeł, obiekty klasy `Employee` są aktualizowane o dodatkowe informacje, takie jak:
        - `db_url`: flaga ustawiana na `True`, jeśli pracownik istnieje w bazie URL.
        - `stanowisko`: stanowisko pracownika z bazy URL.
        - `email`: adres email pracownika z bazy URL.

4. **Zapis zaktualizowanych danych do JSON:**
    - Po porównaniu danych, zaktualizowane obiekty klasy `Employee` są zapisywane do pliku JSON w katalogu `input/` z nazwą zawierającą timestamp.

5. **Wyświetlanie wyników w konsoli (opcjonalne):**
    - Jeżeli program zostanie uruchomiony z flagą `--shell`, moduł `table_display.py` wyświetla wyniki w formie tabeli w konsoli.
    - Pracownicy są grupowani na kadry zarządzające, kierownicze oraz pozostałych, a każda grupa jest podzielona według statusu ważności szkolenia: aktualne, zbliżające się do wygaśnięcia, przeterminowane.

6. **Wyświetlanie wyników w konsoli (opcjonalne):**
    - Jeżeli program zostanie uruchomiony z flagą `--generate-training-lists`, moduł html_list_generator.py generuje osobne listy w formacie HTML dla każdej grupy zawodowej:
      - Kadra Zarządzająca
      - Kadra Kierownicza
      - Pracownicy
      > Listy są zapisywane w katalogu `output/lists/`.

## Moduły w projekcie

### 1. `csv_loader.py`
- **Opis**: Moduł odpowiedzialny za wczytywanie i filtrowanie danych z pliku CSV.
- **Funkcjonalności**:
  - Wczytuje dane z pliku CSV i sprawdza poprawność liczby kolumn oraz zawartości wierszy.
  - Pomija niepoprawne wiersze i loguje informacje o błędach.
  - Przetwarza dane na listę wierszy gotowych do dalszego przetwarzania i porównania z bazą danych URL.

### 2. `db_fetcher.py`
- **Opis**: Moduł do pobierania danych pracowników z zewnętrznego źródła (API).
- **Funkcjonalności**:
  - Używa biblioteki `urllib3` do wykonywania żądania HTTP GET na URL pobrany z pliku konfiguracyjnego.
  - Dane są pobierane w formacie JSON i zwracane jako lista obiektów, które mogą być porównane z danymi z CSV.
  - Obsługuje timeouty, błędy połączeń oraz różne statusy HTTP, takie jak 404 (nie znaleziono) i 500 (błąd serwera).

### 3. `employee_management.py`
- **Opis**: Moduł do zarządzania porównywaniem danych pracowników z CSV oraz z bazy URL.
- **Funkcjonalności**:
  - Porównuje dane na podstawie `nazwiska` i `imienia`.
  - Aktualizuje obiekty klasy `Employee` o informacje takie jak `stanowisko`, `email` oraz ustawia flagę `db_url`, jeśli pracownik został znaleziony w bazie URL.
  - Oferuje możliwość filtrowania pracowników na podstawie stanowisk, grupując ich według kadry zarządzającej, kierowniczej i pracowników.

### 4. `json_loader.py`
- **Opis**: Moduł odpowiedzialny za konwersję danych z CSV na format JSON oraz za odczyt i zapis danych w formacie JSON.
- **Funkcjonalności**:
  - Konwertuje przetworzone dane CSV na obiekty klasy `Employee` i zapisuje je do pliku JSON.
  - Oferuje możliwość ładowania najnowszego pliku JSON na podstawie daty w nazwie pliku.
  - W przypadku problemów z zapisem lub odczytem danych, loguje odpowiednie błędy.

### 5. `employee.py`
- **Opis**: Klasa reprezentująca pracownika.
- **Funkcjonalności**:
  - Przechowuje informacje o pracowniku, takie jak `nazwisko`, `imie`, `jednostka`, `nazwa szkolenia`, `data szkolenia`, `data ważności szkolenia`, `stanowisko`, `email`, oraz status obecności w bazie URL (`db_url`).
  - Oferuje metody do obliczania liczby dni do wygaśnięcia szkolenia oraz sprawdzania, czy szkolenie jest ważne, zbliżające się do wygaśnięcia lub przeterminowane.

### 6. `table_display.py`
- **Opis**: Moduł do wyświetlania danych w formie tabeli w konsoli.
- **Funkcjonalności**:
  - Grupuje pracowników według stanowisk oraz statusu ważności szkolenia.
  - Wyświetla dane w formie tabeli, uwzględniając dodatkowe informacje o pracowniku, takie jak `stanowisko` i `email`, jeśli dane te są dostępne z bazy URL.

### 7. `html_list_generator.py`
- **Opis**: Moduł odpowiedzialny za generowanie list pracowników w formacie HTML.
- **Funkcjonalności**:
  - Generuje osobne listy dla różnych grup zawodowych (kadra zarządzająca, kadra kierownicza, pracownicy).
  - Listy są zapisywane w katalogu `output/lists/`.

### 8. `logger_setup.py`
- **Opis**: Moduł odpowiedzialny za konfigurację loggera.
- **Funkcjonalności**:
  - Umożliwia logowanie informacji, ostrzeżeń oraz błędów do pliku i konsoli.
  - Logi są zapisywane w pliku z timestampem, co ułatwia analizę działania programu.
  - Podczas testów logger może być mockowany, aby wyciszyć zbędne komunikaty.

### 9. `arg_parser.py`
- **Opis**: Moduł odpowiedzialny za obsługę argumentów z linii komend.
- **Funkcjonalności**:
  - Umożliwia uruchomienie programu z flagami `--csv`, `--shell`, `--generate-training-lists`, co pozwala na różne tryby pracy programu.
  - Obsługuje argumenty dla ścieżki do pliku CSV oraz wyświetlania danych w konsoli w formie tabeli.

## Przykładowy przepływ danych

1. **Uruchomienie programu z plikiem CSV**:
    ```bash
    python3 edumonitor.py --csv <ścieżka do pliku CSV> --shell
    ```
    - Program wczytuje dane z CSV, porównuje je z danymi z URL, a następnie zapisuje wynik do pliku JSON oraz wyświetla dane w formie tabeli w konsoli (jeśli podano flagę `--shell`).

2. **Pobranie danych z URL**:
    - Program pobiera dane z URL zdefiniowanego w pliku `config.ini`:
    ```ini
    [DATABASE]
    URL = https://example.com/data
    ```

3. **Porównanie i zapis danych**:
    - Dane z CSV są porównywane z danymi z URL. W przypadku dopasowania danych, obiekty `Employee` są aktualizowane o dodatkowe informacje z bazy URL.
    - Zaktualizowane dane są zapisywane do pliku JSON w katalogu `input/`.

4. **Wyświetlenie wyników w konsoli**:
    - Jeśli użyto flagi `--shell`, dane są wyświetlane w formie tabeli z dodatkowymi informacjami o pracownikach, takimi jak `stanowisko`, `email` oraz flaga `db_url`, wskazująca, czy pracownik został znaleziony w bazie URL.

5. **Generowanie list pracowników w formacie HTML:**:
    - Jeśli użyto flagi `--generate-training-lists`, generowane są osobne listy dla kadry zarządzającej, kadry kierowniczej oraz pracowników, zapisywane w katalogu `output/lists/`.
    