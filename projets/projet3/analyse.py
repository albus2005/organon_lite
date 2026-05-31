# =============================
# ORGANON DATA SOLUTIONS
# projets/projet3/analyse.py
#
# Étude épidémiologique et clinique
# de la prééclampsie — HGR de Panzi
# Janvier 2023 — Décembre 2024
#
# Données : BANENE MWAMINI Divine
# Mémoire de fin d'études — UOB 2023-2024
# Directeur : CT Dr Philémon MATABISHI
# Analyse : Organon Data Solutions
# =============================

import os
import sys

# ------------------------------------------------
# On indique à Python où trouver nos outils (core/)
# PROJET_DIR = dossier de ce fichier (projets/projet3/)
# BASE_DIR   = racine du projet (organon_lite/)
# PYTHON_DIR = dossier python/ qui contient core/
# ------------------------------------------------
PROJET_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR   = os.path.dirname(os.path.dirname(PROJET_DIR))
PYTHON_DIR = os.path.join(BASE_DIR, "python")

# On ajoute python/ au chemin de recherche de Python
# Sans ça, "from core.nettoyage import ..." échoue
sys.path.insert(0, PYTHON_DIR)

# ------------------------------------------------
# On importe nos quatre outils principaux :
# - pipeline_nettoyage : charge et nettoie les données
# - analyser           : calcule toutes les statistiques
# - visualiser         : produit les graphiques
# - pipeline_rendu     : génère PDF, Excel, Word
# ------------------------------------------------
from core.nettoyage     import pipeline_nettoyage
from core.stats         import analyser
from core.visualisation import visualiser
from core.rendu         import pipeline_rendu

# ------------------------------------------------
# CHEMINS — où se trouvent les fichiers
# DATA       : le CSV des 94 patientes
# GRAPHIQUES : dossier où on sauvegarde les PNG
# RAPPORTS   : dossier où on sauvegarde PDF/Excel/Word
# ------------------------------------------------
DATA       = os.path.join(PROJET_DIR, "data", "divine.csv")
GRAPHIQUES = os.path.join(PROJET_DIR, "graphiques")
RAPPORTS   = os.path.join(PROJET_DIR, "rapports")

# ------------------------------------------------
# MÉTADONNÉES — informations sur l'étude
# Ce dictionnaire sera utilisé pour générer
# automatiquement la page de garde et le contexte
# du rapport PDF, Excel et Word
# ------------------------------------------------
META = {
    # Titre complet de l'étude
    "titre": (
        "Étude épidémiologique et clinique de la prééclampsie : "
        "cas spécifique de l'HGR de Panzi "
        "du 1er janvier 2023 au 31 décembre 2024"
    ),

    # Auteur original des données + mention Organon
    "auteur": (
        "BANENE MWAMINI Divine — Mémoire de fin d'études\n"
        "Université Officielle de Bukavu — 2023-2024\n"
        "Directeur : CT Dr Philémon MATABISHI — Gynécologue-obstétricien\n"
        "Analyse et visualisation : Organon Data Solutions"
    ),

    # Date de l'analyse
    "date": "2026",

    # Contexte de l'étude — paragraphe introductif du rapport
    "contexte": (
        "La prééclampsie est une complication hypertensive spécifique à la "
        "grossesse, caractérisée par une pression artérielle systolique "
        "supérieure ou égale à 140 mmHg et/ou une pression artérielle "
        "diastolique supérieure ou égale à 90 mmHg, associée à une "
        "protéinurie apparaissant à partir de la 20e semaine d'aménorrhée. "
        "Elle représente une cause majeure de morbi-mortalité maternelle "
        "et néonatale, particulièrement dans les pays à revenu faible. "
        "Cette étude a été menée à l'Hôpital Général de Référence de Panzi "
        "à Bukavu, en République Démocratique du Congo."
    ),

    # Objectifs de l'étude
    "objectifs": (
        "Déterminer la prévalence ainsi que les facteurs de risque de la "
        "prééclampsie à l'HGR de Panzi. "
        "Identifier les complications materno-fœtales les plus fréquentes. "
        "Décrire les modalités de prise en charge disponibles. "
        "Analyser les signes cliniques et paracliniques à l'admission."
    ),

    # Population étudiée
    "population": (
        "94 patientes ayant développé une prééclampsie parmi 5 830 femmes "
        "enceintes admises et ayant accouché à la maternité de l'HGR de Panzi "
        "entre janvier 2023 et décembre 2024. "
        "Critères d'inclusion : PA ≥ 140/90 mmHg associée à une protéinurie "
        "à partir de 20 SA. Étude rétrospective, descriptive et analytique."
    ),

    # Source des données
    "source": (
        "Dossiers médicaux, registres d'accouchement et carnets de "
        "consultations prénatales de l'HGR de Panzi — Bukavu, RDC. "
        "Données collectées via KoboCollect. "
        "Reconstruction et analyse réalisées par Organon Data Solutions."
    ),

    # Interprétation générale — complète l'interprétation automatique
    "interpretation": (
        "Cette étude confirme la prévalence élevée et la sévérité de la "
        "prééclampsie à l'HGR de Panzi. Les primigestes et primipares "
        "sont les plus touchées, principalement dans la tranche 20-35 ans. "
        "L'éclampsie (29,7%), l'hématome rétroplacentaire (10,6%) et le "
        "syndrome HELLP (8,5%) constituent les complications maternelles "
        "les plus fréquentes. Le taux de mortalité néonatale atteint 37,2%, "
        "reflétant les insuffisances du suivi prénatal — 73,4% des patientes "
        "ayant effectué moins de 4 consultations. Le pronostic maternel reste "
        "favorable dans 96,8% des cas grâce à l'utilisation de la nicardipine "
        "(91,4%) et du sulfate de magnésium (80,85%)."
    ),
}


