<!--edumonitor/docs/data_flow.md-->

# Przepływ danych w projekcie EduMonitor

## Ogólny przepływ danych

1. **Odczyt plików lokalnych (CSV):**
    - Użytkownik uruchamia program z opcją wczytywania danych z pliku CSV lub w trybie testowym.
    - Moduł `csv_loader.py` przetwarza dane i zamienia je na listę obiektów klasy `Employee`, które zawierają informacje takie jak `Nazwisko`, `Imię`, `Jednostka`, `Nazwa szkolenia`, `Data szkolenia`, `Ważne do`.

2. **Filtrowanie dat szkolenia:**
    - Program automatycznie rozpoznaje daty szkolenia i daty wygaśnięcia z pola `Okres szkolenia` w pliku CSV.
    - `Okres szkolenia` jest podawany w formacie `dd.mm.rrrr...dd.mm.rrrr`, gdzie pierwsza data to `data_szkolenia`, a druga to `wazne_do` (data ważności szkolenia).
    - Przykład formatu: `24.12.2023...24.12.2024`.
    - Program waliduje daty, upewniając się, że są w poprawnym formacie. W przypadku błędu formatu, wiersz jest pomijany.

3. **Pobieranie danych z URL:**
    - Program odczytuje URL z pliku konfiguracyjnego `config/config.ini`.
    - Moduł `db_fetcher.py` pobiera dane z zewnętrznego źródła przy użyciu `urllib3`, z pominięciem weryfikacji certyfikatu SSL.
    - Wynikowe dane zawierają informacje o użytkownikach, takie jak `nazwisko`, `imie`, `dzial`, `stanowisko`, `email` i są zwracane w formacie JSON.

4. **Porównanie danych:**
    - Moduł `employee_class.py` zawiera metody do porównywania danych z CSV z danymi pobranymi z URL.
    - Klucze używane do porównania:
        - `Nazwisko` (plik) vs `nazwisko` (URL)
        - `Imię` (plik) vs `imie` (URL)
    - Jeśli dane pasują, obiekt klasy `Employee` aktualizuje dodatkowe pola:
        - `db_url` - wartość `True`, jeśli użytkownik istnieje w bazie danych z URL.
        - `stanowisko` i `email` - pobrane z bazy danych z URL, jeśli są dostępne, lub pozostają puste.

5. **Generowanie tabel i wyświetlanie wyników:**
    - Zaktualizowane dane pracowników są przetwarzane w module `table_data.py`, który generuje tabele dla grup zawodowych (kadra zarządzająca, kadra kierownicza, pracownicy).
    - Każda grupa jest podzielona na pracowników z aktualnym szkoleniem oraz tych, których szkolenie wygaśnie w ciągu 30 dni lub już wygasło.
    - Tabele są wyświetlane na konsoli za pomocą modułu `table_display.py`, ale tylko w przypadku podania flagi `--shell`.

## Moduły w projekcie

### 1. `csv_loader.py`
- Moduł odpowiedzialny za wczytywanie i przetwarzanie pliku CSV. Dane są konwertowane na listę obiektów `Employee`, które zawierają takie pola jak `Nazwisko`, `Imię`, `Jednostka`, `Nazwa szkolenia`, `Data szkolenia`, `Ważne do`.

### 2. `db_fetcher.py`
- Moduł odpowiedzialny za pobieranie danych z zewnętrznego URL przy użyciu biblioteki `urllib3`.
- Zwracane dane są w formacie JSON i zawierają informacje takie jak `nazwisko`, `imie`, `dzial`, `stanowisko`, `email`.

### 3. `employee_class.py`
- Klasa `Employee` zawiera metody do przetwarzania danych pracowników, porównywania ich z danymi z URL oraz filtrowania pracowników według stanowiska.
- Metody takie jak `is_expired()`, `is_soon_expiring()` oraz `is_valid_training()` służą do określenia statusu ważności szkoleń.

### 4. `table_data.py`
- Moduł odpowiedzialny za generowanie tabel dla grup zawodowych (kadra zarządzająca, kadra kierownicza, pracownicy).
- Każda grupa jest dzielona na pracowników z aktualnym szkoleniem oraz tych, których szkolenie wygasa lub już wygasło.

### 5. `table_display.py`
- Moduł odpowiedzialny za wyświetlanie danych w formie tabeli, w tym dane pracowników z CSV oraz dodatkowe kolumny (`db_url`, `stanowisko`, `email`), jeśli pracownik istnieje w bazie danych z URL.

## Przykładowy przepływ danych

1. **Uruchomienie programu**: Użytkownik uruchamia program z plikiem CSV:
    ```bash
    python3 edumonitor.py --csv patch/to/file.csv --shell
    ```
    Plik CSV zostaje odczytany, a dane są porównane z danymi pobranymi z URL. Wyniki są wyświetlane na konsoli, jeśli podano flagę `--shell`.

2. **Pobranie danych z URL**: Program pobiera dane z URL zdefiniowanego w pliku url_config.ini:
    ```ini
    [DEFAULT]
    URL = https://example.com/data
    ```

3. **Porównanie i wyświetlenie wyników**: Dane z CSV są porównywane z danymi z URL. Jeśli wartości `Nazwisko`, `Imię` pasują, wyświetlana jest informacja o użytkowniku wraz z jego stanowiskiem, emailem oraz informacją, czy istnieje w bazie danych (`db_url = True`).
