from utils import *
from prettytable import PrettyTable

def push_relabel(capacites, noms, afficher=True):
    n = len(capacites)
    source = 0
    puits = n - 1

    hauteur = [0] * n
    exces = [0] * n
    residuel = [row[:] for row in capacites]

    hauteur[source] = n
    for v in range(n):
        if residuel[source][v] > 0:
            flot = residuel[source][v]
            residuel[source][v] -= flot
            residuel[v][source] += flot
            exces[v] += flot
            exces[source] -= flot

    def push(u, v):
        delta = min(exces[u], residuel[u][v])
        residuel[u][v] -= delta
        residuel[v][u] += delta
        exces[u] -= delta
        exces[v] += delta
        if afficher:
            print(f"Push effectué : {noms[u]} → {noms[v]} (Δ = {delta})")

    def relabel(u):
        min_h = float('inf')
        for v in range(n):
            if residuel[u][v] > 0:
                min_h = min(min_h, hauteur[v])
        if min_h < float('inf'):
            if afficher:
                print(f"Relabel : {noms[u]} passe de {hauteur[u]} à {min_h + 1}")
            hauteur[u] = min_h + 1

    def afficher_etat(iteration):
        if afficher:
            print(f"\nÉtat à l’itération {iteration} :")
            table = PrettyTable()
            table.field_names = ["Sommet", "Hauteur", "Excès"]
            for i in range(n):
                table.add_row([noms[i], hauteur[i], exces[i]])
            print(table)
            afficher_matrice("Graphe résiduel", residuel, noms)

    def choisir_sommet_actif():
        candidats = [(hauteur[i], noms[i], i) for i in range(n) if i != source and i != puits and exces[i] > 0]
        if not candidats:
            return None
        return sorted(candidats, key=lambda x: (-x[0], x[1]))[0][2]

    if afficher:
        print("\n--- Début de l’algorithme Push-Relabel ---")
    iteration = 1
    afficher_etat(iteration)

    while True:
        u = choisir_sommet_actif()
        if u is None:
            break

        pushed = False
        voisins = sorted([v for v in range(n) if residuel[u][v] > 0], key=lambda x: (noms[x] != noms[puits], noms[x]))
        for v in voisins:
            if residuel[u][v] > 0 and hauteur[u] == hauteur[v] + 1:
                push(u, v)
                afficher_etat(iteration)
                pushed = True
                break
        if not pushed:
            relabel(u)
            afficher_etat(iteration)

        iteration += 1

    if afficher:
        print("\nRésumé du flot maximum :")
        matrice_flot = [["0"]*n for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if capacites[u][v] > 0:
                    matrice_flot[u][v] = f"{capacites[u][v] - residuel[u][v]}/{capacites[u][v]}"
        afficher_matrice("Flot maximum", matrice_flot, noms)
        print(f"Valeur totale du flot : {exces[puits]}")

    return exces[puits]

def executer_push_relabel(capacites, noms, afficher=True):
    return push_relabel(capacites, noms, afficher=afficher)