import csv

def load_csv(filename):
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def load_csv2(filename):
    with open(filename, "r") as input_file:
        reader = csv.reader(input_file, delimiter=';')
        matrix = [row for row in reader]
    return matrix

def print_csv(matrix, file_path):
    with open(file_path, "w") as output_file:
        writer = csv.writer(output_file, delimiter=';')
        for row in matrix:
            writer.writerow(row)

filename = '.\PracticasPython\csv_bad_format.csv'
matrix = load_csv2(filename)
print_csv(matrix, filename)