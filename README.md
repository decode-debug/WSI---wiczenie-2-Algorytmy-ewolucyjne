# WSI — Ćwiczenie 2: Algorytmy Ewolucyjne

Repozytorium zawiera implementację **algorytmu ewolucyjnego (EA)** rozwiązującego zadania optymalizacji numerycznej. Projekt został zrealizowany w ramach przedmiotu *Wprowadzenie do Sztucznej Inteligencji* (WSI).

---

## Opis projektu

Celem zadania jest znalezienie minimum globalnego zadanej funkcji celu przy użyciu mechanizmów inspirowanych biologiczną ewolucją. Algorytm operuje na populacji osobników, dążąc do znalezienia optymalnego rozwiązania w wielowymiarowej przestrzeni poszukiwań.

### Główne cechy implementacji:
* **Kodowanie:** Rzeczywistowartościowe (floating-point representation).
* **Populacja:** Stała liczba osobników ewoluująca w czasie.
* **Elitaryzm:** Mechanizm zachowujący najlepszego osobnika z poprzedniego pokolenia.

---

## Mechanizm działania

Proces ewolucyjny w obu algorytmach jest podobny:

1. **Inicjalizacja:** Generowanie losowej populacji początkowej w zadanym zakresie.
2. **Ocena:** Wyznaczenie wartości funkcji przystosowania dla każdego osobnika.
3. **Selekcja:** Wybór rodziców do reprodukcji (u mnie metoda turniejowa).
4. **Operatory genetyczne:**
    * **Krzyżowanie:** Wymiana informacji między wybranymi parami rodziców.
    * **Mutacja:** Losowa modyfikacja genów zapobiegająca utknięciu w optimach lokalnych.
5. **Sukcesja:** Zastąpienie starej populacji nowym pokoleniem.

---

## Technologie i wymagania

Projekt został napisany w języku **Python 3.x**.

### Wymagane biblioteki:
* **NumPy** – obliczenia wektorowe i macierzowe.
* **Matplotlib** – generowanie wykresów zbieżności i wizualizacja wyników.

---

### Sklonuj repozytorium:
```bash
git clone https://github.com/decode-debug/WSI---wiczenie-2-Algorytmy-ewolucyjne.git
```