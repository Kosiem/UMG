# Laboratorium 1 — rozkład LU i rozwiązywanie układu równań

Program rozkłada macierz współczynników układu równań liniowych na macierze trójkątne, a następnie wykorzystuje ten rozkład do obliczenia rozwiązania.

Rozwiązywany układ ma postać:

$$
Ax=b
$$

gdzie $A$ jest macierzą współczynników, $x$ — wektorem niewiadomych, a $b$ — wektorem prawej strony.

## Czym jest rozkład LU?

Rozkład LU polega na zapisaniu macierzy $A$ jako iloczynu dwóch macierzy:

$$
A=LU
$$

- \(L\) (*lower triangular*) jest macierzą trójkątną dolną — elementy nad jej przekątną są zerami.
- \(U\) (*upper triangular*) jest macierzą trójkątną górną — elementy pod jej przekątną są zerami.

W tym programie przekątna macierzy $L$ składa się z jedynek. Macierz $U$ powstaje bezpośrednio z macierzy $A$ w trakcie eliminacji Gaussa:

1. Na początku \(U\) jest kopią \(A\) (po ewentualnych zamianach wierszy odpowiada macierzy \(PA\)).
2. W kolumnie \(k\) dla każdego wiersza \(i>k\) obliczany jest mnożnik
   $$
   l_{ik}=\frac{u_{ik}}{u_{kk}}
   $$
3. Od wiersza \(i\) odejmuje się \(l_{ik}\)-krotność wiersza \(k\):
   $$
   \text{wiersz}_i \leftarrow \text{wiersz}_i-l_{ik}\,\text{wiersz}_k
   $$
   W efekcie element $u_{ik}$ pod pivotem staje się zerem. Mnożnik $l_{ik}$ jest zapisywany w pozycji $L_{ik}$, a zmieniony wiersz pozostaje w $U$.

Po wykonaniu tych operacji w każdej kolumnie wszystkie elementy pod główną przekątną w $U$ są równe zeru. Wartości na przekątnej i nad nią są wynikami kolejnych odejmowań — to właśnie one tworzą górnotrójkątną macierz $U$. Innymi słowy, $L$ przechowuje mnożniki użyte do eliminacji, a $U$ — macierz, która pozostaje po tej eliminacji.

W praktyce rozkład często zapisuje się z macierzą permutacji:

$$
PA=LU
$$

Macierz $P$ opisuje zamiany wierszy wykonywane w celu wyboru elementu głównego (pivotu). Mnożenie macierzy z lewej strony przez $P$ zmienia kolejność jej wierszy. Na przykład

$$
P=\begin{bmatrix}0&1\\1&0\end{bmatrix}
$$

zamienia pierwszy i drugi wiersz macierzy:

$$
P\begin{bmatrix}a&b\\c&d\end{bmatrix}
=\begin{bmatrix}c&d\\a&b\end{bmatrix}
$$

Sama zamiana kolejności równań nie zmienia ich rozwiązania, ale pozwala wybrać lepszy pivot — najlepiej niezerowy i możliwie duży co do wartości bezwzględnej — dzięki czemu można uniknąć dzielenia przez zero i ograniczyć błędy numeryczne. Ponieważ zmieniamy kolejność wierszy po lewej stronie równania, te same zamiany trzeba wykonać po prawej stronie: $PAx=Pb$. Stąd $PA=LU$, a podczas rozwiązywania układu używamy $Pb$.

## Jak z rozkładu otrzymuje się rozwiązanie?

Po podstawieniu $PA=LU$ do układu $Ax=b$ dostajemy:

$$
LUx=Pb
$$

Wprowadzamy pomocniczy wektor \(y\) i rozwiązujemy dwa prostsze układy:

1. **Podstawianie w przód:** $Ly=Pb$. Ponieważ $L$ jest trójkątna dolna, kolejne elementy $y$ oblicza się od pierwszego do ostatniego.
2. **Podstawianie wstecz:** $Ux=y$. Ponieważ $U$ jest trójkątna górna, niewiadome oblicza się od ostatniej do pierwszej.

Zamiast rozwiązywać od początku jeden ogólny układ, wykorzystujemy strukturę macierzy trójkątnych. Sam rozkład ma złożoność około $O(n^3)$, a podstawiania — $O(n^2)$.

## Co robi program?

Plik `main.py` wykonuje następujące kroki:

1. Wczytuje rozmiar macierzy, macierz $A$ i wektor $b$ z `input.txt`.
2. Wyznacza macierze $L$, $U$ oraz $P$ w funkcji `lu_decomposition`.
3. Rozwiązuje kolejno układy $Ly=Pb$ i $Ux=y$ w funkcji `solve_lu`.
4. Wyświetla dane wejściowe, macierze rozkładu i obliczony wektor \(x\).
5. Zgłasza komunikat, gdy podczas obliczeń napotka pivot bliski zeru.

Funkcja `load_matrix_from_file` odpowiada za odczyt danych. Stała `EPS = 1e-12` jest używana jako próg do wykrywania elementów diagonalnych uznanych za numerycznie bliskie zeru.

## Format pliku wejściowego

`input.txt` powinien zawierać:

1. W pierwszym wierszu rozmiar $n$.
2. W kolejnych $n$ wierszach — po $n$ liczb opisujących macierz $A$.
3. W ostatnim wierszu — $n$ liczb wektora $b$.

Przykład:

```text
2
2 1
1 3
5 7
```

Odpowiada on układowi:

$$
\begin{bmatrix}2&1\\1&3\end{bmatrix}
\begin{bmatrix}x_1\\x_2\end{bmatrix}
=
\begin{bmatrix}5\\7\end{bmatrix}
$$

Wiersze powinny zawierać liczby rozdzielone spacjami. Plik jest otwierany pod ścieżką względną `input.txt`, więc program należy uruchamiać z katalogu `MetodyNumeryczne/Lab1` albo zapewnić ten plik w bieżącym katalogu roboczym.

## Uruchomienie

Wymagany jest Python oraz biblioteka NumPy. W razie potrzeby można ją zainstalować poleceniem:

```bash
python -m pip install numpy
```

Następnie, z katalogu `MetodyNumeryczne/Lab1`, uruchom:

```bash
python main.py
```