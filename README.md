# VulnScanner
Mały projekt który skanuje zabezpieczenia komputera.

vuln_scanner.py to plik który:
- Skanuje zabezpieczenia przy pomocy Lynis,
- Spisuje użytkowników którzy włączyli skan,
- Posiada proste menu w terminalu,
- Zapisuje skan w pliku txt. oraz w bazie danych PostgreSQL

1. Aby wszystko działało poprawnie zainstaluj w terminalu potrzebne paczki:
[

sudo apt update

sudo apt install lynis postgresql postgresql-client python3-pip -y

pip3 install psycopg2-binary

]

Zobacz czy działa paczka z pythona:
python3 -c "import psycopg2; print('psycopg2 is working ✅')"

Jeżeli nie to wpisz to co poniżej w terminalu i powinno być w porządku:

sudo apt update

sudo apt install python3-psycopg2

(Jeżeli miałes błąd było to spowodowane przez zabezpieczenia pythona)

2.  Utwórz baze danych postgresql:

- sudo -u postgres psql

-- w psql
CREATE DATABASE vuln_scan;
\c vuln_scan
CREATE TABLE scan_results (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    scan_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    scan_output TEXT NOT NULL
);



Aktywując plik w terminalu nie musimy łączyć się z bazą danych gdyż skrypt robi to już za nas!.

Aktywuj skan za pomocą
[ sudo python3 vuln_scanner.py ]

Aby wyświetlić skan w bazie danych potrzeba:

1. Przełączyć się na użytkownika postgres ( sudo -u postgres psql )
2. Połączyć się do bazy danych vuln_scan ( \c vuln_scan ) 
3. Można zobaczyć egzystujące tabele (  \dt )
4. Aby zobaczyć kto i kiedy włączył skan trzeba wpisać w terminalu 
[ SELECT id, username, scan_time FROM scan_results ORDER BY scan_time DESC; ]

Możemy też alternatywnie użyć GUI do postgresql np. pgAdmin 4
