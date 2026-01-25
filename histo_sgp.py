import pandas as pd
import argparse
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def generer_graphique():
    parser = argparse.ArgumentParser(description="Graphique des temps avec détection de timeout (>100s).")
    parser.add_argument("csv_file", help="Chemin du fichier CSV")
    args = parser.parse_args()

    try:
        df = pd.read_csv(args.csv_file)
        df.columns = df.columns.str.strip()

        col_nom = 'Instance'
        col_temps = 'Temps(s)'

        df[col_temps] = pd.to_numeric(df[col_temps], errors='coerce')
        df = df.dropna(subset=[col_temps])
        df = df.sort_values(by=col_nom)

        # --- LOGIQUE DE FILTRAGE ET COULEURS ---
        couleurs_barres = []
        indices_trop_longs = []

        # On crée une copie pour ne pas corrompre les données originales si besoin
        temps_a_afficher = []

        for i, row in df.iterrows():
            if row[col_temps] > 100:
                temps_a_afficher.append(0)    # Barre à 0
                couleurs_barres.append('red') # (Optionnel car barre invisible)
                indices_trop_longs.append(row[col_nom])
            else:
                temps_a_afficher.append(row[col_temps])
                couleurs_barres.append('royalblue')

    except Exception as e:
        print(f"Erreur : {e}")
        return

    # --- CRÉATION DU GRAPHIQUE ---
    plt.figure(figsize=(14, 8))

    # On utilise temps_a_afficher (avec les 0 pour les > 100s)
    bars = plt.bar(df[col_nom], temps_a_afficher, color=couleurs_barres, edgecolor='black')

    plt.title(f"Temps d'exécution par Instance (Rouge = Timeout > 100s)", fontsize=14)
    plt.ylabel("Temps (secondes)")

    # Rotation des noms
    ax = plt.gca()
    plt.xticks(rotation=45, ha='right', fontsize=9)

    # --- MISE EN ROUGE DES LABELS ---
    # On récupère les étiquettes générées par matplotlib
    labels = ax.get_xticklabels()
    for label in labels:
        if label.get_text() in indices_trop_longs:
            label.set_color('red')
            label.set_weight('bold') # Un peu de gras pour que ça ressorte

    plt.grid(axis='y', linestyle='--', alpha=0.6)
    plt.tight_layout()

    print(f"Affichage : {len(indices_trop_longs)} instance(s) trop longue(s) détectée(s).")
    plt.show()

if __name__ == "__main__":
    generer_graphique()
