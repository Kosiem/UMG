"""
Metody Numeryczne - Laboratorium 1
"""

import numpy as np

# Stała dla maksymalnej wartości zero
EPS = 1e-12


def load_matrix_from_file(filename) -> tuple:
    """
    Funkcja wczytująca macierz z pliku tekstowego.

    Parameters:
    filename (str): Scieżka do pliku tekstowego zawierającego macierz.

    Returns:
    matrix_a: Macierz A wczytana z pliku.
    matrix_b: Wektor B wczytany z pliku.
    matrix_n: Liczba wierszy macierzy A.
    """

    with open(filename, "r", encoding="utf-8") as file:

        matrix_n = int(file.readline().strip())

        matrix_a = []
        for _ in range(matrix_n):
            row = list(map(float, file.readline().strip().split()))
            matrix_a.append(row)

        matrix_b = [float(x) for x in file.readline().strip().split()]

    return matrix_a, matrix_b, matrix_n


def lu_decomposition(matrix_a, matrix_n) -> tuple:
    """
    Rozkład LU macierzy A na macierz dolną L i macierz górną U.

    Parameters:
    matrix_a: Macierz A do rozkładu.
    matrix_n: Liczba wierszy macierzy A.

    Returns:
    matrix_l: Macierz dolna L.
    matrix_u: Macierz górna U.
    matrix_p: Macierz permutacyjna P.
    """
    # Macierz L, trojkątna dolna
    matrix_l = np.zeros((matrix_n, matrix_n))
    # Macierz U, trojkątna górna
    matrix_u = matrix_a.copy()
    # Macierz P, permutacyjna
    matrix_p = np.eye(matrix_n)

    for i in range(matrix_n):
        # Szukanie największego elementu w kolumnie i wierszu
        pivot = -1.0
        row_with_max = i
        for col in range(i, matrix_n):
            # Sprawdzenie czy element jest większy od aktualnego pivotu
            if abs(matrix_u[col][i]) > pivot:
                pivot = abs(matrix_u[col][i])
                row_with_max = col
        if row_with_max != i:
            # Zamień wiersze w macierzy U i P, jeśli znaleziono lepszy pivot
            copy_u = matrix_u.copy()
            copy_p = matrix_p.copy()

            matrix_u[i], matrix_u[row_with_max] = (
                copy_u[row_with_max],
                copy_u[i],
            )
            matrix_p[i], matrix_p[row_with_max] = (
                copy_p[row_with_max],
                copy_p[i],
            )

            # Zamień wcześniejsze współczynniki wierszy macierzy L
            if i > 0:
                copy_l_i = matrix_l[i, :i].copy()
                matrix_l[i, :i] = matrix_l[row_with_max, :i]
                matrix_l[row_with_max, :i] = copy_l_i

        if abs(matrix_u[i][i]) < EPS:
            raise ZeroDivisionError

        # Wpisz jedynkę na przekątnej macierzy L
        matrix_l[i][i] = 1.0
        for k in range(i + 1, matrix_n):
            # Mnożnik do eliminacji elementu poniżej przekątnej macierzy U
            factor = matrix_u[k][i] / matrix_u[i][i]
            matrix_l[k][i] = factor
            # Wstaw zero poniżej przekątnej macierzy U
            matrix_u[k][i] = 0.0
            for j in range(i + 1, matrix_n):
                # Zaktualizuj wiersz U przez eliminację z użyciem wiersza i
                matrix_u[k][j] -= factor * matrix_u[i][j]

    return matrix_l, matrix_u, matrix_p


def solve_lu(matrix_l, matrix_u, matrix_p, matrix_b, matrix_n):
    """
    Rozwiązuje układ równań liniowych Ax = B przy użyciu rozkładu LU.

    Parameters:
    matrix_l: Macierz dolna L z rozkładu LU.
    matrix_u: Macierz górna U z rozkładu LU.
    matrix_p: Macierz permutacyjna P z rozkładu LU.
    matrix_b: Wektor B w równaniu Ax = B.
    matrix_n: Liczba wierszy macierzy A.

    Returns:
    x: Rozwiązanie układu równań Ax = B.

    """
    permuted_b = np.dot(matrix_p, matrix_b)

    # Ly = Pb
    y = np.zeros(matrix_n)
    for i in range(matrix_n):
        value = 0.0
        for j in range(i):
            value += matrix_l[i][j] * y[j]
        y[i] = permuted_b[i] - value

    # Ux = y
    x = np.zeros(matrix_n)
    for i in range(matrix_n - 1, -1, -1):
        if abs(matrix_u[i][i]) < EPS:
            raise ZeroDivisionError
        value = 0.0
        for j in range(i + 1, matrix_n):
            value += matrix_u[i][j] * x[j]
        x[i] = (y[i] - value) / matrix_u[i][i]

    return x


def main():
    """
    Wczytaj macierz z pliku, zrób rozkład LU i rozwiąż układ równań.
    """
    try:
        matrix_a, matrix_b, matrix_n = load_matrix_from_file("test.txt")

        print("Rozmiar macierzy:", matrix_n)
        print("Macierz A:", matrix_a)
        print("Wektor B:", matrix_b)

        print("Rozkład LU macierzy A:")
        matrix_l, matrix_u, matrix_p = lu_decomposition(matrix_a, matrix_n)
        print("Macierz L:")
        for row in matrix_l:
            print(row)
        print("Macierz U:")
        for row in matrix_u:
            print(row)
        print("Macierz P:")
        for row in matrix_p:
            print(row)

        x = solve_lu(matrix_l, matrix_u, matrix_p, matrix_b, matrix_n)
        print("Rozwiązanie x:", x)

    except ZeroDivisionError:
        print(
            "Dzielenie przez zero wystąpiło podczas rozkładu LU. "
            "Macierz A może być osobliwa."
        )


if __name__ == "__main__":
    main()
