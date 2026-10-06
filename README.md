# Analiza Wikipedii: Popularność vs. Zaangażowanie Społeczności

Projekt analityczny wykonany w ramach inicjatywy **#BI_NGO**, poświęcony analizie popularności artykułów Wikipedii oraz aktywności społeczności związanej z ich edycją.

## Cel projektu

Głównym celem analizy było sprawdzenie, czy artykuły Wikipedii, które cieszą się największą popularnością wśród czytelników, są jednocześnie artykułami, które są najczęściej edytowane przez społeczność.

Analiza koncentruje się na dwóch wymiarach:

- **popularność** - liczba wyświetleń artykułów,
- **zaangażowanie społeczności** - liczba edycji artykułów.

Na tej podstawie przeanalizowano trendy w czasie, rankingi, zależność pomiędzy wyświetleniami i edycjami oraz grupy artykułów o podobnej charakterystyce.

## Zakres analizy

- okres: **2016-2026**,
- dane w ujęciu miesięcznym,
- ponad **33 tys. unikalnych identyfikatorów `page_id`** w połączonym i zduplikowanym słowniku artykułów,
- początkowa baza danych: **207 122 073 rekordy**,
- zbiór po filtrowaniu: **3 601 067 rekordów**,
- analiza danych dotyczących wyświetleń i edycji artykułów.

Filtrowanie pozwoliło ograniczyć zbiór do około **1,74%** pierwotnej liczby rekordów.

## Źródła danych

W projekcie wykorzystano dane udostępnione w ramach inicjatywy #BI_NGO związanej z analizą danych Wikipedii.

Do przygotowania zakresu analizowanych artykułów wykorzystano dwa źródła:

- `5-top_1000_artykulow_monthly`
- `7-top_100_najczesciej_edytowanych_artykulow_monthly`

Dane źródłowe obejmowały łącznie **126 plików miesięcznych**. Surowe dane nie są przechowywane w tym repozytorium.

## Przygotowanie danych

Ze względu na dużą liczbę rekordów dane zostały przygotowane etapami.

### 1. Budowa bazy SQLite

126 plików miesięcznych zostało przetworzonych za pomocą **Python + Pandas** i zapisanych w bazie **SQLite**.

Podczas importu:

- dane były wczytywane partiami (`chunksize`), aby ograniczyć zużycie pamięci,
- do rekordów dodawana była data miesiąca,
- dane trafiały do tabeli `wyswietlenia_monthly`,
- utworzono indeksy na `page_id` oraz `date`.

W rezultacie powstała baza zawierająca:

**207 122 073 rekordy.**

### 2. Utworzenie słownika artykułów

W Power Query utworzono dwa odwołania do źródeł:

- `Baza_5` - dataset `5-top_1000_artykulow_monthly`,
- `Baza_7` - dataset `7-top_100_najczesciej_edytowanych_artykulow_monthly`.

Z obu tabel pozostawiono wyłącznie:

- `page_id`,
- `title`.

Następnie tabele zostały połączone operacją **Append Queries** w tabelę `Slownik_Artykulow`.

Po połączeniu usunięto duplikaty według `page_id`, uzyskując unikalny zbiór identyfikatorów artykułów.

Słownik został następnie wyeksportowany do pliku CSV i wykorzystany jako lista identyfikatorów do filtrowania dużej bazy SQLite.

### 3. Filtrowanie danych za pomocą SQL

Za pomocą skryptu Python połączono się z bazą SQLite i pobrano z tabeli `wyswietlenia_monthly` wyłącznie rekordy, których `page_id` znajdował się w słowniku.

Wynikiem tego procesu jest plik:

`gotowe_wyswietlenia_dla_powerbi.csv`

zawierający:

- `page_id`,
- `views`,
- `date`.

Po filtrowaniu pozostało:

**3 601 067 rekordów**, czyli około **1,74%** początkowego zbioru.

### 4. Model danych

Raport wykorzystuje model gwiazdy, oparty na dwóch głównych wymiarach:

- `Kalendarz` - obsługa analizy w czasie,
- `Slownik_Artykulow` - identyfikacja i segmentacja analizowanych artykułów.

W modelu znajdują się również tabele zawierające dane dotyczące wyświetleń i edycji artykułów. Relacje pomiędzy tabelami umożliwiają wspólną analizę popularności oraz aktywności społeczności.

