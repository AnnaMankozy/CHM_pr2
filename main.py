import math

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
    dimension = len(matrix)
    for idx in range(dimension):
        diag_elem = abs(matrix[idx][idx])
        row_sum = sum(abs(matrix[idx][col]) for col in range(dimension) if col != idx)
        if diag_elem <= row_sum:
            print("\nМатриця не задовольняє умову діагональної переваги.")
            exit()

def transform_matrix(matrix_coeffs, size):
    transformed = []
    for i in range(size):
        if matrix_coeffs[i][i] == 0:
            print("Діагональний елемент дорівнює 0. Обчислення неможливе.")
            exit()
        transformed_row = []
        for j in range(size):
            value = -matrix_coeffs[i][j] / matrix_coeffs[i][i] if i != j else 0
            transformed_row.append(value)
        transformed.append(transformed_row)
    return transformed

def compute_free_terms(coeff_matrix, const_terms, size):
    return [const_terms[i] / coeff_matrix[i][i] for i in range(size)]

def calculate_norms(matrix, size):
    m_norm = max(sum(abs(elem) for elem in row) for row in matrix)
    one_norm = max(sum(abs(matrix[i][j]) for i in range(size)) for j in range(size))
    euclid_norm = math.sqrt(sum(matrix[i][j]**2 for i in range(size) for j in range(size)))
    return m_norm, one_norm, euclid_norm

def check_convergence(norms):
    m_norm, one_norm, euclid_norm = norms
    print("\nПеревірка достатньої умови збіжності за еквівалентною системою ( ||a|| < 1 ):")
    if m_norm < 1:
        print(f"m-норма = {m_norm:.4f} < 1 (задовольняє)")
    else:
        print(f"m-норма = {m_norm:.4f} >= 1 (не задовольняє)")
        exit()
    if one_norm < 1:
        print(f"1-норма = {one_norm:.4f} < 1 (задовольняє)")
    else:
        print(f"1-норма = {one_norm:.4f} >= 1 (не задовольняє)")
        exit()
    if euclid_norm < 1:
        print(f"Евклідова норма = {euclid_norm:.4f} < 1 (задовольняє)")
    else:
        print(f"Евклідова норма = {euclid_norm:.4f} >= 1 (не задовольняє)")
        exit()

def iterative_calculation(A1, A2, b, m_norm, tolerance):
    size = len(b)
    x_current = b[:]
    iteration = 0

    while True:
        iteration += 1
        x_prev = x_current[:]
        max_delta = 0

        for i in range(size):
            new_val = b[i]
            for j in range(i):
                new_val += A2[i][j] * x_current[j]
            for j in range(i, size):
                new_val += A1[i][j] * x_prev[j]

            diff = abs(new_val - x_prev[i])
            max_delta = max(max_delta, diff)
            x_current[i] = new_val

        A1_norm = max(sum(abs(num) for num in row) for row in A1)
        error_estimate = max_delta * (A1_norm / (1 - m_norm))

        if error_estimate < tolerance:
            break

    return x_current, iteration, error_estimate

def main_program():
    while True:
        try:
            dimension = int(input("Введіть розмір квадратної матриці: "))
            break
        except ValueError:
            print("Помилка.")

    coeff_matrix = []
    print("\nВведіть коефіцієнти матриці:")
    for i in range(dimension):
        coeff_matrix.append(input_float_row(f"Рядок {i + 1}: ", dimension))

    const_terms = input_float_row(f"\nВведіть вектор вільних членів ({dimension} числа): ", dimension)

    print("\nРозширена матриця:")
    for i in range(dimension):
        print("[", " ".join(f"{val:8.4f}" for val in coeff_matrix[i]), f"| {const_terms[i]:8.4f} ]")

    verify_diagonal_dominance(coeff_matrix)

    transformed_matrix = transform_matrix(coeff_matrix, dimension)
    free_terms = compute_free_terms(coeff_matrix, const_terms, dimension)

    print("\nЕквівалентна система:")
    for row in transformed_matrix:
        print(" ".join(f"{val:8.4f}" for val in row))

    print("\nВектор вільних членів:")
    for val in free_terms:
        print(f"{val:8.4f}")

    A1 = [[transformed_matrix[i][j] if j > i else 0 for j in range(dimension)] for i in range(dimension)]
    A2 = [[transformed_matrix[i][j] if j < i else 0 for j in range(dimension)] for i in range(dimension)]

    norms = calculate_norms(transformed_matrix, dimension)
    check_convergence(norms)

    while True:
        try:
            tolerance = float(input("\nВведіть бажану точність: "))
            break
        except ValueError:
            print("Помилка: потрібно ввести число.")

    solution, iterations, final_error = iterative_calculation(A1, A2, free_terms, norms[0], tolerance)

    print("\nРезультат обчислень:")
    for idx, value in enumerate(solution):
        print(f"x{idx + 1} = {value:.4f}")
    print(f"Кількість ітерацій: {iterations}")
    print(f"Похибка обчислень: {final_error:.4e}")

if __name__ == "__main__":
    main_program()







