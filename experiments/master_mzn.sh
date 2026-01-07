#!/bin/bash

# ============================================================
# MASTER RUNNER - Social Golfer Problem Benchmark
# ============================================================

# Configuration
RUNNER="./run_mzn.sh"
MODELS_DIR="../modeles"
INSTANCES_DIR="instances"
RESULTS_DIR="resultats"

# Vérifications préliminaires
if [ ! -f "$RUNNER" ]; then
    echo "❌ Erreur : Le script $RUNNER est introuvable."
    exit 1
fi

if [ ! -d "$MODELS_DIR" ]; then
    echo "❌ Erreur : Le dossier $MODELS_DIR n'existe pas."
    exit 1
fi

# Création du dossier de résultats
mkdir -p "$RESULTS_DIR"

# Rendre le runner exécutable au cas où
chmod +x "$RUNNER"

echo "🚀 Démarrage de la campagne de tests sur les modèles..."
echo "-----------------------------------------------------"

# Boucle sur tous les fichiers .mzn du dossier modeles
# shopt -s nullglob permet d'éviter les erreurs si le dossier est vide
shopt -s nullglob
for model_path in "$MODELS_DIR"/*.mzn; do
    # Extraction du nom du fichier sans chemin (ex: base.mzn)
    model_filename=$(basename "$model_path")
    # Nom du modèle sans extension (ex: base) pour le fichier CSV
    model_name="${model_filename%.*}"
    
    csv_output="$RESULTS_DIR/res_${model_name}.csv"
    
    echo "👉 Test du modèle : $model_name"
    
    # Appel de ton script run_mzn.sh
    # Usage: ./run_mzn.sh <programme.mzn> [repertoire_instances] [fichier_sortie.csv]
    "$RUNNER" "$model_path" "$INSTANCES_DIR" "$csv_output"
    
    echo "✅ Résultats sauvegardés dans $csv_output"
    echo "-----------------------------------------------------"
done

echo "💾 Tous les benchmarks sont terminés."

# Lancement de la génération des graphiques
if [ -f "visualize_results.py" ]; then
    echo "📊 Génération des graphiques et heatmaps..."
    python3 visualize_results.py
else
    echo "⚠️ Le script python 'visualize_results.py' est manquant. Pas de graphiques générés."
fi

echo "✨ Terminé !"