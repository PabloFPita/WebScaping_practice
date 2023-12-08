import csv

filename = "PracticasPython\csv_bad_format.csv"
with open(filename) as f:
    reader = csv.reader(f, delimiter=",")
    matrix = list(reader)

curated_matrix = []

for row in matrix:
    curated_row = []
    for value in row:
        # Eliminar las comillas y los espacios en blanco
        value = value.strip('" ')
        # Convertir los números en enteros o flotantes
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value.replace(",", "."))
            except ValueError:
                pass
        # Sustituir las celdas vacías o n/a por None
        if value == "" or value == "n/a":
            value = None
        curated_row.append(value)
    curated_matrix.append(curated_row)
