from utils import *
from ford_fulkerson import executer_ford_fulkerson
from push_relabel import executer_push_relabel
from bellman_ford import *
from prettytable import PrettyTable

def main():
    print("=== Interface de Traitement de Réseaux ===")

    while True:
        choix = input("\n→ Sélectionnez un graphe (1 à 10), 'test' pour un graphe aléatoire, ou 'q' pour quitter : ")

        if choix.lower() == 'q':
            print("✔ Fin du programme.")
            break

        else:
            try:
                numero = int(choix)
                if 1 <= numero <= 10:
                    n, capacites, couts = lire_graphe(f"fichier_test/K5-proposition{numero}")
                    noms = get_noms_sommets(n)
                    print(f"\n📂 Graphe #{numero} chargé.")
                    afficher_matrice("Capacités", capacites, noms)

                    if est_flot_a_cout_min(numero):
                        afficher_matrice("Coûts", couts, noms)

                        # Initialisation Bellman
                        residuel = [row[:] for row in capacites]
                        couts_residuel = [row[:] for row in couts]
                        distances = [float('inf')] * n
                        parents = [-1] * n
                        distances[0] = 0
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

                        afficher_table_bellman_detaillee(noms, etapes)

                        sortie_s = sum(capacites[0])
                        entree_t = sum(capacites[i][n - 1] for i in range(n))
                        val_flot = min(sortie_s, entree_t)

                        print(f"\nCapacité sortante de s : {sortie_s}")
                        print(f"Capacité entrante vers t : {entree_t}")
                        print(f"Flot max autorisé : {val_flot}")

                        val = int(input("\n→ Entrez une valeur de flot à envoyer : "))
                        if 0 < val <= val_flot:
                            executer_flot_min_cout(capacites, couts, noms, val)
                        else:
                            print("❌ Valeur invalide.")

                    else:
                        print("\n⚙️ Choisissez l’algorithme à utiliser :")
                        print("ff - Ford-Fulkerson")
                        print("pr - Push-Relabel")
                        algo = input("→ Votre choix : ")
                        if algo == "ff":
                            executer_ford_fulkerson(capacites, noms)
                        elif algo == "pr":
                            executer_push_relabel(capacites, noms)
                        else:
                            print("❌ Choix invalide.")
                else:
                    print("❌ Numéro hors plage (1 à 10).")
            except ValueError:
                print("❌ Format invalide.")

if __name__ == "__main__":
    main()
