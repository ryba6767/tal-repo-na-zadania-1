# Python — programowanie do matury rozszerzonej

Kurs obejmuje 12 kart pracy dla uczniów znających podstawy Pythona. Początkowe lekcje są powtórzeniem, a kolejne rozwijają umiejętności potrzebne w zadaniach maturalnych. Prowadzący: por. Jakub GRĄTKIEWICZ · jakub.gratkiewicz@wat.edu.pl.

Zacznij od [organizacji i zasad zajęć](00_organizacja_i_zasady_zajec.md). Nie ma sprawdzianów: oceniane są zadania, odpowiedzi dotyczące zadań, kartkówki i aktywność. Każda kartkówka poprzedza część dydaktyczną i trwa 10 minut. Karty nie zawierają szacunków czasu wykonania ćwiczeń.

## Lekcje

Każda lekcja ma osobny folder, własny notatnik `karta_pracy.ipynb` i potrzebne dane obok niego. Liczba zadań zależy od karty. Karta 05 służy samodzielnemu sprawdzeniu wiadomości: zawiera trzy podpunkty zadania maturalnego 3.1–3.3 i puste komórki na kod, bez dodatkowych ćwiczeń ani pracy domowej. W pozostałych kartach zadania do samodzielnego wykonania są wskazane w osobnej sekcji. Pytania do powtórzenia w kartach nie są zestawami kartkówek.

| Nr | Karta pracy | Zakres |
|---:|---|---|
| 1 | [Powtórzenie Pythona: Jupyter, obliczenia i sterowanie](01_jupyter_i_podstawy_pythona/karta_pracy.ipynb) | Typy, operatory, warunki, pętle i stan jądra |
| 2 | [Powtórzenie: napisy, kolekcje i funkcje](02_kolekcje_napisy_i_funkcje/karta_pracy.ipynb) | Kopie, palindromy, słowniki, kontrakty i testy |
| 3 | [Powtórzenie: samodzielna praca z plikami](03_pliki_tekstowe_i_wyniki/karta_pracy.ipynb) | Otwieranie, odczyt, konwersja, kontrola i zapis |
| 4 | [Cyfry, systemy liczbowe i NWD](04_cyfry_skroty_i_nwd/karta_pracy.ipynb) | Horner, skrót, Euklides i własny odczyt danych |
| 5 | [Matura 2024 — Nieparzysty skrót](05_matura_2024_zadanie_3_nieparzysty_skrot/karta_pracy.ipynb) | Zadanie 3.1–3.3 od pliku do odpowiedzi |
| 6 | [Sortowanie, liczności i czynniki](06_sortowanie_zliczanie_i_czynniki/karta_pracy.ipynb) | Duplikaty, dzielniki i zapas czynników |
| 7 | [Sumy prefiksowe i fragmenty](07_sumy_prefiksowe_i_fragmenty/karta_pracy.ipynb) | Granice, złożoność, średnie i remisy |
| 8 | [Matura 2024 — Liczby](08_matura_2024_zadanie_4_liczby/karta_pracy.ipynb) | Zadanie 4.1–4.4, dane przykładowe i pełne |
| 9 | [Napisy, system trójkowy i siatki](09_napisy_system_trojkowy_i_siatki/karta_pracy.ipynb) | Systemy 2/3/8/16, palindromy i bloki 3×3 |
| 10 | [Matura 2025 — Zapis symboliczny](10_matura_2025_zadanie_2_zapis_symboliczny/karta_pracy.ipynb) | Zadanie 2.1–2.4 i samodzielny zapis wyników |
| 11 | [Wektory, punkty i geometria](11_nwd_ruch_i_geometria/karta_pracy.ipynb) | Trasa z pliku, NWD, wnętrze i środek odcinka |
| 12 | [Matura 2025 — Dron](12_matura_2025_zadanie_3_dron/karta_pracy.ipynb) | Zadanie 3.1–3.2 i obrona całego rozwiązania |

Oryginalne zadania CKE są wyraźnie oznaczone rokiem, numerem i symbolem arkusza. Na kartach 5, 8, 10 i 12 PDF odpowiedniego arkusza znajduje się także w folderze lekcji. Kurs obejmuje cztery zadania programistyczne z arkuszy 2024 i 2025; nie obejmuje ich części bazodanowej i arkusza kalkulacyjnego.

