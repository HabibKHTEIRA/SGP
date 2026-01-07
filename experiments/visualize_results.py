import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import glob
import os
import sys

# Configuration
RESULTS_DIR = "resultats"
OUTPUT_BARPLOT = "benchmark_barplot.png"
OUTPUT_HEATMAP = "benchmark_heatmap.png"

def load_data():
    all_files = glob.glob(os.path.join(RESULTS_DIR, "res_*.csv"))
    
    if not all_files:
        print(f"❌ Aucun fichier CSV trouvé dans {RESULTS_DIR}")
        sys.exit(1)
        
    df_list = []
    
    for filename in all_files:
        # On déduit le nom du modèle depuis le nom du fichier (res_base.csv -> base)
        basename = os.path.basename(filename)
        model_name = basename.replace("res_", "").replace(".csv", "")
        
        try:
            # Lecture du CSV
            df = pd.read_csv(filename)
            # Ajout de la colonne Modèle
            df['Modele'] = model_name
            df_list.append(df)
        except Exception as e:
            print(f"⚠️ Erreur de lecture pour {filename}: {e}")

    if not df_list:
        print("❌ Aucune donnée valide chargée.")
        sys.exit(1)

    # Fusion de tous les dataframes
    full_df = pd.concat(df_list, ignore_index=True)
    
    # Nettoyage : Enlever l'extension .dzn des noms d'instances pour l'affichage
    full_df['Instance'] = full_df['Instance'].astype(str).str.replace('.dzn', '', regex=False)
    
    return full_df

def plot_barplot(df):
    plt.figure(figsize=(12, 6))
    sns.set_theme(style="whitegrid")
    
    # Création du barplot groupé
    chart = sns.barplot(
        data=df,
        x="Instance",
        y="Temps(s)",
        hue="Modele",
        palette="viridis",
        edgecolor="black",
        errorbar=None # On ne veut pas de barre d'erreur si une seule exécution par instance
    )
    
    plt.title("Comparaison des temps d'exécution par Modèle et Instance", fontsize=16, pad=15)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(OUTPUT_BARPLOT, dpi=300)
    print(f"✅ Graphique en barres généré : {OUTPUT_BARPLOT}")
    plt.close()

def plot_heatmap(df):
    # Pivot des données pour avoir : Index=Instance, Colonnes=Modele, Valeurs=Temps
    pivot_table = df.pivot(index="Instance", columns="Modele", values="Temps(s)")
    
    plt.figure(figsize=(10, 8))
    
    # Heatmap
    # annot=True affiche les temps dans les cases
    # cmap="YlOrRd" va du Jaune (Rapide) au Rouge (Lent/Timeout)
    sns.heatmap(
        pivot_table, 
        annot=True, 
        fmt=".2f", 
        cmap="YlOrRd", 
        linewidths=.5,
        cbar_kws={'label': 'Temps (s)'}
    )
    
    plt.title("Heatmap de Performance (Temps en secondes)", fontsize=16, pad=15)
    plt.tight_layout()
    plt.savefig(OUTPUT_HEATMAP, dpi=300)
    print(f"✅ Heatmap générée : {OUTPUT_HEATMAP}")
    plt.close()

if __name__ == "__main__":
    print("🔄 Chargement des données...")
    df = load_data()
    
    # Affichage d'un aperçu
    print(f"   Données chargées : {len(df)} lignes.")
    
    print("📊 Génération des graphiques...")
    plot_barplot(df)
    plot_heatmap(df)