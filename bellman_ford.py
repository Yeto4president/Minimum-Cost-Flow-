from utils import *
from prettytable import PrettyTable

def afficher_table_bellman_detaillee(noms, etapes):
    print("\nTable des distances et prédécesseurs (Bellman-Ford)")
    table = PrettyTable()
    headers = ["Étape"] + noms
    table.field_names = headers

    n = len(noms)
    for k in range(len(etapes) + 1):
        ligne = [str(k)]
        if k == 0:
            ligne += ["0"] + ["∞"] * (n - 1)
        else:
            distances, parents = etapes[k - 1]
            for i in range(n):
                if distances[i] == float('inf'):
                    ligne.append("∞")
                elif parents[i] == -1:
                    ligne.append(str(distances[i]))
                else:
                    ligne.append(f"{distances[i]} ({noms[parents[i]]})")
        table.add_row(ligne)

    print(table)

def executer_flot_min_cout(capacites, couts, noms, val_flot, afficher=True):
    n = len(capacites)
    source = 0
    puits = n - 1
    flot_total = 0
    cout_total = 0

    residuel = [row[:] for row in capacites]
    couts_residuel = [row[:] for row in couts]

    if afficher:
        print("\nDémarrage de l'algorithme de flot à coût minimal...")

    while flot_total < val_flot:
        distances = [float('inf')] * n
        parents = [-1] * n
        distances[source] = 0
        etapes = []

        for _ in range(n - 1):
            new_distances = distances[:]
            new_parents = parents[:]
            for u in range(n):
                for v in range(n):
                    if residuel[u][v] > 0 and distances[u] + couts_residuel[u][v] < new_distances[v]:
                        new_distances[v] = distances[u] + couts_residuel[u][v]
                        new_parents[v] = u
            etapes.append((new_distances[:], new_parents[:]))
            if new_distances == distances:
                break
            distances = new_distances
            parents = new_parents

        if afficher:
            afficher_table_bellman_detaillee(noms, etapes)

        if distances[puits] == float('inf'):
            if afficher:
                print("Aucun chemin possible. Arrêt de l'algorithme.")
            break

        chemin = []
        v = puits
        while v != source:
            u = parents[v]
            chemin.append((u, v))
            v = u
        chemin.reverse()

        if afficher:
            chemin_str = ' -> '.join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])
            print(f"Chemin sélectionné : {chemin_str}")

        flot_augmentable = min(residuel[u][v] for u, v in chemin)
        flot_envoye = min(flot_augmentable, val_flot - flot_total)
        cout_chaine = sum(couts_residuel[u][v] for u, v in chemin)

        if afficher:
            print(f"Flot envoyé : {flot_envoye}")
            print(f"Coût du chemin : {cout_chaine}")

        for u, v in chemin:
            residuel[u][v] -= flot_envoye
            residuel[v][u] += flot_envoye
            couts_residuel[v][u] = -couts_residuel[u][v]

        flot_total += flot_envoye
        cout_total += flot_envoye * cout_chaine

        if afficher:
            print("Matrice résiduelle mise à jour :")
            afficher_graphe_residuel_pondere(residuel, couts_residuel, noms)
            print(f"Flot cumulé : {flot_total} / {val_flot}")
            print(f"Coût cumulé : {cout_total}\n")

    if afficher:
        print("Algorithme terminé.")
        print(f"Flot total transmis : {flot_total}")
        print(f"Coût total du flot : {cout_total}")

    return flot_total
