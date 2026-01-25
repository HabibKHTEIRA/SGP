import pandas as pd
import argparse
import matplotlib
import os
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

def generer_graphique():
    parser = argparse.ArgumentParser(description="Génère et sauvegarde un graphique de performance.")
    parser.add_argument("csv_file", help="Chemin du fichier CSV")
    args = parser.parse_args()

    # --- EXTRACTION DU NOM DU MODÈLE ET PRÉPARATION DU DOSSIER ---
    # On récupère le nom du fichier sans l'extension (ex: 'res_base')
    nom_base = os.path.splitext(os.path.basename(args.csv_file))[0]

    # Création du dossier 'graphiques' s'il n'existe pas
    dossier_sortie = "graphiques"
    if not os.path.exists(dossier_sortie):
        os.makedirs(dossier_sortie)

    chemin_sauvegarde = os.path.join(dossier_sortie, f"{nom_base}_graphe.png")

    try:
        df = pd.read_csv(args.csv_file)
        df.columns = df.columns.str.strip()

        col_nom = 'Instance'
        col_temps = 'Temps(s)'

        df[col_temps] = pd.to_numeric(df[col_temps], errors='coerce')
        df = df.dropna(subset=[col_temps])
        df = df.sort_values(by=col_nom)

    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
        return

    plt.figure(figsize=(15, 8))
    ax = plt.gca()

    # --- DESSIN DES BARRES ---
    for i, row in df.iterrows():
        nom = row[col_nom]
        temps = row[col_temps]

        if temps > 100:
            plt.bar(nom, 100, color='red', edgecolor='black', alpha=0.8)
            plt.text(nom, 101, 'TO', color='red', ha='center', va='bottom',
                     fontweight='bold', fontsize=9)
        else:
            plt.bar(nom, temps, color='royalblue', edgecolor='black')
            plt.text(nom, temps + 1, f'{temps:.2f}s', ha='center', va='bottom', fontsize=8)

    # --- MISE EN FORME ---
    plt.ylim(0, 115)
    plt.axhline(y=100, color='red', linestyle='--', alpha=0.3)
    plt.title(f"Performance : {nom_base}\n(Timeout 100s)", fontsize=14)
    plt.ylabel("Temps (secondes)")
    plt.xticks(rotation=45, ha='right', fontsize=9)

    # Couleur des labels X
    labels = ax.get_xticklabels()
    for label in labels:
        nom_inst = label.get_text()
        valeur_temps = df.loc[df[col_nom] == nom_inst, col_temps].values[0]
        if valeur_temps > 100:
            label.set_color('red')
            label.set_weight('bold')

    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.tight_layout()

    # --- SAUVEGARDE ET AFFICHAGE ---
    plt.savefig(chemin_sauvegarde)
    print(f"Graphique sauvegardé sous : {chemin_sauvegarde}")
    plt.show()

if __name__ == "__main__":
    generer_graphique()
