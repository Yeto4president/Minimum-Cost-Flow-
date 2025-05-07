import os, random, math
from prettytable import PrettyTable

def lire_graphe(path):
    with open(path, 'r') as f:
        lines = f.readlines()
    n = int(lines[0].strip())
    capacites = [list(map(int, lines[i + 1].strip().split())) for i in range(n)]
    couts = [list(map(int, lines[i + 1 + n].strip().split())) for i in range(n)] if len(lines) >= 2 * n + 1 else None
    return n, capacites, couts

def get_noms_sommets(n):
    return ['s'] + [chr(ord('a') + i - 1) for i in range(1, n - 1)] + ['t'] if n > 2 else ['s', 't'][:n]

def est_flot_a_cout_min(numero):
    return numero >= 6

def afficher_matrice(nom, matrice, noms_sommets=None):
    if matrice is None:
        print("Aucune donnée.")
        return
    if noms_sommets is None:
        noms_sommets = get_noms_sommets(len(matrice))

    table = PrettyTable()
    table.field_names = [" "] + noms_sommets
    for i, row in enumerate(matrice):
        display_row = [noms_sommets[i]] + row
        table.add_row(display_row)

    print(f"\n=== {nom} ===")
    print(table)

def generer_graphe_aleatoire(n):
    capacites = [[0]*n for _ in range(n)]
    couts = [[0]*n for _ in range(n)]
    couples = [(i, j) for i in range(n) for j in range(n) if i != j]
    for i, j in random.sample(couples, math.floor(n*n/2)):
        capacites[i][j] = random.randint(1, 100)
        couts[i][j] = random.randint(1, 100)
    return capacites, couts


def afficher_graphe_residuel_pondere(residuel, couts_residuel, noms):
    n = len(residuel)
    table = PrettyTable()
    table.field_names = [" "] + noms
    for i in range(n):
        row = []
        for j in range(n):
            if residuel[i][j] > 0:
                row.append(f"{residuel[i][j]} ; {couts_residuel[i][j]}")
            else:
                row.append("0")
        table.add_row([noms[i]] + row)
    print("\n=== Graphe résiduel pondéré (capacité ; coût) ===")
    print(table)
