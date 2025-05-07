import os
from prettytable import PrettyTable

# === CONFIGURATION ===
GROUPE = "K5"
DOSSIER_BASE = "traces-executions"
os.makedirs(DOSSIER_BASE, exist_ok=True)

# === LOGGER ===
def log(nom_fichier, msg=""):
    with open(nom_fichier, "a", encoding="utf-8") as f:
        f.write(str(msg) + "\n")

# === OUTILS ===
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

def afficher_matrice(nom_fichier, nom, matrice, noms_sommets=None):
    if matrice is None:
        log(nom_fichier, "Aucune donnée.")
        return
    if noms_sommets is None:
        noms_sommets = get_noms_sommets(len(matrice))
    table = PrettyTable()
    table.field_names = [" "] + noms_sommets
    for i, row in enumerate(matrice):
        table.add_row([noms_sommets[i]] + row)
    log(nom_fichier, f"\n=== {nom} ===\n{table}")

# === ALGOS ===
def executer_ford_fulkerson(capacites, noms, nom_fichier):
    source = 0
    puits = len(capacites) - 1
    log(nom_fichier, "\nExécution de l’algorithme Ford-Fulkerson")
    return ford_fulkerson(capacites, source, puits, noms, nom_fichier)

def ford_fulkerson(capacites, source, puits, noms, nom_fichier):
    n = len(capacites)
    residuel = [row[:] for row in capacites]
    parent = [-1] * n
    flot_max = 0
    iteration = 1

    while bfs(capacites, residuel, source, puits, parent, noms, iteration, nom_fichier):
        chemin = []
        v = puits
        flot = float('inf')
        while v != source:
            u = parent[v]
            chemin.append((u, v))
            flot = min(flot, residuel[u][v])
            v = u
        chemin.reverse()
        chemin_str = " → ".join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])
        log(nom_fichier, f"\nChaîne améliorante trouvée : {chemin_str} de flot = {flot}")
        v = puits
        while v != source:
            u = parent[v]
            residuel[u][v] -= flot
            residuel[v][u] += flot
            v = u
        afficher_matrice(nom_fichier, "Matrice résiduelle mise à jour", residuel, noms)
        flot_max += flot
        iteration += 1

    matrice_flot = [["0"]*n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if capacites[u][v] > 0:
                matrice_flot[u][v] = f"{capacites[u][v] - residuel[u][v]}/{capacites[u][v]}"
    afficher_matrice(nom_fichier, "Flot maximum", matrice_flot, noms)
    log(nom_fichier, f"Valeur totale du flot : {flot_max}")
    return flot_max

def bfs(capacites, residuel, source, puits, parent, noms, iteration, nom_fichier):
    n = len(capacites)
    visited = [False] * n
    visited[source] = True
    log(nom_fichier, f"\nItération {iteration} — Parcours BFS depuis {noms[source]}")
    niveaux = [[source]]
    level = 0
    while niveaux[level]:
        next_level, ligne_sommets, ligne_parents = [], [], []
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
                        log(nom_fichier, "".join(ligne_sommets) + " : " + " , ".join(ligne_parents))
                        return True
        if ligne_sommets:
            log(nom_fichier, "".join(ligne_sommets) + " : " + " , ".join(ligne_parents))
        niveaux.append(next_level)
        level += 1
    return False

def executer_push_relabel(capacites, noms, nom_fichier):
    from prettytable import PrettyTable
    n = len(capacites)
    source, puits = 0, n - 1
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

    def log_etat(iteration):
        table = PrettyTable()
        table.field_names = ["Sommet", "Hauteur", "Excès"]
        for i in range(n):
            table.add_row([noms[i], hauteur[i], exces[i]])
        log(nom_fichier, f"\nÉtat à l'itération {iteration} :\n{table}")
        afficher_matrice(nom_fichier, "Graphe résiduel", residuel, noms)

    def choisir_sommet_actif():
        candidats = [(hauteur[i], noms[i], i) for i in range(n) if i != source and i != puits and exces[i] > 0]
        return sorted(candidats, key=lambda x: (-x[0], x[1]))[0][2] if candidats else None

    def push(u, v):
        delta = min(exces[u], residuel[u][v])
        residuel[u][v] -= delta
        residuel[v][u] += delta
        exces[u] -= delta
        exces[v] += delta
        log(nom_fichier, f"Push : {noms[u]} -> {noms[v]} (delta = {delta})")

    def relabel(u):
        min_h = float('inf')
        for v in range(n):
            if residuel[u][v] > 0:
                min_h = min(min_h, hauteur[v])
        if min_h < float('inf'):
            log(nom_fichier, f"Relabel : {noms[u]} (h: {hauteur[u]} -> {min_h + 1})")
            hauteur[u] = min_h + 1

    log(nom_fichier, "\nDémarrage de Push-Relabel")
    iteration = 1
    log_etat(iteration)

    while True:
        u = choisir_sommet_actif()
        if u is None:
            break
        pushed = False
        voisins = sorted([v for v in range(n) if residuel[u][v] > 0], key=lambda x: (noms[x] != noms[puits], noms[x]))
        for v in voisins:
            if residuel[u][v] > 0 and hauteur[u] == hauteur[v] + 1:
                push(u, v)
                log_etat(iteration)
                pushed = True
                break
        if not pushed:
            relabel(u)
            log_etat(iteration)
        iteration += 1

    matrice_flot = [["0"]*n for _ in range(n)]
    for u in range(n):
        for v in range(n):
            if capacites[u][v] > 0:
                matrice_flot[u][v] = f"{capacites[u][v] - residuel[u][v]}/{capacites[u][v]}"
    log(nom_fichier, "\nFlot final :")
    afficher_matrice(nom_fichier, "Flot maximum", matrice_flot, noms)
    log(nom_fichier, f"Valeur du flot maximal = {exces[puits]}")
    return exces[puits]

def executer_flot_min_cout(capacites, couts, noms, val_flot, nom_fichier):
    n = len(capacites)
    source, puits = 0, n - 1
    flot_total = 0
    cout_total = 0
    residuel = [row[:] for row in capacites]
    couts_residuel = [row[:] for row in couts]

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
            distances, parents = new_distances, new_parents

        if distances[puits] == float('inf'):
            log(nom_fichier, "Aucun chemin possible. Arrêt de l'algorithme.")
            break

        chemin = []
        v = puits
        while v != source:
            u = parents[v]
            chemin.append((u, v))
            v = u
        chemin.reverse()

        chemin_str = ' -> '.join([noms[u] for u, _ in chemin] + [noms[chemin[-1][1]]])
        log(nom_fichier, f"Chemin sélectionné : {chemin_str}")

        flot_augmentable = min(residuel[u][v] for u, v in chemin)
        flot_envoye = min(flot_augmentable, val_flot - flot_total)
        cout_chaine = sum(couts_residuel[u][v] for u, v in chemin)

        log(nom_fichier, f"Flot envoyé : {flot_envoye}")
        log(nom_fichier, f"Coût du chemin : {cout_chaine}")

        for u, v in chemin:
            residuel[u][v] -= flot_envoye
            residuel[v][u] += flot_envoye
            couts_residuel[v][u] = -couts_residuel[u][v]

        flot_total += flot_envoye
        cout_total += flot_envoye * cout_chaine

        afficher_matrice(nom_fichier, "Graphe résiduel (capacité ; coût)", [[f"{residuel[i][j]} ; {couts_residuel[i][j]}" if residuel[i][j] > 0 else "0" for j in range(n)] for i in range(n)], noms)
        log(nom_fichier, f"Flot cumulé : {flot_total} / {val_flot}")
        log(nom_fichier, f"Coût cumulé : {cout_total}\n")

    log(nom_fichier, "Algorithme terminé.")
    log(nom_fichier, f"Flot total transmis : {flot_total}")
    log(nom_fichier, f"Coût total du flot : {cout_total}")
    return flot_total

# === MAIN ===
def main():
    for numero in range(1, 11):
        n, capacites, couts = lire_graphe(f"fichier_test/K5-proposition{numero}")
        noms = get_noms_sommets(n)

        if numero <= 5:
            # Ford-Fulkerson
            nom_fichier_ff = os.path.join(DOSSIER_BASE, f"K5-trace{numero}-FF.txt")
            open(nom_fichier_ff, 'w').close()
            executer_ford_fulkerson(capacites, noms, nom_fichier_ff)

            # Push-Relabel
            nom_fichier_pr = os.path.join(DOSSIER_BASE, f"K5-trace{numero}-PR.txt")
            open(nom_fichier_pr, 'w').close()
            executer_push_relabel(capacites, noms, nom_fichier_pr)

        else:
            # Flot à coût minimal
            nom_fichier_min = os.path.join(DOSSIER_BASE, f"K5-trace{numero}-MIN.txt")
            open(nom_fichier_min, 'w').close()
            sortie_s = sum(capacites[0])
            entree_t = sum(capacites[i][n - 1] for i in range(n))
            val_flot = min(sortie_s, entree_t)
            executer_flot_min_cout(capacites, couts, noms, val_flot, nom_fichier_min)

if __name__ == "__main__":
    main()
