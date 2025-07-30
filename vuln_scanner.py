import subprocess
import getpass
import psycopg2
from datetime import datetime
import os

# PostgreSQL config
DB_CONFIG = {
    "dbname": "vuln_scan",
    "user": "scanner_user",  # or "postgres" if using default
    "password": "strongpassword",  # Change this to your DB password
    "host": "localhost",
    "port": "5432"
}

def run_lynis_scan():
    print("\n[🔍] Skanowanie...\n")
    try:
        result = subprocess.run(
            ["sudo", "lynis", "audit", "system", "--quick"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"Error! : {e.stderr}"

def save_to_postgres(username, scan_output):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO scan_results (username, scan_output) VALUES (%s, %s);",
        (username, scan_output)
    )
    conn.commit()
    cur.close()
    conn.close()

def save_to_file(username, scan_output):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{username}_scan_{timestamp}.txt"
    filepath = os.path.join(os.getcwd(), filename)

    with open(filepath, "w") as file:
        file.write(scan_output)

    print(f"[📁] Skanowanie zapisane do: {filepath}")

def view_last_scan(username):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("""
        SELECT scan_time, scan_output 
        FROM scan_results 
        WHERE username = %s 
        ORDER BY scan_time DESC 
        LIMIT 1;
    """, (username,))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        scan_time, scan_output = result
        print(f"\n🕒 Ostatnie skanowanie rozpoczete przez {username} o {scan_time}:\n")
        print(scan_output[:1000] + "...")  # Truncate for readability
    else:
        print(f"\n⚠️ Brak skanow dla uzytkownika {username}.\n")

def main():
    username = getpass.getuser()

    while True:
        print("\n=== Menu skanowania zabezpieczen ===")
        print("1. Nowy skan")
        print("2. Wyswietl poprzednie skanowanie")
        print("3. Wyjdz z programu")
        choice = input("Wpisz swoj wybor: ")

        if choice == "1":
            output = run_lynis_scan()
            save_to_postgres(username, output)
            save_to_file(username, output)
            print("\n✅ Skanowanie zakonczone oraz zapisane!.\n")

        elif choice == "2":
            view_last_scan(username)

        elif choice == "3":
            print("\n👋 Zakonczenie programu.\n")
            break

        else:
            print("\n❌ Niepoprawny wybor... Wybierz 1,2 albo 3.\n")

if __name__ == "__main__":
    main()
