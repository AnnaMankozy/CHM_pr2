def input_float_row(prompt, size):
    while True:
        try:
            row_data = list(map(float, input(prompt).split()))
            if len(row_data) != size:
                raise ValueError(f"Введіть {size} чисел.")
            return row_data
        except ValueError:
            print("Помилка.")


def verify_diagonal_dominance(matrix):
    n = len(matrix)
    for i in range(n):
        diag_elem = abs(matrix[i][i])
        row_sum = sum(abs(matrix[i][j]) for j in range(n) if j != i)
        if diag_elem <= row_sum:
            print("\nМатриця не задовольняє умову діагональної переваги.")
            exit()


def transform_matrix(A, n):
    B = []
    for i in range(n):
        if A[i][i] == 0:
            print("Діагональний елемент дорівнює 0. Обчислення неможливе.")
            exit()
        row = []
        for j in range(n):
            if j == i:
                row.append(0)
            else:
                row.append(-A[i][j] / A[i][i])
        B.append(row)
    return B


def calculate_norm(B, n):
    max_norm = 0
    for row in B:
        row_sum = sum(abs(x) for x in row)
        max_norm = max(max_norm, row_sum)
    if max_norm >= 1:
        print("Умова збіжності не виконується.")
        exit()
    return max_norm


def compute_free_terms(A, b, n):
    return [b[i] / A[i][i] for i in range(n)]


def iterative_calculation(B, g, x, n, norm, eps, k):
    max_delta = 0
    for i in range(n):
        # Використовуємо нові значення для j < i
        new_value = g[i] + sum(B[i][j] * x[j] for j in range(n) if j != i)
        diff = abs(new_value - x[i])
        max_delta = max(max_delta, diff)
        x[i] = new_value
    err = max_delta * norm / (1 - norm)
    return x, err <= eps, k + 1, err


def main_program():
    while True:
        try:
            n = int(input("Введіть розмір квадратної матриці: "))
            break
        except ValueError:
            print("Помилка.")

    A = []
    print("\nВведіть коефіцієнти матриці:")
    for i in range(n):
        A.append(input_float_row(f"Рядок {i + 1}: ", n))

    b = input_float_row(f"\nВведіть вектор вільних членів ({n} числа): ", n)

    while True:
        try:
            eps = float(input("\nВведіть бажану точність: "))
            break
        except ValueError:
            print("Помилка: потрібно ввести число.")

    print("\nРозширена матриця:")
    for i in range(n):
        print("[", " ".join(f"{val:6.2f}" for val in A[i]), f"| {b[i]:6.2f} ]")

    verify_diagonal_dominance(A)

    B = transform_matrix(A, n)
    g = compute_free_terms(A, b, n)
    norm = calculate_norm(B, n)

    x = g[:]  # початкове наближення
    k = 0

    while True:
        x, done, k, err = iterative_calculation(B, g, x, n, norm, eps, k)
        if done:
            break

    print("\nРезультат обчислень:")
    for i, val in enumerate(x):
        print(f"x{i + 1} = {val:.4f}")
    print(f"Кількість ітерацій: {k}")
    print(f"Оцінка похибки: {err:.4g}")


if __name__ == "__main__":
    main_program()
