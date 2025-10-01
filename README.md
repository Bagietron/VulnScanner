VulnScanner
Mały projekt, który skanuje zabezpieczenia komputera z systemem Linux.

Plik vuln_scanner.py:
- wykonuje skan bezpieczeństwa za pomocą narzędzia Lynis,
- zapisuje użytkownika, który uruchomił skan,
- posiada proste menu w terminalu,
- zapisuje wynik skanu w pliku .txt oraz w bazie danych PostgreSQL.

1) Instalacja potrzebnych pakietów

    W terminalu uruchom:

    sudo apt update
    sudo apt install lynis postgresql postgresql-client python3-pip -y
    pip3 install psycopg2-binary

    Sprawdź, czy działa adapter do PostgreSQL:

    python3 -c "import psycopg2; print('psycopg2 is working ✅')"

    Jeżeli pojawi się błąd, doinstaluj systemowy pakiet:

    sudo apt update
    sudo apt install python3-psycopg2

    (Uwaga: błąd może wynikać z mechanizmu ochrony pakietów w Pythonie na Ubuntu/Debian — w takim przypadku instalacja przez apt jest bezpieczniejsza.)

2) Konfiguracja bazy danych PostgreSQL

	1. Wejdź do PostgreSQL:
	   sudo -u postgres psql

	2. Utwórz bazę danych:
	   CREATE DATABASE vuln_scan;

	3. Przełącz się do niej:
	   \c vuln_scan

	4. Utwórz tabelę na wyniki skanów:
	   CREATE TABLE scan_results (
	       id SERIAL PRIMARY KEY,
	       username TEXT NOT NULL,
	       scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	       scan_output TEXT NOT NULL
	   );

	5. Wyjdź z PostgreSQL:
	   \q

3) Uruchamianie skanera

	W terminalu:
	sudo python3 vuln_scanner.py

	Skrypt sam łączy się z bazą danych i zapisuje wyniki — nie trzeba ręcznie łączyć się z bazą.

4) Sprawdzanie wyników w bazie danych

	1. Zaloguj się do PostgreSQL:
	   sudo -u postgres psql
	
	2. Połącz się z bazą:
	   \c vuln_scan

	3. Zobacz istniejące tabele:
	   \dt

	4. Wyświetl historię skanów:
	   SELECT id, username, scan_time FROM scan_results ORDER BY scan_time DESC;

	5. Alternatywa – GUI

	Wyniki można także obejrzeć w narzędziu graficznym pgAdmin 4, które ułatwia zarządzanie bazą danych.

	5. Lokalizacje plików Lynis (przydatne)

	- /var/log/lynis.log — główny log Lynis (detaliczne informacje o teście)
	- /var/log/lynis-report.dat — raport w formacie danych Lynis
	- Pliki .txt generowane przez skrypt mogą być zapisywane w katalogu, z którego uruchamiasz skrypt (np. /home/użytkownik/)

	Jeżeli chcesz odczytać plik tekstowy z raportem:
	- Polecenie w terminalu:
	  less /ścieżka/do/pliku.txt
	  lub
	  cat /ścieżka/do/pliku.txt

	6. Dobre praktyki i uwagi

	- Nie używaj stałych haseł w skryptach publicznych — rozważ użycie zmiennych środowiskowych lub pliku konfiguracyjnego (np. .env) wyłączonego z kontroli wersji.
	- Dla środowisk produkcyjnych preferuj instalację python3-psycopg2 przez apt zamiast psycopg2-binary przez pip.
	- Regularnie aktualizuj system i pakiety: sudo apt update && sudo apt upgrade
	- Przechowuj kopie zapasowe bazy danych, jeśli potrzebujesz historii skanów długoterminowo.

	7. Szybkie przypomnienie komend (podsumowanie)

	Instalacja:
	sudo apt update
	sudo apt install lynis postgresql postgresql-client python3-pip -y
	pip3 install psycopg2-binary
	-- lub w razie problemów:
	sudo apt install python3-psycopg2

	Tworzenie bazy i tabeli (w psql):
	CREATE DATABASE vuln_scan;
	\c vuln_scan
	CREATE TABLE scan_results (
	    id SERIAL PRIMARY KEY,
	    username TEXT NOT NULL,
	    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	    scan_output TEXT NOT NULL
	);

	Uruchomienie skryptu:
	sudo python3 vuln_scanner.py

	Sprawdzenie wyników:
	sudo -u postgres psql
	\c vuln_scan
	SELECT id, username, scan_time FROM scan_results ORDER BY scan_time DESC;
