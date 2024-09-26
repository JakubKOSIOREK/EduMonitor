# CHANGELOG

## [Undefined] - 2024-09-26 no.2
### Zmiany:
- **Przeniesienie logiki przetwarzania argumentu CSV**: Funkcja odpowiedzialna za walidację i przetwarzanie pliku CSV została przeniesiona z `edumonitor.py` do modułu `arg_parser.py`. 
   - Nowa funkcja `process_csv_argument()` w `arg_parser.py` zajmuje się wczytywaniem, filtrowaniem oraz walidacją pliku CSV.
   - Uproszczenie głównej funkcji `main()` w `edumonitor.py`, co poprawia czytelność i modularność kodu.

## [Undefined] - 2024-09-26 no.1
### Nowości:
- **Dodano flagę --csv** umożliwiającą podanie pliku CSV z zewnętrznego źródła przez linię komend.
    - Program odczytuje podany plik CSV, konwertuje jego zawartość do formatu JSON i zapisuje wynikowy plik JSON w katalogu `input/`.
    - Plik JSON jest tworzony z nazwą w formacie `ukonczone_szkolenia_<timestamp>.json`, gdzie `<timestamp>` to aktualna data.
- **Dodano flagę --shell** umożliwiającą wyświetlanie wyników w konsoli w postaci tabeli.
    - Program wyświetla dane pracowników podzielone na grupy zawodowe (kadra zarządzająca, kadra kierownicza, pracownicy).
    - Tabela zawiera informacje o pracownikach z aktualnym, wygasającym i już wygasłym szkoleniem.

### Ulepszenia:
- **Integracja danych z URL**:
    - Program pobiera dane o pracownikach z zewnętrznej bazy danych (URL skonfigurowany w pliku `config.ini`), a następnie porównuje je z danymi z CSV.
    - Do wynikowego pliku JSON dodano pola `db_url`, `stanowisko` oraz `email`, które uzupełniają informacje o pracowniku na podstawie danych z URL.
- **Automatyczne uzupełnianie danych o pracownikach**:
    - Jeśli dany pracownik znajduje się w bazie danych (URL), do jego rekordu w JSON dodawane są pola `stanowisko` oraz `email`.
    - Dodano flagę `db_url = True/False`, informującą o tym, czy pracownik istnieje w bazie URL.
- **Zoptymalizowano zarządzanie danymi pracowników**:
    - Użycie klasy `Employee` do reprezentacji danych o pracownikach oraz porównywania ich z bazą URL.
    - Automatyczne sortowanie plików JSON według daty, co umożliwia zawsze wyświetlanie najnowszego pliku z wynikami.

### Poprawki:
- **Obsługa wyjątków**:
    - Poprawiono obsługę błędów przy ładowaniu danych z pliku JSON (np. błędne argumenty w funkcji `Employee`).
    - Dodano lepsze logowanie i obsługę błędów HTTP oraz wyjątków podczas pobierania danych z URL.
- **Poprawki związane z filtrowaniem pracowników**:
    - Ulepszono filtrację pracowników według grup zawodowych, uwzględniając pola `stanowisko` i `email` pobrane z bazy URL.

### Dokumentacja:
- Zaktualizowano dokumentację, aby odzwierciedlała nową funkcjonalność flag `--csv` oraz `--shell`.
- Opisano sposób działania programu, w tym proces odczytywania pliku CSV, konwersji do JSON oraz porównania danych z bazą URL.

## [v1.4.0] - 2024-09-25
### Nowości:
- **Dodano nowe zmienne konfiguracyjne** w pliku `config/config.ini`:
  - `HTML_LISTS`: Ścieżka do katalogu, w którym zapisywane są listy pracowników w formacie HTML.
  - `HTML_REPORTS`: Ścieżka do katalogu, w którym zapisywane są raporty o stanie wyszkolenia pracowników w formacie HTML.
