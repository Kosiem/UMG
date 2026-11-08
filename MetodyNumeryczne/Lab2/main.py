"""
Metody Numeryczne - Laboratorium 2
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


def qr_decomposition(matrix_a, matrix_n) -> tuple:
    """
    Rozkład QR macierzy A na macierz ortogonalną Q i macierz górna R.

    Parameters:
    matrix_a: Macierz A do rozkładu.
    matrix_n: Liczba wierszy macierzy A.

    Returns:
    matrix_q: Macierz ortogonalna Q.
    matrix_r: Macierz górna R.
    """
    # Macierz ortogonalna
    matrix_q = np.zeros((matrix_n, matrix_n))
    # Macierz trojkatna gorna
    matrix_r = np.zeros((matrix_n, matrix_n))

    for i in range(matrix_n):
        # Tworzenie wektora kolumny
        # Zapis [:,i] oznacza, że bierzemy wszystkie wiersze i kolumnę i
        column_vector = matrix_a[:, i].copy()

        # Przechodzimy przez wszystkie poprzednie kolumny
        # aby obliczyć wartości R i zaktualizować wektor kolumny
        for j in range(i):
            # Iloczyn skalarny wektora kolumny z kolumną Q,
            # jaka część wektora kolumny jest w kierunku Q[:,j]
            matrix_r[j, i] = np.dot(matrix_q[:, j], column_vector)
            # Odejmowanie iloczynu skalarnych od wektora kolumny
            column_vector = column_vector - matrix_r[j][i] * matrix_q[:, j]

        # Normalizacja wektora kolumny,
        # który teraz jest ortogonalny do wszystkich poprzednich kolumn Q
        matrix_r[i][i] = np.linalg.norm(column_vector)

        if matrix_r[i][i] < EPS:
            raise ZeroDivisionError

        # Normalizacja wektora kolumny (długość 1) i zapisanie go do macierzy Q
        matrix_q[:, i] = column_vector / matrix_r[i][i]

    return matrix_q, matrix_r


def solve_qr(matrix_q, matrix_r, matrix_b, matrix_n):
    """
    Rozwiązuje układ równań liniowych Ax = B przy użyciu rozkładu QR.

    Parameters:
    matrix_q: Macierz ortogonalna Q z rozkładu QR.
    matrix_r: Macierz górna R z rozkładu QR.
    matrix_b: Wektor B w równaniu Ax = B.
    matrix_n: Liczba wierszy macierzy A.

    Returns:
    x: Rozwiązanie układu równań Ax = B.

    """
    # Q^T * B
    matrix_b = np.dot(matrix_q.T, matrix_b)
    # Wektor x do przechowywania rozwiązania
    x = np.zeros(matrix_n)

    # Przechodzimy od ostatniego wiersza do pierwszego
    for i in range(matrix_n - 1, -1, -1):

        if abs(matrix_r[i][i]) < EPS:
            raise ZeroDivisionError

        value = 0.0

        # Przechodzimy przez wszystkie kolumny po prawej stronie od i,
        # aby obliczyć wartość dla x[i]
        for j in range(i + 1, matrix_n):
            # Obliczenie sumy znanych wartości
            value += matrix_r[i][j] * x[j]

        # Obliczenie kolejnej niewiadomej
        x[i] = (matrix_b[i] - value) / matrix_r[i][i]

    return x


def main():
    """
    Wczytaj macierz z pliku, zrób rozkład QR i rozwiąż układ równań.
    """
    try:
        matrix_a, matrix_b, matrix_n = load_matrix_from_file("input2.txt")

        print("Rozmiar macierzy:", matrix_n)
        print("Macierz A:", matrix_a)
        print("Wektor B:", matrix_b)

        print("Rozkład QR macierzy A:")
        matrix_q, matrix_r = qr_decomposition(np.array(matrix_a), matrix_n)
        print("Macierz Q:")
        for row in matrix_q:
            print(row)
        print("Macierz R:")
        for row in matrix_r:
            print(row)

        x = solve_qr(matrix_q, matrix_r, np.array(matrix_b), matrix_n)
        print("Rozwiązanie x:", x)
    except ZeroDivisionError:
        print(
            "Dzielenie przez zero wystąpiło podczas rozkładu QR. "
            "Macierz A może być osobliwa."
        )


if __name__ == "__main__":
    main()
