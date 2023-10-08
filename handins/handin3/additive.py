def read_matrix(file_name):
    with open(file_name, "r") as f:
        lines = f.readlines()
    matrix = []
    for line in lines:
        row = list(line.strip().split())
        matrix.append(row)
    for i, row in enumerate(matrix):
        matrix[i] = [int(a) for a in row]
    return matrix


def is_additive(matrix):
    n = len(matrix)

    # check every quadruplet
    for i in range(n):
        for j in range(n):
            for k in range(n):
                for l in range(n):
                    equal_count = 0  # equal to largest count

                    sum_1 = matrix[i][j] + matrix[k][l]
                    sum_2 = matrix[i][k] + matrix[j][l]
                    sum_3 = matrix[i][l] + matrix[j][k]

                    largest = max(sum_1, sum_2, sum_3)

                    if sum_1 == largest:
                        equal_count += 1
                    if sum_2 == largest:
                        equal_count += 1
                    if sum_3 == largest:
                        equal_count += 1

                    if equal_count < 2:
                        return False
    return True


if __name__ == "__main__":
    DATA_PATH = "handins/handin3/ultrametric.txt"
    m = read_matrix(DATA_PATH)
    print(is_additive(m))