- **Flaga --test-csv**: Wprowadzono flagę `--test-csv`, która pozwala na szybkie testowanie programu za pomocą przykładowego pliku CSV z katalogu `tests/test_files/`.
- **Testy jednostkowe**: Dodano kompleksowy zestaw testów jednostkowych obejmujących m.in.:
  - Wczytywanie danych z plików CSV (`CSVLoader`).
  - Porównywanie danych z pliku CSV z danymi z URL (`EmployeeManager`).
  - Generowanie raportów HTML (`HTMLReportGenerator`).
  - Wyświetlanie danych w konsoli (`TableDisplay`).
  - Pobieranie danych z URL i obsługę wyjątków (`fetch_employee_data_from_url`).

### Ulepszenia:
- **Modularność kodu**: Przebudowano strukturę projektu, rozdzielając logikę na osobne moduły, takie jak `csv_loader`, `employee_management`, `html_generator`, `table_display`. To umożliwia łatwiejsze zarządzanie kodem i jego przyszłą rozbudowę.
- **Poprawa logowania**: Dodano dedykowany moduł `logger_setup`, który konfiguruje logger na podstawie ustawień z pliku `config.ini`. Obsługiwane są różne poziomy logowania, a każde uruchomienie programu generuje plik logów z timestampem w nazwie.
- **Obsługa wyjątków**: Lepsze zarządzanie błędami i wyjątkami dzięki dekoratorowi `@log_exceptions`, który automatycznie loguje nieoczekiwane błędy występujące podczas działania programu.
- **Konfiguracja**: Wprowadzono klasę `ConfigLoader`, która ułatwia zarządzanie ustawieniami programu, takimi jak format dat, ścieżki do plików i ustawienia połączeń z bazą danych.

### Poprawki:
- **Poprawa loggera**: Upewniono się, że uchwyty loggera są prawidłowo zamykane, co eliminuje problemy z wyciekami zasobów (np. ostrzeżenia `ResourceWarning`).
- **Poprawa obsługi wyjątków**: W funkcji `fetch_employee_data_from_url` wprowadzono lepszą obsługę błędów związanych z połączeniami (np. `ConnectionError`), timeoutami oraz błędami HTTP (404, 500).
- **Elastyczne logowanie**: Dodano możliwość mockowania loggera w testach, co pozwala na wyciszenie zbędnych komunikatów i przyspieszenie testów.

### Dokumentacja:
- Zaktualizowano dokumentację, aby odzwierciedlała wszystkie zmiany wprowadzone w tej wersji, w tym nową strukturę modułów, konfigurację logowania oraz zarządzanie wyjątkami.
- Dodano szczegółowe informacje dotyczące konfiguracji programu, w tym zarządzanie katalogami dla plików HTML i CSV oraz formatowanie dat.

## [v1.3.2] - 2024-09-25
### Naprawy i zmiany:
- **Dodano nowe zmienne konfiguracyjne w pliku `config/config.ini`**:
  - `HTML_LISTS` dla katalogu, w którym zapisywane są listy pracowników w formacie HTML.
  - `HTML_REPORTS` dla katalogu, w którym zapisywane są raporty o stanie wyszkolenia pracowników w formacie HTML.
- **Aktualizacja modułu `HTMLReportGenerator`**:
  - Oddzielenie zapisywania list pracowników i raportów szkoleniowych do odpowiednich katalogów na podstawie zmiennych z pliku konfiguracyjnego.
  - Listy pracowników są teraz zapisywane w katalogu `output/lists/`, a raporty w katalogu `output/reports/`.
- **Aktualizacja testów**:
  - Zaktualizowano testy w pliku `tests/test_HTMLReportGenerator.py`, aby uwzględniały nowe ścieżki katalogów dla list i raportów.
  - Testy sprawdzają teraz poprawność generowania raportów i list HTML oraz poprawność ścieżek do plików.

## [1.3.1] - 2024-09-25
### Dodano:
- **Testy jednostkowe:**
    - Dodano kompleksowy zestaw testów jednostkowych dla modułów projektu, w tym:
        - Testy dla wczytywania danych z plików CSV (`CSVLoader`).
        - Testy dla porównywania danych z pliku CSV z danymi z URL (`EmployeeManager`).
        - Testy dla generowania raportów HTML (`HTMLReportGenerator`).
        - Testy dla wyświetlania danych w konsoli (`TableDisplay`).
        - Testy dla funkcji pobierającej dane pracowników z URL (`fetch_employee_data_from_url`), z obsługą błędów połączeń i statusów HTTP.
    - Testy obejmują mockowanie połączeń HTTP oraz loggera, co pozwala na szybsze i bardziej niezawodne testy.
