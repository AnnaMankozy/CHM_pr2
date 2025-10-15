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
            value = -matrix_coeffs[i][j]/matrix_coeffs[i][i] if i != j else 0
            transformed_row.append(value)
        transformed.append(transformed_row)
    return transformed

def compute_free_terms(coeff_matrix, const_terms, size):
    return [const_terms[i]/coeff_matrix[i][i] for i in range(size)]

def calculate_norms(matrix, size):
    m_norm = max(sum(abs(elem) for elem in row) for row in matrix)
    one_norm = max(sum(abs(matrix[i][j]) for i in range(size)) for j in range(size))
    euclid_norm = math.sqrt(sum(matrix[i][j]**2 for i in range(size) for j in range(size)))
    return m_norm, one_norm, euclid_norm

def iterative_calculation(transformed_matrix, free_terms, init_guess, size, norm, tolerance):
    current_guess = init_guess[:]
    iteration_count = 0
    while True:
        max_delta = 0
        for i in range(size):
            new_value = free_terms[i] + sum(transformed_matrix[i][j] * current_guess[j] for j in range(size))
            diff = abs(new_value - current_guess[i])
            max_delta = max(max_delta, diff)
            current_guess[i] = new_value
        iteration_count += 1
        error_estimate = max_delta * norm / (1 - norm) if norm < 1 else max_delta
        if error_estimate <= tolerance:
            break
    return current_guess, iteration_count, error_estimate

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

    # Правильна еквівалентна система для ітерацій
    transformed_matrix = transform_matrix(coeff_matrix, dimension)
    free_terms = compute_free_terms(coeff_matrix, const_terms, dimension)

    print("\nЕквівалентна система (A' та b'):")
    print("Матриця A':")
    for row in transformed_matrix:
        print(" ".join(f"{val:8.4f}" for val in row))
    
    print("\nВектор вільних членів b':")
    for i, val in enumerate(free_terms):
        print(f"{val:8.4f}")

    # --- A1 і A2 ---
    A1 = [[transformed_matrix[i][j] if j < i else 0 for j in range(dimension)] for i in range(dimension)]
    A2 = [[transformed_matrix[i][j] if j > i else 0 for j in range(dimension)] for i in range(dimension)]

    print("\nМатриця A1 (нижня трикутна без діагоналі):")
    for row in A1:
        print(" ".join(f"{val:8.4f}" for val in row))

    print("\nМатриця A2 (верхня трикутна без діагоналі):")
    for row in A2:
        print(" ".join(f"{val:8.4f}" for val in row))

    # --- Перевірка норм ---
    m_norm, one_norm, euclid_norm = calculate_norms(transformed_matrix, dimension)
    print(f"\nПеревірка умови збіжності за еквівалентною системою ||a|| < 1:")
    print(f"m-норма = {m_norm:.4f} {'< 1 (задовольняє)' if m_norm < 1 else '> 1 (не задовольняє)'}")
    print(f"1-норма = {one_norm:.4f} {'< 1 (задовольняє)' if one_norm < 1 else '> 1 (не задовольняє)'}")
    print(f"Евклідова норма = {euclid_norm:.4f} {'< 1 (задовольняє)' if euclid_norm < 1 else '> 1 (не задовольняє)'}")

    while True:
        try:
            tolerance = float(input("\nВведіть бажану точність: "))
            break
        except ValueError:
            print("Помилка: потрібно ввести число.")

    solution, iterations, final_error = iterative_calculation(
        transformed_matrix, free_terms, free_terms[:], dimension, m_norm, tolerance
    )

    print("\nРезультат обчислень:")
    for idx, value in enumerate(solution):
        print(f"x{idx + 1} = {value:8.4f}")
    print(f"Кількість ітерацій: {iterations}")
    print(f"Оцінка похибки: {final_error:8.4f}")

if __name__ == "__main__":
    main_program()

