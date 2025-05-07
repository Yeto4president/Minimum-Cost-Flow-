from utils import afficher_matrice
def bfs(capacites, residuel, source, puits, parent, noms, iteration, afficher=True):
    n = len(capacites)
    visited = [False] * n
    visited[source] = True

    if afficher:
        print(f"\nItération {iteration} — Parcours BFS depuis {noms[source]}")

    niveaux = [[source]]
    level = 0

    while niveaux[level]:
        next_level = []
        ligne_sommets = []
        ligne_parents = []
        for u in niveaux[level]:
            for v in range(n):
                if not visited[v] and residuel[u][v] > 0:
                    parent[v] = u
                    visited[v] = True
                    next_level.append(v)
                    ligne_sommets.append(noms[v])
                    ligne_parents.append(f"Π({noms[v]}) = {noms[u]}")
                    if v == puits:
                        niveaux.append(next_level)
                        if afficher:
                            print("".join(ligne_sommets) + " : " + " , ".join(ligne_parents))
                        return True
        if ligne_sommets and afficher:
            print("".join(ligne_sommets) + " : " + " , ".join(ligne_parents))
        niveaux.append(next_level)
        level += 1

    return False

def ford_fulkerson(capacites, source, puits, noms, afficher=True):
    n = len(capacites)
    residuel = [row[:] for row in capacites]
    parent = [-1] * n
    flot_max = 0
    iteration = 1

    while bfs(capacites, residuel, source, puits, parent, noms, iteration, afficher):
        chemin = []
        v = puits
        flot = float('inf')
        while v != source:
            u = parent[v]
            chemin.append((u, v))
            flot = min(flot, residuel[u][v])
            v = u
        chemin.reverse()

        if afficher:
            chemin_str = " → ".join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])
            print(f"\nChaîne améliorante trouvée : {chemin_str} de flot = {flot}")

        v = puits
        while v != source:
            u = parent[v]
            residuel[u][v] -= flot
            residuel[v][u] += flot
            v = u

        if afficher:
            afficher_matrice("Matrice résiduelle mise à jour", residuel, noms)

        flot_max += flot
        iteration += 1

    if afficher:
        matrice_flot = [["0"]*n for _ in range(n)]
        for u in range(n):
            for v in range(n):
                if capacites[u][v] > 0:
                    matrice_flot[u][v] = f"{capacites[u][v] - residuel[u][v]}/{capacites[u][v]}"
        afficher_matrice("Flot maximum", matrice_flot, noms)
        print(f"Valeur totale du flot : {flot_max}")

    return flot_max

def executer_ford_fulkerson(capacites, noms, afficher=True):
    source = 0
    puits = len(capacites) - 1
    if afficher:
        print("\nExécution de l’algorithme Ford-Fulkerson")
    return ford_fulkerson(capacites, source, puits, noms, afficher=afficher)