- **Flaga --test-csv:**
    - Dodano flagę --test-csv, która umożliwia wczytywanie pliku testowego CSV bez potrzeby podawania pełnej ścieżki. Flaga używa domyślnie pliku testowego dane_testowe.csv z katalogu tests/test_files/.
    - Flaga ułatwia szybkie testowanie programu bez konieczności korzystania z rzeczywistych plików danych.

### Poprawiono:
- **Logger:**
    - Ulepszono obsługę loggera poprzez wprowadzenie dedykowanego modułu `logger_setup`, który konfiguruje logger w oparciu o plik konfiguracyjny `config.ini`.
    - Dodano możliwość mockowania loggera w testach, co pozwala na wyciszenie zbędnych komunikatów i przyspieszenie testów.
    - Umożliwiono resetowanie handlerów loggera, aby uniknąć powielania komunikatów podczas wielokrotnych uruchomień testów.
- **Obsługa wyjątków:**
    - Wprowadzono lepszą obsługę wyjątków w funkcji `fetch_employee_data_from_url`, która teraz loguje błędy związane z połączeniami (np. `ConnectionError`), timeoutami oraz błędami HTTP (404, 500).
    - Zastosowano dekorator `@log_exceptions`, który automatycznie loguje nieoczekiwane wyjątki podczas działania programu, co ułatwia diagnostykę problemów.

### Usunięto:
- **Niepotrzebne komunikaty logowania:**
    - Usunięto niepotrzebne komunikaty logowania, które były wywoływane w testach, eliminując problemy związane z zaśmiecaniem konsoli.

## [1.3.0] - 2024-09-24
### Usunięto:
- **Testy jednostkowe**: Usunięto wszystkie testy jednostkowe z projektu, w tym pliki testowe oraz wszelkie zależności i konfiguracje związane z testowaniem (np. unittest, pliki w katalogu tests/).
- **Sekcja TEST w pliku konfiguracyjnym**: Sekcja odpowiadająca za testowe ustawienia logowania (tj. LOG_LEVEL_CONSOLE, LOG_LEVEL_FILE, i LOG dla sekcji TEST) została usunięta z pliku config/config.ini.
- **Obsługa logowania dla testów**: Usunięto modyfikacje loggera związane z ustawieniami logowania tylko dla testów. Przywrócono domyślną konfigurację logowania dla programu.

### Zmieniono:
- **Przebudowa struktury projektu**: Wprowadzono znaczącą refaktoryzację kodu w celu zwiększenia czytelności, modularności oraz łatwości rozbudowy. Główne zmiany to:
    - **Modularność**: Rozbicie logiki na osobne moduły (m.in. `csv_loader`, `employee_management`, `html_generator`, `table_display`) w celu lepszego zarządzania kodem oraz ułatwienia rozszerzalności programu.
    - **Ulepszone logowanie**: Logger został przeniesiony do dedykowanego modułu `logger_setup`. Obsługuje teraz różne poziomy logowania (np. INFO, ERROR) z możliwością konfiguracji przez plik `config.ini`. Każde uruchomienie programu generuje plik logów z timestampem w nazwie.
    - **Lepsza obsługa wyjątków**: Dzięki wprowadzeniu dekoratora `@log_exceptions` możliwe jest automatyczne logowanie wyjątków, co ułatwia diagnostykę błędów i problemów występujących podczas działania programu.
    - **Elastyczność konfiguracji**: Dodano dedykowaną klasę `ConfigLoader`, która umożliwia łatwe zarządzanie konfiguracjami z pliku `config.ini`. Obsługuje m.in. format dat, ścieżki do plików logów oraz ustawienia dla połączeń z bazą danych.
