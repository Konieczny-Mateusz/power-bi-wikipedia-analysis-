import sqlite3
import pandas as pd
from pathlib import Path


def extract_and_filter_data():
    """
    Ekstrakcja danych z bazy SQLite na podstawie słownika pożądanych artykułów
    i eksport do pliku analitycznego dla środowiska Power BI.
    """

    # 1. Definicja ścieżek względnych (niezależnych od systemu i użytkownika)
    sciezka_slownik = Path("moj_slownik.csv")
    sciezka_bazy = Path("baza_wikipedia.db")
    sciezka_wyjscia = Path("gotowe_wyswietlenia_dla_powerbi.csv")

    # Weryfikacja czy pliki wejściowe istnieją
    if not sciezka_slownik.exists():
        raise FileNotFoundError(f"Brak pliku słownika: {sciezka_slownik}")
    if not sciezka_bazy.exists():
        raise FileNotFoundError(f"Brak pliku bazy danych: {sciezka_bazy}")

    # 2. Wczytanie Słownika
    print("Wczytywanie identyfikatorów ze słownika...")
    slownik = pd.read_csv(sciezka_slownik, sep=';')

    # Wyciągamy unikalne numery page_id do formatu zrozumiałego dla SQL
    wybrane_ids = tuple(int(x) for x in slownik['page_id'].dropna().unique())
    print(f"Znaleziono {len(wybrane_ids)} unikalnych artykułów. Odpytuję bazę SQL...")

    # 3. Połączenie z bazą i wyciągnięcie tylko pasujących wierszy
    # Użycie bloku 'with' automatycznie zarządza zamknięciem połączenia
    with sqlite3.connect(sciezka_bazy) as conn:
        zapytanie = f"SELECT * FROM wyswietlenia_monthly WHERE page_id IN {wybrane_ids}"
        df_wynik = pd.read_sql(zapytanie, conn)

    # 4. Zapisanie odchudzonego pliku dla Power BI
    print("Zapisywanie gotowego pliku CSV...")
    df_wynik.to_csv(sciezka_wyjscia, index=False)
    print(f"Sukces! Plik '{sciezka_wyjscia.name}' jest gotowy do załadowania.")


if __name__ == "__main__":
    extract_and_filter_data()