## Proces przygotowania danych

```text
126 plików źródłowych
        │
        ▼
Python + Pandas
        │
        ▼
SQLite
207 122 073 rekordy
        │
        │
        ├───────────────┐
        │               │
        ▼               ▼
 Dataset 5          Dataset 7
        │               │
        └───────┬───────┘
                ▼
       Power Query
      Slownik_Artykulow
                │
                ▼
       unikalne page_id
                │
                ▼
        Python + SQL
                │
                ▼
3 601 067 rekordów
                │
                ▼
            Power BI
```

## Analiza w Power BI

Raport został podzielony na kilka głównych obszarów:

### Executive Summary

Podsumowanie najważniejszych informacji dotyczących popularności i aktywności społeczności.

### Perspektywa czytelnika

Analiza z perspektywy czytelnika:

- liczba wyświetleń,
- trendy w czasie,
- rankingi popularności,
- zmiany miesiąc do miesiąca.

### Praca społeczności

Analiza aktywności społeczności:

- liczba edycji,
- trendy liczby edycji,
- rankingi najczęściej edytowanych artykułów,
- zmiany aktywności w czasie.

### Segmentacja

Segmentacja artykułów na podstawie ich charakterystyki.

W projekcie wykorzystano **K-means clustering**, aby pogrupować artykuły o podobnych wartościach wyświetleń i edycji.

Dodatkowo przeanalizowano zależność pomiędzy popularnością artykułów a aktywnością społeczności. Zależność ta jest **dodatnia, ale nieliniowa**, dlatego do analizy relacji wykorzystano również skalę logarytmiczną.

## Technologie

- **Power BI**
- **DAX**
- **Power Query**
- **Python**
- **Pandas**
- **SQL**
- **SQLite**
- **K-means clustering**
- **Data visualization**
- **Data preparation / ETL**
- **Time-based analysis**
- **Model gwiazdy**

## Własny motyw Power BI

Raport wykorzystuje własny motyw przygotowany z myślą o wymaganiach wizualnych projektu Wikimedia.

Motyw:

`Wikimedia Creative Palette Theme`

zawiera m.in. dedykowaną paletę kolorów oraz konfigurację typografii dla elementów raportu.

Plik motywu znajduje się w:

`power-bi/motyw.json`

## Najważniejsze elementy projektu

Projekt pokazuje pełny proces przygotowania i analizy dużego zbioru danych:

1. import wielu plików źródłowych,
2. przetwarzanie danych za pomocą Pandas,
3. budowa bazy SQLite,
4. utworzenie słownika artykułów w Power Query,
5. filtrowanie danych za pomocą SQL,
6. przygotowanie zbioru do Power BI,
7. modelowanie danych, tworzenie relacji i miar DAX,
8. analiza trendów i rankingów,
9. analiza zależności wyświetlenia-edycje,
10. segmentacja artykułów za pomocą K-means,
11. przygotowanie interaktywnego raportu Power BI.

## Struktura repozytorium

```text
power-bi-wikipedia-analysis/
│
├── README.md
│
├── power-bi/
│   ├── Analiza_Wikipedia_Mateusz_Konieczny.pbix
│   └── motyw.json
│
├── python/
│   ├── build_wikipedia_database.py
│   └── extract_selected_pages.py
│
├── data/
│   └── gotowe_wyswietlenia_dla_powerbi.csv
│
└── screenshots/
    ├── executive-summary.png
    ├── reader-perspective.png
    ├── community-perspective.png
    ├── segmentation.png
    └── model_gwiazdy.png
```

## Pliki, których nie umieszczono w repozytorium

Ze względu na rozmiar nie są przechowywane tutaj:

- oryginalne 126 plików źródłowych,
- baza `baza_wikipedia.db` o rozmiarze ok. 11,2 GB.

Plik `gotowe_wyswietlenia_dla_powerbi.csv` jest wynikiem przetworzenia i filtrowania danych, a nie surowym źródłem.

## Źródła

- #BI_NGO - inicjatywa związana z analizą danych Wikipedii
- Wikimedia / Wikipedia - dane wykorzystane w projekcie
- źródła danych udostępnione przez organizatorów projektu

## Autor

**Mateusz Konieczny**

Projekt portfolio w obszarze analizy danych i Business Intelligence.
