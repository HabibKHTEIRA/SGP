#!/bin/bash

# Usage: ./run_mzn.sh mon_programme.mzn [repertoire_instances] [fichier_sortie.csv]

# Vérification des paramètres
if [ $# -lt 1 ]; then
    echo "Usage: $0 <programme.mzn> [repertoire_instances] [fichier_sortie.csv]"
    exit 1
fi

PROGRAM=$1
DIR=${2:-instances}        # dossier par défaut
OUTPUT=${3:-resultats.csv} # fichier CSV par défaut
TIMEOUT_SEC=10             # temps max par instance

# Vérifie que le programme existe
if [ ! -f "$PROGRAM" ]; then
    echo "Le fichier $PROGRAM n'existe pas."
    exit 1
fi

# Initialise le fichier CSV
echo "Instance,Resultat,Temps(s)" > "$OUTPUT"

# Parcourt tous les fichiers .dzn dans le répertoire
for INSTANCE in "$DIR"/*.dzn; do
    if [ -f "$INSTANCE" ]; then
        echo "Traitement de $INSTANCE..."

        # Mesure du temps d'exécution
        START=$(date +%s.%N)

        # Exécution de MiniZinc avec timeout
        RESULT=$(timeout ${TIMEOUT_SEC}s minizinc "$PROGRAM" "$INSTANCE" 2>&1)
        STATUS=$?

        END=$(date +%s.%N)
        ELAPSED=$(echo "$END - $START" | bc)

        # Gestion du statut
        if [ $STATUS -eq 124 ]; then
            RESULT_CSV="TIMEOUT"
        elif [ $STATUS -ne 0 ]; then
            RESULT_CSV="ERREUR"
        else
            # Nettoyage du résultat pour CSV
            RESULT_CSV=$(echo "$RESULT" | tr '\n' ' ' | sed 's/ $//')
        fi

        # Ajout au CSV
        echo "$(basename "$INSTANCE"),$RESULT_CSV,$ELAPSED" >> "$OUTPUT"
    fi
done

echo "Traitement terminé. Résultats dans $OUTPUT."

