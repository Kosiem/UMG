# Laboratorium 2 — rozkład QR i rozwiązywanie układu równań

Program rozkłada macierz współczynników układu równań liniowych na macierz ortogonalną i macierz trójkątną górną, a następnie wykorzystuje ten rozkład do obliczenia rozwiązania.

Rozwiązywany układ ma postać:

$$
Ax=b
$$

gdzie $A$ jest macierzą współczynników, $x$ — wektorem niewiadomych, a $b$ — wektorem prawej strony.

## Czym jest rozkład QR?

Rozkład QR polega na zapisaniu macierzy $A$ jako iloczynu:

$$
A=QR
$$

- \(Q\) jest macierzą ortogonalną — jej kolumny są wzajemnie prostopadłe i mają długość 1, czyli \(Q^TQ=I\).
- \(R\) jest macierzą trójkątną górną — elementy pod jej główną przekątną są zerami.

W programie rozkład jest oparty na metodzie Grama-Schmidta. Dla każdej kolumny macierzy $A$ obliczane są jej projekcje na wcześniej wyznaczone kolumny macierzy $Q$. Współczynniki projekcji trafiają do macierzy $R$, a pozostały wektor jest normalizowany i zapisywany jako kolejna kolumna $Q$. Dzięki temu kolejne kolumny $Q$ powinny być ortonormalne.

## Jak z rozkładu otrzymuje się rozwiązanie?

Po podstawieniu $A=QR$ do układu $Ax=b$ dostajemy:

$$
QRx=b
$$

Mnożymy obie strony przez \(Q^T\). Ponieważ \(Q^TQ=I\), otrzymujemy:

$$
Rx=Q^Tb
$$

Pozostaje rozwiązać układ z macierzą trójkątną górną. Niewiadome oblicza się od ostatniej do pierwszej, czyli przez **podstawianie wstecz**. Sam rozkład ma złożoność około $O(n^3)$, a podstawianie wstecz — $O(n^2)$.

## Co robi program?

Plik `main.py` wykonuje następujące kroki:

1. Wczytuje rozmiar macierzy, macierz $A$ i wektor $b$ z `test.txt`.
2. Wyznacza macierze $Q$ i $R$ w funkcji `qr_decomposition`.
3. Oblicza \(Q^Tb\), a następnie rozwiązuje układ \(Rx=Q^Tb\) w funkcji `solve_qr`.
4. Wyświetla dane wejściowe, macierze rozkładu i obliczony wektor \(x\).
5. Zgłasza komunikat, gdy podczas obliczeń napotka element diagonalny macierzy $R$ bliski zeru.

Funkcja `load_matrix_from_file` odpowiada za odczyt danych. Stała `EPS = 1e-12` jest używana jako próg do wykrywania elementów uznanych za numerycznie bliskie zeru. Do obliczeń macierzowych i norm wektorów program wykorzystuje bibliotekę NumPy.

## Format pliku wejściowego

`test.txt` powinien zawierać:

1. W pierwszym wierszu rozmiar $n$.
2. W kolejnych $n$ wierszach — po $n$ liczb opisujących macierz $A$.
3. W ostatnim wierszu — $n$ liczb wektora $b$.

Przykładowa zawartość pliku:

```text
4
2 7 6 4
3 8 0 5
6 7 8 1
0 2 4 3
45 34 47 26
```

Wiersze powinny zawierać liczby rozdzielone spacjami. Plik jest otwierany pod ścieżką względną `test.txt`, więc program należy uruchamiać z katalogu `MetodyNumeryczne/Lab2` albo zapewnić ten plik w bieżącym katalogu roboczym.

## Uruchomienie

Wymagany jest Python oraz biblioteka NumPy. W razie potrzeby można ją zainstalować poleceniem:

```bash
python -m pip install numpy
```

Następnie, z katalogu `MetodyNumeryczne/Lab2`, uruchom:

```bash
python main.py
```

## Uwaga dotycząca bieżącej implementacji

W `qr_decomposition` wektor roboczy jest za każdym razem obliczany od pierwotnej kolumny macierzy, zamiast kolejno odejmować od niego wszystkie projekcje. W metodzie Grama-Schmidta wektor powinien być aktualizowany po każdej projekcji. W obecnej postaci wyznaczone kolumny $Q$ mogą nie być ortogonalne, dlatego obliczone rozwiązanie może być niepoprawne.
