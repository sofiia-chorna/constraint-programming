from sys import exit, argv


# Test if the grid contains an error
def estContradictoire(liste):
    chiffres = set(liste) - {0}
    for c in chiffres:
        if liste.count(c) != 1:
            return True
    return False


# Return the list of possible values for a cell
def casePossibles(case, sudoku):
    chiffres = set(sudoku[case[0]])
    chiffres |= {sudoku[i][case[1]] for i in range(9)}
    cellule = case[0] // 3, case[1] // 3
    for i in range(3):
        chiffres |= set(sudoku[cellule[0] * 3 + i][cellule[1] * 3: (cellule[1] + 1) * 3])
    return list(set(range(1, 10)) - chiffres)


def is_sudoku_ok(sudoku):
    nl = len(sudoku)
    if nl != 9:
        print("Le jeu contient " + str(nl + 1) + " lignes au lieu de 9.")
        return False

    for l in range(9):
        if estContradictoire(sudoku[l]):
            print("La ligne " + str(l + 1) + " est contradictoire.")
            return False

    for c in range(9):
        colonne = [sudoku[l][c] for l in range(9)]
        if estContradictoire(colonne):
            print("La colonne " + str(c + 1) + " est contradictoire.")
            return False

    for l in range(3):
        for c in range(3):
            cellule = []
            for i in range(3):
                cellule = cellule + sudoku[l * 3 + i][c * 3 : (c + 1) * 3]
            if estContradictoire(cellule):
                print("La cellule (" + str(l + 1) + " ; " + str(c + 1) + ") est contradictoire.")
                return False
    return True


try:
    fichier = argv[1]
except IndexError:
    print("Usage : " + argv[0] + " fichier.txt")
    exit(0)

sudoku = []
trous = []

try:
    with open(fichier, "r") as f:
        for nl, ligne in enumerate(f):
            try:
                nouvelle = [int(i) for i in list(ligne.strip())]
            except ValueError:
                print("La ligne " + str(nl + 1) + " contient autre chose qu'un chiffre.")
                exit(1)
            if len(nouvelle) != 9:
                print("La ligne " + str(nl + 1) + " ne contient pas 9 chiffres.")
                exit(1)
            trous = trous + [[nl, i] for i in range(9) if nouvelle[i] == 0]
            sudoku.append(nouvelle)
except FileNotFoundError:
    print("Fichier " + fichier + " non trouvé.")
    exit(1)
except PermissionError:
    print("Vous n'avez pas le droit de lire le fichier " + fichier + ".")
    exit(1)

if not is_sudoku_ok(sudoku):
    exit(0)

# Display initial grid
print("Initial grid :")
for line in sudoku:
    elements = ""
    for element in line:
        elements = elements + str(element)
    print(elements)

# Resolution
possibles = [[] for i in range(len(sudoku) * len(sudoku[0]))]
caseAremplir = 0

while caseAremplir < len(trous):
    trou = trous[caseAremplir]
    possibles[caseAremplir] = casePossibles(trou, sudoku)

    while len(possibles[caseAremplir]) == 0:
        trou_line, trou_column = trous[caseAremplir]
        sudoku[trou_line][trou_column] = 0
        caseAremplir -= 1

    trou_line, trou_column = trous[caseAremplir]
    sudoku[trou_line][trou_column] = possibles[caseAremplir].pop()
    caseAremplir += 1

print("\nGrille resolue : ")

# Display solved grid
for line in sudoku:
    elements = ""
    for element in line:
        elements = elements + str(element)
    print(elements)
