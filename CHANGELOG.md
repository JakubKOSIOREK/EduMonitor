# CHANGELOG

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
