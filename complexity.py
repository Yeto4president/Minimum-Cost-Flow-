import random
import time
import csv
import os
from ford_fulkerson import *
from push_relabel import *
from bellman_ford import *

# Génère matrices de capacité et de coût pour un graphe de flot
def generer_matrice_flot(n):
    capacites = [[0]*n for _ in range(n)]
    couts = [[0]*n for _ in range(n)]
    nb_aretes = (n * n) // 2
    indices = [(i, j) for i in range(n) for j in range(n) if i != j]
    echantillon = random.sample(indices, nb_aretes)

    for i, j in echantillon:
        capacites[i][j] = random.randint(1, 100)
        couts[i][j] = random.randint(1, 100)

    return capacites, couts

# Mesure du temps pour Ford-Fulkerson
def mesurer_temps_ford_fulkerson(capacites):
    noms = [str(i) for i in range(len(capacites))]
    start = time.perf_counter()
    ford_fulkerson(capacites, 0, len(capacites)-1, noms, afficher=False)
    end = time.perf_counter()
    return round(end - start, 20)

# Mesure du temps pour Push-Relabel
def mesurer_temps_push_relabel(capacites):
    noms = [str(i) for i in range(len(capacites))]
    start = time.perf_counter()
    push_relabel(capacites, noms, afficher=False)
    end = time.perf_counter()
    return round(end - start, 20)

# Mesure du temps pour Flot à coût minimal
def mesurer_temps_flot_min_cout(capacites, couts):
    noms = [str(i) for i in range(len(capacites))]
    val_flot = ford_fulkerson(capacites, 0, len(capacites)-1, noms, afficher=False) // 2
    start = time.perf_counter()
    executer_flot_min_cout(capacites, couts, noms, val_flot, afficher=False)
    end = time.perf_counter()
    return round(end - start, 20)

# Exécution avec écriture immédiate dans le CSV
def executer_mesures(tailles, repetitions=100, nom_fichier='temps_execution_algorithmes.csv'):
    fichier_existe = os.path.isfile(nom_fichier)

    with open(nom_fichier, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["n", "Ford-Fulkerson", "Push-Relabel", "Flot Min-Cout"])
        if not fichier_existe:
            writer.writeheader()

        for n in tailles:
            for rep in range(repetitions):
                capacites, couts = generer_matrice_flot(n)
                t_ff = mesurer_temps_ford_fulkerson(capacites)
                t_pr = mesurer_temps_push_relabel(capacites)
                t_min = mesurer_temps_flot_min_cout(capacites, couts)
                ligne = {
                    "n": n,
                    "Ford-Fulkerson": t_ff,
                    "Push-Relabel": t_pr,
                    "Flot Min-Cout": t_min
                }
                writer.writerow(ligne)
                print(f"[{n} | {rep+1}/{repetitions}] FF: {t_ff} | PR: {t_pr} | MIN: {t_min}")

# À adapter selon ton environnement (import ou définition des fonctions)
# from ton_module import ford_fulkerson, push_relabel, executer_flot_min_cout

if __name__ == "__main__":
    tailles = [10, 20, 40, 100, 400]  # étends si tu veux : 1000, 4000, 10000
    executer_mesures(tailles, repetitions=100)
