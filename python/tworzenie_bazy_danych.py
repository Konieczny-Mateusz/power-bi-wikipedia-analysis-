import sqlite3
import pandas as pd
from pathlib import Path

def build_sqlite_database():
    """
    Pobiera surowe dane o wyświetleniach (pliki TSV) z dedykowanego folderu
    w paczkach (chunks) i buduje zoptymalizowaną bazę danych SQLite.
    """
    # 1. Definicja ścieżek względnych
    # Wskazujemy bezpośrednio na ten jeden konkretny folder z rozpakowanymi danymi
    katalog_danych = Path("10-wyswietlenia_monthly_raw_data/Rozpakowane")
    sciezka_bazy = Path("baza_wikipedia.db")

    # Weryfikacja czy folder docelowy istnieje
    if not katalog_danych.exists():
        raise FileNotFoundError(f"Nie znaleziono folderu z danymi: {katalog_danych}")

    # Użycie zwykłego glob, ponieważ szukamy tylko w tym jednym, konkretnym folderze
    pliki = list(katalog_danych.glob("*.tsv.gz.tmp"))

    if not pliki:
        raise FileNotFoundError(f"Nie znaleziono plików *.tsv.gz.tmp w folderze {katalog_danych}.")

    print(f"Znaleziono {len(pliki)} plików. Rozpoczynam budowę bazy '{sciezka_bazy.name}'...")

    # 2. Tworzenie bazy i bezpieczne ładowanie danych
    with sqlite3.connect(sciezka_bazy) as conn:
        for plik in pliki:
            print(f"Przetwarzanie pliku: {plik.name}")

            # Wyciąganie daty z nazwy pliku (np. "2016-01.tsv.gz.tmp" -> "2016-01-01")
            rok_miesiac = plik.name[:7]
            data_format = f"{rok_miesiac}-01"

            # Ładowanie danych w mniejszych paczkach (optymalizacja RAM)
            chunks = pd.read_csv(plik, sep='\t', chunksize=100000)

            for chunk in chunks:
                chunk['date'] = data_format
                chunk.to_sql('wyswietlenia_monthly', conn, if_exists='append', index=False)

        print("Załadowano wszystkie dane! Rozpoczynam tworzenie indeksów SQL...")

        # 3. Tworzenie indeksów ułatwiających szybkie zapytania
        cursor = conn.cursor()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_page_id ON wyswietlenia_monthly (page_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_date ON wyswietlenia_monthly (date);")
        conn.commit()

    print("Baza danych SQL została pomyślnie utworzona i zindeksowana!")

if __name__ == "__main__":
    build_sqlite_database()