## Jak pracować

1. Pobierz cały kurs albo paczkę wybranej lekcji i rozpakuj folder. Nie przenoś samego notatnika bez jego danych.
2. Otwórz `karta_pracy.ipynb` w folderze lekcji. Jądro Pythona powinno pracować w tym folderze, aby zwykłe nazwy plików wskazywały właściwe dane.
3. Jeśli potrzebujesz środowiska, utwórz je przez `python3 -m venv .venv`, aktywuj i zainstaluj `jupyterlab` poleceniem `python -m pip install jupyterlab`. W Windows polecenie Pythona może mieć nazwę `py`.
4. Uruchom `jupyter lab` i otwórz kartę z odpowiedniego katalogu. Każdą kartę wykonuj w osobnym, świeżym jądrze.
5. Sam napisz kod w komórkach roboczych. W zadaniach plikowych obejmuje to **otwarcie pliku, odczyt, konwersję, obliczenia i zapis odpowiedzi**. Nie ma globalnego loadera ani wstępnie wczytanych danych zadaniowych.
6. Odkomentuj podane testy po napisaniu własnego rozwiązania i dodaj testy przypadków brzegowych. Testy w pustej karcie są komentarzami; wykonanie takiej komórki nie potwierdza rozwiązania.
7. Zapisuj pliki wynikowe obok notatnika, pod nazwami wymaganymi w poleceniach. Nie nadpisuj plików wejściowych. Przed oddaniem zrestartuj jądro, uruchom cały własny kod i zapisz notatnik.

Podane małe przykłady pokazują narzędzia; nie wczytują plików zadaniowych za ucznia. W lekcji 3 demonstracja otwiera osobny `demo-liczby.txt`, a uczeń sam pracuje na pozostałych plikach. W lekcjach 1–2 nie są potrzebne pliki zewnętrzne.

## Prezentacja i materiały prowadzącego

Gotowa prezentacja jest w sąsiednim folderze `prezentacja-python`. Zawiera lekcję 0 z zasadami oraz lekcje 1–12. Nawigacja: **←/→ między lekcjami, ↑/↓ między elementami**. Karty, slajdy, druk i paczki pobierane ze strony nie zawierają rozwiązań zadań ani zestawów kartkówek.

W pełnym lokalnym projekcie folder `materialy-prowadzacego` zawiera:

- `kartkowki_01-12.md` — 12 zestawów po trzy pytania oraz klucz odpowiedzi w jednym pliku;
- 12 katalogów z notatnikami `rozwiazania.ipynb`, danymi i aktywnymi testami.

Materiały prowadzącego nie są dołączane do publicznych paczek. **Na GitHub Pages publikuj wyłącznie folder `prezentacja-python`, nie cały lokalny projekt.** Paczka ucznia nie zawiera kluczy ani narzędzi do regenerowania kursu.

## Aktualizacja pełnego projektu

Treść źródłowa jest w `scripts/content`, teksty CKE w `tresci-maturalne`, a oryginalne dane do kopiowania w `dane`. Źródłowe arkusze i wcześniejsze kody C++ zachowano lokalnie w `materialy-zrodlowe`; kody C++ nie są publikowane.

Po zmianie treści uruchom z katalogu pełnego kursu:

```text
python3 scripts/build-course.py
```

Generator odświeża foldery lekcji, materiały prowadzącego, slajdy i paczki ucznia. Nie edytuj ręcznie wygenerowanych kopii w prezentacji. Zachowaj własne prace uczniów w oddzielnych kopiach — regenerowanie nadpisuje szablony kart.

Weryfikacja wymaga `nbformat`, `nbclient` i `ipykernel`:

```text
python -m pip install nbformat nbclient ipykernel
python scripts/verify-course.py
```

Testy sprawdzają osobne katalogi i jądra, algorytmy, pliki wynikowe oraz brak kluczy w publicznych plikach. Pracują w katalogach tymczasowych, nie zmieniając prac uczniów.
