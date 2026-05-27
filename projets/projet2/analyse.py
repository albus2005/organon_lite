# =============================
# ORGANON DATA SOLUTIONS
# projets/projet2/analyse.py
# Décollement de la rétine
# CELPA Bukavu — 2018-2024
# =============================

import os
import sys

PROJET_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(os.path.dirname(PROJET_DIR))
PYTHON_DIR = os.path.join(BASE_DIR, "python")

sys.path.insert(0, PYTHON_DIR)

from core.nettoyage     import pipeline_nettoyage
from core.stats         import analyser
from core.visualisation import visualiser
from core.rendu         import pipeline_rendu

DATA       = os.path.join(PROJET_DIR, "data", "kachunga.csv")
GRAPHIQUES = os.path.join(PROJET_DIR, "graphiques")
RAPPORTS   = os.path.join(PROJET_DIR, "rapports")

META = {
    "titre": (
        "Aspects épidémiologiques, étiologiques, cliniques et thérapeutiques "
        "du décollement de la rétine à la clinique ophtalmologique CELPA Bukavu "
        "— 2018 à 2024"
    ),
    "auteur":  "KACHUNGA MULUMBILWA Daniel — Analyse : Organon Data Solutions",
    "date":    "2026",
    "contexte": (
        "Le décollement de la rétine (DR) est une urgence ophtalmologique "
        "pouvant conduire à la cécité définitive en l'absence de prise en "
        "charge rapide. En République Démocratique du Congo, les données "
        "épidémiologiques sur cette pathologie demeurent rares. Cette étude "
        "a été menée à la clinique ophtalmologique CELPA de Bukavu sur une "
        "période de sept ans, du 1er janvier 2018 au 31 décembre 2024."
    ),
    "objectifs": (
        "Décrire les aspects épidémiologiques, étiologiques, cliniques et "
        "thérapeutiques du décollement de la rétine dans notre milieu. "
        "Déterminer la fréquence, les facteurs de risque, les moyens "
        "diagnostiques disponibles et les modalités de prise en charge."
    ),
    "population": (
        "49 patients diagnostiqués avec un décollement de la rétine à la "
        "clinique ophtalmologique CELPA de Bukavu entre 2018 et 2024. "
        "Étude rétrospective, descriptive et analytique."
    ),
    "source": (
        "Dossiers médicaux de la clinique ophtalmologique CELPA Bukavu. "
        "Données collectées via Kobocollect et analysées par "
        "Organon Data Solutions."
    ),
    "interpretation": (
        "Le décollement de la rétine représente 3,5% des pathologies "
        "rétiniennes enregistrées à la CELPA. La prédominance masculine "
        "(71,4%) et la jeunesse des patients (36,7% entre 16 et 30 ans) "
        "s'expliquent par une exposition plus fréquente aux traumatismes "
        "oculaires dans cette population. "
        "Le traumatisme constitue la principale étiologie (59,2%), "
        "confirmant les données africaines sur le sujet. "
        "L'évolution défavorable dans 81,6% des cas reflète les "
        "limitations diagnostiques et thérapeutiques de notre milieu."
    ),
}


def main():
    print()
    print("=" * 52)
    print("  ORGANON DATA SOLUTIONS")
    print("  Projet 2 — Décollement de la rétine")
    print("  CELPA Bukavu — 2018-2024")
    print("=" * 52)

    df, rapport_nettoyage = pipeline_nettoyage(DATA)
    if df is None:
        print("  Arrêt — données non chargées.")
        return

    resultats_stats = analyser(df)
    if resultats_stats is None:
        print("  Arrêt — analyse échouée.")
        return

    fichiers_graphiques = visualiser(
        df,
        resultats_stats["types"],
        dossier=GRAPHIQUES,
    )

    pipeline_rendu(
        nom_projet          = "projet2_kachunga",
        meta                = META,
        df                  = df,
        rapport_nettoyage   = rapport_nettoyage,
        resultats_stats     = resultats_stats,
        fichiers_graphiques = fichiers_graphiques,
        dossier             = RAPPORTS,
    )

    print()
    print("=" * 52)
    print("  Projet 2 terminé.")
    print(f"  Graphiques : {GRAPHIQUES}")
    print(f"  Rapports   : {RAPPORTS}")
    print("=" * 52)
    print()


if __name__ == "__main__":
    main()