# ------------------------------------------------
# FONCTION PRINCIPALE
# Elle orchestre les 4 étapes du pipeline :
# 1. Nettoyage
# 2. Analyse statistique
# 3. Visualisation
# 4. Rendu des livrables
# ------------------------------------------------
def main():

    # Affichage du titre en console
    print()
    print("=" * 52)
    print("  ORGANON DATA SOLUTIONS")
    print("  Projet 3 — Prééclampsie HGR Panzi")
    print("  Données : BANENE MWAMINI Divine")
    print("=" * 52)

    # ----
    # ÉTAPE 1 : NETTOYAGE
    # pipeline_nettoyage() charge le CSV, normalise
    # les colonnes, supprime les doublons et les
    # lignes vides, puis te propose des corrections
    # manuelles si nécessaire.
    # df      = le tableau de données nettoyé
    # rapport = un résumé du nettoyage (nb lignes, etc.)
    # ----
    df, rapport_nettoyage = pipeline_nettoyage(DATA)

    # Si le chargement a échoué on arrête tout
    if df is None:
        print("  Arrêt — données non chargées.")
        return

    # ----
    # ÉTAPE 2 : ANALYSE STATISTIQUE
    # analyser() détecte automatiquement les types
    # de colonnes (numérique, catégorie) et calcule :
    # - Pour les numériques : moyenne, médiane,
    #   écart-type, min, max, Q1, Q3, IQR,
    #   asymétrie, aplatissement, outliers
    # - Pour les catégories : fréquences, mode,
    #   pourcentages, barres ASCII en console
    # resultats = dict complet de tous les résultats
    # ----
    resultats_stats = analyser(df)

    # Si l'analyse a échoué on arrête
    if resultats_stats is None:
        print("  Arrêt — analyse échouée.")
        return

    # ----
    # ÉTAPE 3 : VISUALISATION
    # visualiser() affiche pour chaque variable
    # les graphiques recommandés et te laisse choisir.
    # Les PNG sont sauvegardés dans GRAPHIQUES/.
    # fichiers_graphiques = liste des chemins PNG produits
    # ----
    fichiers_graphiques = visualiser(
        df,                        # le tableau nettoyé
        resultats_stats["types"],  # types de colonnes détectés
        dossier=GRAPHIQUES,        # où sauvegarder les PNG
    )

    # ----
    # ÉTAPE 4 : RENDU DES LIVRABLES
    # pipeline_rendu() te demande quel format tu veux :
    # 1. PDF  — rapport complet avec page de garde,
    #           tableaux, graphiques, interprétation
    # 2. Excel — données nettoyées + stats en feuilles
    # 3. Word  — rapport éditable même structure que PDF
    # 4. Tout  — les trois formats d'un coup
    # ----
    pipeline_rendu(
        nom_projet          = "projet3_divine",
        meta                = META,
        df                  = df,
        rapport_nettoyage   = rapport_nettoyage,
        resultats_stats     = resultats_stats,
        fichiers_graphiques = fichiers_graphiques,
        dossier             = RAPPORTS,
    )

    # Résumé final en console
    print()
    print("=" * 52)
    print("  Projet 3 terminé.")
    print(f"  Graphiques : {GRAPHIQUES}")
    print(f"  Rapports   : {RAPPORTS}")
    print("=" * 52)
    print()


# ------------------------------------------------
# Point d'entrée du script
# Cette condition garantit que main() ne s'exécute
# que si on lance ce fichier directement :
#   python projets/projet3/analyse.py
# Et pas si on l'importe depuis un autre fichier.
# ------------------------------------------------
if __name__ == "__main__":
    main()