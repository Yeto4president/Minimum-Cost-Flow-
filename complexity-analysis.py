import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

# Créer le dossier de sortie si besoin
os.makedirs("graphique", exist_ok=True)

# Charger les données
df = pd.read_csv("temps_executions.csv")

# Mise en forme
df_melted = pd.melt(df, id_vars=["n"], var_name="Algorithme", value_name="Temps (s)")
df_melted = df_melted.rename(columns={"n": "Taille"})

# Raccourcis noms
remap = {
    "Ford-Fulkerson": "FF",
    "Push-Relabel": "PR",
    "Flot Min-Cout": "MIN"
}
df_melted["Algorithme"] = df_melted["Algorithme"].map(remap)

# Extraire max
max_times = df_melted.groupby(['Algorithme', 'Taille'])['Temps (s)'].max().reset_index()

# Fonctions de complexité
def linear(n, a, b): return a * n + b
def quadratic(n, a, b): return a * n**2 + b
def cubic(n, a, b): return a * n**3 + b
def exponential(n, a, b): return a * np.exp(b * n)
def log_polylog_fit(n, loga, b, c): return loga + b * np.log(n) + c * np.log(np.log(n))

plausible_fits = {
    'FF': {'Quadratique': quadratic, 'Cubique': cubic},
    'PR': {'Linéaire': linear, 'Quadratique': quadratic},
    'MIN': {'PolyLog': log_polylog_fit}
}

colors = {
    'Linéaire': 'green',
    'Quadratique': 'blue',
    'Cubique': 'orange',
    'Exponentielle': 'red',
    'PolyLog': 'purple'
}

algos = {'FF': "Ford-Fulkerson", 'PR': "Pousser-Réétiqueter", 'MIN': "Flot à coût minimal"}

# --- 1. Graphiques Ajustement (sans nuage global) ---
for code, name in algos.items():
    algo_data = max_times[max_times['Algorithme'] == code].sort_values('Taille')
    n_vals = algo_data['Taille'].values
    t_vals = algo_data['Temps (s)'].values

    plt.figure(figsize=(10, 6))

    if code == 'MIN':
        plt.yscale('log')
        plt.scatter(n_vals, t_vals, label="Temps max mesurés (log)", color='black', s=50)
    else:
        plt.scatter(n_vals, t_vals, label="Temps max mesurés", color='black', s=40)

    for label, func in plausible_fits[code].items():
        try:
            if label == 'PolyLog':
                log_t_vals = np.log(t_vals)
                popt, _ = curve_fit(func, n_vals, log_t_vals, p0=[1.0, 3.0, 2.0], maxfev=10000)
                fitted_vals = np.exp(func(n_vals, *popt))
            else:
                popt, _ = curve_fit(func, n_vals, t_vals, maxfev=5000)
                fitted_vals = func(n_vals, *popt)

            plt.plot(n_vals, fitted_vals, label=f"{label}", color=colors[label], linewidth=2)
        except RuntimeError:
            print(f"⚠️ Échec d'ajustement pour {name} avec {label}")
            continue

    plt.title(f"{name} — Ajustement sur max", fontsize=14)
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"graphique/{code}_ajustement_max.png")
    plt.show()

# --- 2. Graphiques Nuage vs Max (seulement ici) ---
for code, name in algos.items():
    nuage_data = df_melted[df_melted["Algorithme"] == code]
    max_data = max_times[max_times["Algorithme"] == code]

    plt.figure(figsize=(10, 6))

    if code == 'MIN':
        plt.yscale("log")
        plt.scatter(nuage_data["Taille"], nuage_data["Temps (s)"], alpha=0.4, label="Tous les points (log)", color="lightgray")
        plt.scatter(max_data["Taille"], max_data["Temps (s)"], label="Temps max mesurés (log)", color="black", s=60)
    else:
        plt.scatter(nuage_data["Taille"], nuage_data["Temps (s)"], alpha=0.4, label="Tous les points", color="lightgray")
        plt.scatter(max_data["Taille"], max_data["Temps (s)"], label="Temps max mesurés", color="black", s=60)

    plt.title(f"{name} — Nuage de points vs Maximum", fontsize=14)
    plt.xlabel("Taille du graphe (n)")
    plt.ylabel("Temps (s)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"graphique/{code}_nuage_separe_max.png")
    plt.show()

# --- 3. Ratio FF/PR ---
pivot_df = max_times.pivot(index='Taille', columns='Algorithme', values='Temps (s)')
pivot_df['Ratio_FF_PR'] = pivot_df['FF'] / pivot_df['PR']

plt.figure(figsize=(10, 6))
plt.plot(pivot_df.index, pivot_df['Ratio_FF_PR'], marker='o', linestyle='-', color='darkblue', label='θ_FF / θ_PR')
plt.xlabel('Taille du graphe (n)')
plt.ylabel('Ratio θ_FF / θ_PR')
plt.title('Comparaison de la complexité dans le pire des cas : FF vs PR')
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig("graphique/ratio_FF_PR.png")
plt.show()