- **Logger**: Przywrócono domyślne logowanie programu, usunięto logikę odpowiadającą za wyłączanie `StreamHandler` podczas testów. Logger nie ma już specjalnej konfiguracji związanej z testami.
- **Zamknięcie uchwytów loggera**: Wprowadzono poprawkę dotyczącą zamykania uchwytów loggera, aby uniknąć problemów z niezamkniętymi plikami logów i ostrzeżeniami dotyczącymi `ResourceWarning`.

### Naprawiono:
- **Ostrzeżenia ResourceWarning**: Naprawiono problem z ostrzeżeniami o niezamkniętych plikach logów. Upewniono się, że uchwyty loggera są prawidłowo zamykane, co eliminuje wycieki zasobów.

### Dokumentacja:
- Zaktualizowano dokumentację, usuwając wszelkie wzmianki o testach jednostkowych oraz sekcji TEST w pliku konfiguracyjnym.
- Uaktualniono instrukcje dotyczące konfiguracji programu, uwzględniając nowe możliwości zarządzania logowaniem oraz konfiguracją poprzez `config.ini`.

## [1.2.0] - 2024-09-23
### Dodano:
- **Generowanie raportów HTML**: Program umożliwia generowanie raportu o stanie wyszkolenia pracowników z podziałem na grupy zawodowe. Raport zawiera liczbę pracowników z ważnymi, wygasającymi oraz przeterminowanymi szkoleniami. Raport jest generowany z timestampem w nazwie pliku.
- **Aktualna data w raporcie**: W każdym wygenerowanym raporcie HTML wyświetlana jest aktualna data w formacie `Gdynia dnia <aktualna data>`.

## [1.1.0] - 2024-09-23
### Dodano:
- **Generowanie list HTML**: Program umożliwia generowanie list pracowników do przeszkolenia w formacie HTML, podzielonych na grupy zawodowe. Funkcja jest dostępna pod flagą `--lists-html`.

## [1.0.0] - 2024-09-23
### Dodano
- **Obsługa plików CSV**: Program wczytuje pliki CSV zawierające informacje o pracownikach i ich szkoleniach. Obsługiwane są pliki w formacie `cp1250`, a dane są przetwarzane na obiekty klasy `Employee`.
- **Konfiguracja daty**: Umożliwiono konfigurację formatu daty w pliku konfiguracyjnym `config.ini`, co pozwala na elastyczne zarządzanie formatem daty (np. `dd.mm.yyyy`).
- **Porównanie z bazą danych URL**: Program pobiera dane o pracownikach z zewnętrznego URL (definiowanego w pliku `config.ini`), a następnie porównuje je z danymi z pliku CSV. Dodano informacje o stanowisku i adresie email pracownika, jeśli istnieją w bazie danych.
- **Filtrowanie pracowników według grup zawodowych**: Pracownicy są klasyfikowani na grupy zawodowe, takie jak kadra zarządzająca, kadra kierownicza i pracownicy, co ułatwia wyświetlanie danych w formie tabeli.
- **Generowanie tabel w konsoli**: Program wyświetla dane w konsoli w formie tabeli, z podziałem na grupy zawodowe. Tabele wyświetlają informacje o pracownikach z aktualnym szkoleniem, wygasającym w ciągu 30 dni oraz już wygasłym.
- **Logowanie**: Każde uruchomienie programu generuje nowy plik logów z timestampem w nazwie, co umożliwia śledzenie działania programu. Logi zawierają informacje o przetwarzanych pracownikach, błędach i ostrzeżeniach, a także nazwę grupy zawodowej, z której pochodzą dane.
- **Konfiguracja logowania**: Możliwość niezależnej konfiguracji poziomu logowania dla konsoli oraz pliku logów poprzez zmienne `LOG_LEVEL_CONSOLE` i `LOG_LEVEL_FILE` w pliku konfiguracyjnym.
- **Obsługa wyjątków**: Program lepiej obsługuje błędy, takie jak brak połączenia z URL czy niepoprawne wiersze w pliku CSV, informując użytkownika o potencjalnych problemach.

### Dokumentacja
- Zaktualizowano dokumentację, aby odzwierciedlała wszystkie dodane funkcjonalności oraz szczegóły dotyczące konfiguracji programu.
