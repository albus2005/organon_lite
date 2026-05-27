# =============================
# ORGANON DATA SOLUTIONS
# projets/projet1/analyse.py
# Paludisme — Enfants < 5 ans — Bukavu
# =============================
import os
import sys

# Racine du projet
PROJET_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(os.path.dirname(PROJET_DIR))
PYTHON_DIR = os.path.join(BASE_DIR, "python")

# Accès au core
sys.path.insert(0, PYTHON_DIR)

from core.nettoyage     import pipeline_nettoyage
from core.stats         import analyser
from core.visualisation import visualiser
from core.rendu         import pipeline_rendu

# =============================
# CHEMINS
# =============================

DATA       = os.path.join(PYTHON_DIR, "data", "projet1.csv")
GRAPHIQUES = os.path.join(PROJET_DIR, "graphiques")
RAPPORTS   = os.path.join(PROJET_DIR, "rapports")

# =============================
# MÉTADONNÉES DU PROJET
# =============================

META = {
    "titre": (
        "Prévalence du paludisme chez les enfants "
        "de moins de 5 ans à Bukavu"
    ),
    "auteur":      "Organon Data Solutions",
    "date":        "2026",
    "contexte": (
        "Le paludisme constitue l'une des principales causes de mortalité "
        "infantile en République Démocratique du Congo. Cette étude analyse "
        "sa prévalence chez les enfants de moins de 5 ans dans trois "
        "quartiers de Bukavu : Bagira, Kadutu et Ibanda."
    ),
    "objectifs": (
        "Estimer la prévalence du paludisme dans la population pédiatrique "
        "de Bukavu. Identifier les facteurs associés — quartier de résidence, "
        "sexe, taux d'hémoglobine. Décrire le profil clinique des cas positifs."
    ),
    "population": (
        "Enfants âgés de 6 à 59 mois consultés dans les centres de santé "
        "des quartiers Bagira, Kadutu et Ibanda, Bukavu — RDC."
    ),
    "source": (
        "Données collectées par Organon Data Solutions. "
        "Test de diagnostic rapide (TDR) utilisé comme critère de confirmation. "
        "Taille de l'échantillon : 30 patients."
    ),
    "interpretation": (
        "Ces résultats confirment une charge palustre élevée dans la "
        "population pédiatrique de Bukavu, cohérente avec les données "
        "épidémiologiques de la région des Grands Lacs. "
        "Une attention particulière devrait être portée au quartier de Bagira "
        "qui concentre le plus grand nombre de cas positifs."
    ),
}

# =============================
# PIPELINE
# =============================

def main():

    print()
    print("=" * 52)
    print("  ORGANON DATA SOLUTIONS")
    print("  Projet 1 — Paludisme Bukavu")
    print("=" * 52)

    # 1. Nettoyage
    df, rapport_nettoyage = pipeline_nettoyage(DATA)
    if df is None:
        print("  Arrêt — données non chargées.")
        return

    # 2. Statistiques
    resultats_stats = analyser(df)
    if resultats_stats is None:
        print("  Arrêt — analyse échouée.")
        return

    # 3. Visualisation
    fichiers_graphiques = visualiser(
        df,
        resultats_stats["types"],
        dossier=GRAPHIQUES,
    )

    # 4. Rendu
    pipeline_rendu(
        nom_projet          = "projet1",
        meta                = META,
        df                  = df,
        rapport_nettoyage   = rapport_nettoyage,
        resultats_stats     = resultats_stats,
        fichiers_graphiques = fichiers_graphiques,
        dossier             = RAPPORTS,
    )

    print()
    print("=" * 52)
    print("  Projet 1 terminé.")
    print(f"  Graphiques : {GRAPHIQUES}")
    print(f"  Rapports   : {RAPPORTS}")
    print("=" * 52)
    print()


if __name__ == "__main__":
    main()