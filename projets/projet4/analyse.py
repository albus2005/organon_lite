# =============================
# ORGANON DATA SOLUTIONS
# projets/projet4/analyse.py
#
# Prévalence et facteurs de risque
# associés à l'HTA chez les patients
# diabétiques de type 2 — Bukavu
# Du 1er juillet 2023 au 30 septembre 2023
#
# Données : MUGALIHYA NTONDO Joël
# Mémoire de fin d'études — UOB 2023-2024
# Directeur : Prof. Dr KATCHUNGA BIANGA Philippe
# Analyse : Organon Data Solutions
# =============================

import os
import sys

# ------------------------------------------------
# On indique à Python où trouver nos outils (core/)
# ------------------------------------------------
PROJET_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(os.path.dirname(PROJET_DIR))
PYTHON_DIR = os.path.join(BASE_DIR, "python")

sys.path.insert(0, PYTHON_DIR)

# ------------------------------------------------
# Import des quatre outils principaux
# ------------------------------------------------
from core.nettoyage     import pipeline_nettoyage
from core.stats         import analyser
from core.visualisation import visualiser
from core.rendu         import pipeline_rendu

# ------------------------------------------------
# CHEMINS
# ------------------------------------------------
DATA       = os.path.join(PROJET_DIR, "data", "ntondo.csv")
GRAPHIQUES = os.path.join(PROJET_DIR, "graphiques")
RAPPORTS   = os.path.join(PROJET_DIR, "rapports")

# ------------------------------------------------
# MÉTADONNÉES
# ------------------------------------------------
META = {
    "titre": (
        "Prévalence et facteurs de risque associés à l'hypertension "
        "artérielle chez les patients diabétiques de type 2 "
        "dans la ville de Bukavu — "
        "Du 1er juillet 2023 au 30 septembre 2023"
    ),

    "auteur": (
        "MUGALIHYA NTONDO Joël — Mémoire de fin d'études\n"
        "Université Officielle de Bukavu — 2023-2024\n"
        "Directeur : Prof. Dr KATCHUNGA BIANGA Philippe\n"
        "Analyse et visualisation : Organon Data Solutions"
    ),

    "date": "2026",

    "contexte": (
        "Le diabète sucré de type 2 constitue un problème de santé publique "
        "mondial. L'hypertension artérielle (HTA) est l'un des facteurs de "
        "risque cardiovasculaire les plus fréquemment associés au diabète "
        "de type 2, augmentant significativement la morbi-mortalité. "
        "Cette étude a été menée dans les services de diabétologie des "
        "Cliniques Universitaires de Bukavu et de l'HGR de Panzi, "
        "en République Démocratique du Congo."
    ),

    "objectifs": (
        "Déterminer la prévalence de l'HTA dans un groupe de diabétiques "
        "de type 2 dans la ville de Bukavu. "
        "Analyser l'association entre l'HTA et les facteurs de risque "
        "associés — âge, IMC, tour de taille, durée du diabète, "
        "lipidogramme et insulinorésistance."
    ),

    "population": (
        "288 patients diabétiques connus ayant consulté les services de "
        "diabétologie des Cliniques Universitaires de Bukavu et de l'HGR "
        "de Panzi entre le 1er juillet et le 30 septembre 2023. "
        "Étude rétrospective, descriptive et analytique."
    ),

    "source": (
        "Dossiers médicaux des Cliniques Universitaires de Bukavu "
        "et de l'HGR de Panzi — Bukavu, RDC. "
        "Données collectées et analysées par Organon Data Solutions."
    ),

    "interpretation": (
        "La prévalence de l'HTA chez les diabétiques de type 2 à Bukavu "
        "est de 65,3% — un chiffre alarmant. Plus de la moitié des "
        "hypertendus (51,6%) ignoraient leur statut, et parmi les "
        "hypertendus connus, seulement 19,6% avaient une pression "
        "artérielle contrôlée. "
        "L'âge avancé (≥60 ans) et l'obésité abdominale (tour de taille "
        ">95 cm) sont les deux prédicteurs indépendants de l'HTA "
        "dans cette population. Ces résultats soulignent l'urgence d'un "
        "dépistage systématique de l'HTA chez tout patient diabétique "
        "et d'une prise en charge intégrée des deux pathologies."
    ),
}


# ------------------------------------------------
# PIPELINE PRINCIPAL
# ------------------------------------------------
def main():

    print()
    print("=" * 52)
    print("  ORGANON DATA SOLUTIONS")
    print("  Projet 4 — HTA chez diabétiques")
    print("  Données : MUGALIHYA NTONDO Joël")
    print("=" * 52)

    # ÉTAPE 1 — Chargement et nettoyage
    # pipeline_nettoyage() charge le CSV,
    # normalise les colonnes, supprime les doublons
    # et te propose des corrections manuelles
    df, rapport_nettoyage = pipeline_nettoyage(DATA)
    if df is None:
        print("  Arrêt — données non chargées.")
        return

    # ÉTAPE 2 — Statistiques descriptives complètes
    # analyser() calcule tout automatiquement :
    # moyenne, médiane, écart-type, fréquences, etc.
    resultats_stats = analyser(df)
    if resultats_stats is None:
        print("  Arrêt — analyse échouée.")
        return

    # ÉTAPE 3 — Visualisation interactive
    # Pour chaque variable, le programme recommande
    # des graphiques et tu choisis ceux qui conviennent
    fichiers_graphiques = visualiser(
        df,
        resultats_stats["types"],
        dossier=GRAPHIQUES,
    )

    # ÉTAPE 4 — Génération des livrables
    # PDF, Excel, Word — tu choisis le format
    pipeline_rendu(
        nom_projet          = "projet4_ntondo",
        meta                = META,
        df                  = df,
        rapport_nettoyage   = rapport_nettoyage,
        resultats_stats     = resultats_stats,
        fichiers_graphiques = fichiers_graphiques,
        dossier             = RAPPORTS,
    )

    print()
    print("=" * 52)
    print("  Projet 4 terminé.")
    print(f"  Graphiques : {GRAPHIQUES}")
    print(f"  Rapports   : {RAPPORTS}")
    print("=" * 52)
    print()


if __name__ == "__main__":
    main()