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


def is_ultra(matrix):
    n = len(matrix)
    for i in range(n):
        for j in range(n):
            for k in range(n):
                equal_count = 0
                largest = max(matrix[i][j], matrix[i][k], matrix[j][k])
                if matrix[i][j] == largest:
                    equal_count += 1
                if matrix[i][k] == largest:
                    equal_count += 1
                if matrix[j][k] == largest:
                    equal_count += 1

                if equal_count < 2:
                    return False
    return True


if __name__ == "__main__":
    DATA_PATH = "./ultrametric.txt"
    m = read_matrix(DATA_PATH)
    print(is_ultra(m))
