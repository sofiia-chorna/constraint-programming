from sys import exit, argv
import time


def estContradictoire(liste):
    """
    Test if the grid contains an error
    """
    chiffres = set(liste) - {0}
    for c in chiffres:
        if liste.count(c) != 1:
            return True
    return False


def casePossibles(case, sudoku):
    """
    Return the list of possible values for a cell
    """
    chiffres = set(sudoku[case[0]])
    chiffres |= {sudoku[i][case[1]] for i in range(9)}
    cellule = case[0] // 3, case[1] // 3
    for i in range(3):
        chiffres |= set(
            sudoku[cellule[0] * 3 + i][cellule[1] * 3 : (cellule[1] + 1) * 3]
        )
    return list(set(range(1, 10)) - chiffres)


def get_min_gap(gaps, sudoku):
    """
    Get the index of gap with smallest number of possible values
    """
    min_len = 10
    best_cell_index = 0

    for index, gap in enumerate(gaps):
        possibles_len = len(casePossibles(gap, sudoku))
        if possibles_len < min_len and possibles_len != 0:
            min_len = possibles_len
            best_cell_index = index

    return best_cell_index


try:
    file = argv[1]
except IndexError:
    print("Usage : " + argv[0] + " file.txt")
    exit(0)

sudoku = []
gaps = []


# Read input file
try:
    with open(file, "r") as f:
        for index, ligne in enumerate(f):
            # Check all are numbers
            try:
                line_items = [int(i) for i in list(ligne.strip())]
            except ValueError:
                print(
                    "La ligne "
                    + str(index + 1)
                    + " contient autre chose qu'un chiffre."
                )
                exit(1)

            # Check lenght
            if len(line_items) != 9:
                print("La ligne " + str(index + 1) + " ne contient pas 9 chiffres.")
                exit(1)

            # Get cells without value
            gaps.extend([[index, i] for i in range(9) if line_items[i] == 0])

            # Add line to sudoku
            sudoku.append(line_items)
except FileNotFoundError:
    print("Fichier " + file + " non trouvé.")
    exit(1)
except PermissionError:
    print("Vous n'avez pas le droit de lire le file " + file + ".")
    exit(1)


N_rows = len(sudoku)
if N_rows != 9:
    print("Le jeu contient " + str(N_rows + 1) + " lignes au lieu de 9.")
    exit(0)

# Check lines are correct
for row_index in range(9):
    if estContradictoire(sudoku[row_index]):
        print("La ligne " + str(row_index + 1) + " est contradictoire.")
        exit(1)

# Check columns are correct
for column_index in range(9):
    colonne = [sudoku[row_index][column_index] for row_index in range(9)]
    if estContradictoire(colonne):
        print("La colonne " + str(column_index + 1) + " est contradictoire.")
        exit(1)

# Check subsets are correct
for cell_row_index in range(3):
    for cell_column_index in range(3):
        cell = []
        for elem_index in range(3):
            # Get cell row index
            cell_elem_row_index = cell_row_index * 3 + elem_index

            # Get cell column indexes
            cell_elem_column_index_start = cell_column_index * 3
            cell_elem_column_index_end = (cell_column_index + 1) * 3

            # Add elements to cell
            cell.extend(
                sudoku[cell_elem_row_index][
                    cell_elem_column_index_start:cell_elem_column_index_end
                ]
            )

        # Check cell is correct
        if estContradictoire(cell):
            print(
                "La cellule ("
                + str(cell_row_index + 1)
                + " ; "
                + str(cell_column_index + 1)
                + ") est contradictoire."
            )
            exit(1)

# Display initial grid
print("Initial grid :")
for line in sudoku:
    elements = ""
    for element in line:
        elements = elements + str(element)
    print(elements)

# Start tracking time
start_time = time.time()

# Resolution
N_columns = len(sudoku[0])
possibles = [[] for _ in range(N_rows * N_columns)]
CUR_GAP_INDEX = 0


while len(gaps) != 0:
    gap_index = get_min_gap(gaps, sudoku)
    gap = gaps[gap_index]
    possibles[gap_index] = casePossibles(gap, sudoku)

    if len(possibles[gap_index]) == 0:
        print("No solution!")
        exit(0)

    sudoku[gap[0]][gap[1]] = possibles[gap_index].pop()
    gaps.remove(gap)

# Display solved grid
print("\nGrille resolue : ")
for line in sudoku:
    elements = ""
    for element in line:
        elements = elements + str(element)
    print(elements)

# Execution time
exec_time = time.time() - start_time
print("\nExecution time :", exec_time)
