#!/bin/bash

# Usage: ./run_mzn.sh mon_programme.mzn [repertoire_instances] [fichier_sortie.csv]

if [ $# -lt 1 ]; then
    echo "Usage: $0 <programme.mzn> [repertoire_instances] [fichier_sortie.csv]"
    exit 1
fi

PROGRAM=$1
DIR=${2:-instances}
OUTPUT=${3:-resultats.csv}
TIMEOUT_SEC=100

if [ ! -f "$PROGRAM" ]; then
    echo "Le fichier $PROGRAM n'existe pas."
    exit 1
fi

# En-tête CSV avec temps avant résultat
echo "Instance,Temps(s),Resultat" > "$OUTPUT"

for INSTANCE in "$DIR"/*.dzn; do
    if [ -f "$INSTANCE" ]; then
        echo "Traitement de $INSTANCE..."

        # Mesure du temps
        START=$(date +%s.%N)
        RESULT=$(timeout ${TIMEOUT_SEC}s minizinc "$PROGRAM" "$INSTANCE" 2>&1)
        STATUS=$?
        END=$(date +%s.%N)
        ELAPSED=$(echo "$END - $START" | bc)

        # Gestion des statuts
        if [ $STATUS -eq 124 ]; then
            RESULT_CSV="TIMEOUT"
        elif [ $STATUS -ne 0 ]; then
            RESULT_CSV="ERREUR"
        else
            RESULT_CSV=$(echo "$RESULT" | tr '\n' ' ' | sed 's/ $//')
            RESULT_CSV="\"$RESULT_CSV\""
        fi

        # Ajout au CSV avec temps avant résultat
        echo "$(basename "$INSTANCE"),$ELAPSED,$RESULT_CSV" >> "$OUTPUT"
    fi
done

echo "Traitement terminé. Résultats dans $OUTPUT."

