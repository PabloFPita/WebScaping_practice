import csv

def load_csv(filename):
    with open(filename, "r") as input_file:
        reader = csv.reader(input_file, delimiter=',')
        matrix = [row for row in reader]
    return matrix

# Clean the matrix from the csv file deleting useless information, changing numbers to integres and floats and substituting empty
# values for None. Save this matrix on a clean variable called curated matrix.
def clean_matrix(matrix):
    """
    Cleans a matrix by converting empty strings to None, numeric strings to integers or floats,
    and leaving non-numeric strings as is.

    Args:
        matrix (list): A list of lists representing a matrix.

    Returns:
        list: A cleaned version of the input matrix.
    """
    curated_matrix = []
    for row in matrix:
        curated_row = []
        for element in row:
            if element == '':
                curated_row.append(None)
            elif element.isnumeric():
                curated_row.append(int(element))
            elif element.replace('.', '', 1).isnumeric():
                curated_row.append(float(element))
            else:
                curated_row.append(element)
        curated_matrix.append(curated_row)
    return curated_matrix

# Save the curated matrix on a new csv file.
def print_csv(matrix, file_path):
    with open(file_path, "w") as output_file:
        writer = csv.writer(output_file, delimiter=',')
        for row in matrix:
            writer.writerow(row)

# Load the curated matrix from the csv file.
filename = 'PracticasPython\P5-6_badformat_wikipedia.py\csv_bad_format.csv'
matrix = load_csv(filename)
curated_matrix = clean_matrix(matrix)
print_csv(curated_matrix, filename)
