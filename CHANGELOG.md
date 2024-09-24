# CHANGELOG

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
