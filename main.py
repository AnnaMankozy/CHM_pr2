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
    for row_idx in range(size):
        if matrix_coeffs[row_idx][row_idx] == 0:
            print("Діагональний елемент дорівнює 0. Обчислення неможливе.")
            exit()
        transformed_row = []
        for col_idx in range(size):
            value = -matrix_coeffs[row_idx][col_idx] / matrix_coeffs[row_idx][row_idx] if col_idx != row_idx else 0
            transformed_row.append(value)
        transformed.append(transformed_row)
    return transformed

def calculate_norm(transformed_matrix, size):
    max_norm_value = 0
    for row in transformed_matrix:
        row_norm = sum(abs(elem) for elem in row)
        max_norm_value = max(max_norm_value, row_norm)
    if max_norm_value >= 1:
        print("Умова збіжності не виконується.")
        exit()
    return max_norm_value

def compute_free_terms(coeff_matrix, const_terms, size):
    result_terms = []
    for i in range(size):
        result_terms.append(const_terms[i] / coeff_matrix[i][i])
    return result_terms

def iterative_calculation(transformed_matrix, free_terms, init_guess, size, norm, tolerance, iteration):
    updated_values = init_guess[:]
    max_delta = 0
    for i in range(size):
        new_value = free_terms[i] + sum(transformed_matrix[i][j] * updated_values[j] for j in range(size) if j != i)
        diff = abs(new_value - updated_values[i])
        max_delta = max(max_delta, diff)
        updated_values[i] = new_value
    error_estimate = max_delta * norm / (1 - norm)
    return updated_values, error_estimate <= tolerance, iteration + 1, error_estimate

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
        coeff_matrix.append(input_float_row(f"Рядок {i + 1}): ", dimension))

    const_terms = input_float_row(f"\nВведіть вектор вільних членів ({dimension} числа): ", dimension)

    print("\nРозширена матриця:")
    for i in range(dimension):
        print("[", " ".join(f"{val:6.2f}" for val in coeff_matrix[i]), f"| {const_terms[i]:6.2f} ]")

    verify_diagonal_dominance(coeff_matrix)

    transformed_matrix = transform_matrix(coeff_matrix, dimension)
    free_terms = compute_free_terms(coeff_matrix, const_terms, dimension)

    while True:
        try:
            tolerance = float(input("\nВведіть бажану точність: "))
            break
        except ValueError:
            print("Помилка: потрібно ввести число.")

    current_guess = free_terms[:]
    iteration_count = 0
    norm_value = calculate_norm(transformed_matrix, dimension)

    while True:
        current_guess, converged, iteration_count, current_error = iterative_calculation(
            transformed_matrix, free_terms, current_guess, dimension, norm_value, tolerance, iteration_count
        )
        if converged:
            break

    print("\nРезультат обчислень:")
    for idx, value in enumerate(current_guess):
        print(f"x{idx + 1} = {value:.4f}")
    print(f"Кількість ітерацій: {iteration_count}")
    print(f"Оцінка похибки: {current_error:.4g}")

if __name__ == "__main__":
    main_program()
