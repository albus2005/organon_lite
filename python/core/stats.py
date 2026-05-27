# =============================
# ORGANON DATA SOLUTIONS
# core/stats.py
# Statistiques descriptives
# =============================

import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import PATHS


# =============================
# UTILITAIRES CONSOLE
# =============================

def _separateur():
    print("  " + "-" * 50)

def _titre(texte):
    print(f"\n[ {texte} ]")

def _info(label, valeur):
    print(f"  {label:<30}: {valeur}")

def _erreur(texte):
    print(f"  ERREUR — {texte}")


# =============================
# 1. DÉTECTION DES TYPES
# =============================

def detecter_types(df):
    """
    Détecte et classe les colonnes en :
    - numeriques
    - categories
    - dates
    Retourne un dict {col: type}
    """
    types = {}
    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            types[col] = "numerique"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            types[col] = "date"
        else:
            # Tente de détecter une date cachée en string
            try:
                pd.to_datetime(df[col], infer_datetime_format=True)
                types[col] = "date"
            except Exception:
                types[col] = "categorie"
    return types


# =============================
# 2. APERÇU GÉNÉRAL
# =============================

def apercu(df, types):
    """
    Affiche un aperçu général du dataset.
    """
    _titre("APERÇU GÉNÉRAL")

    print(f"  {'Variable':<22} {'Type':<14} {'N':<8} {'Manquants'}")
    _separateur()

    for col in df.columns:
        n         = df[col].count()
        manquants = df[col].isnull().sum()
        type_col  = types.get(col, "inconnu")
        print(f"  {col:<22} {type_col:<14} {n:<8} {manquants}")


# =============================
# 3. STATISTIQUES NUMÉRIQUES
# =============================

def stats_numeriques(df, types):
    """
    Calcule les statistiques descriptives
    pour toutes les colonnes numériques.
    Retourne un dict de résultats.
    """
    _titre("VARIABLES NUMÉRIQUES")

    cols_num = [col for col, t in types.items() if t == "numerique"]

    if not cols_num:
        print("  Aucune variable numérique détectée.")
        return {}

    resultats = {}

    for col in cols_num:
        serie = df[col].dropna()
        n     = len(serie)

        if n == 0:
            print(f"\n  {col} — aucune donnée valide.")
            continue

        moyenne    = round(serie.mean(), 3)
        mediane    = round(serie.median(), 3)
        ecart_type = round(serie.std(), 3)
        minimum    = round(serie.min(), 3)
        maximum    = round(serie.max(), 3)
        q1         = round(serie.quantile(0.25), 3)
        q3         = round(serie.quantile(0.75), 3)
        iqr        = round(q3 - q1, 3)
        asymetrie  = round(serie.skew(), 3)
        aplatiss   = round(serie.kurt(), 3)
        cv         = round((ecart_type / moyenne) * 100, 1) if moyenne != 0 else None

        # Détection outliers — méthode IQR
        borne_inf  = q1 - 1.5 * iqr
        borne_sup  = q3 + 1.5 * iqr
        outliers   = int(((serie < borne_inf) | (serie > borne_sup)).sum())

        resultats[col] = {
            "n":          n,
            "moyenne":    moyenne,
            "mediane":    mediane,
            "ecart_type": ecart_type,
            "min":        minimum,
            "max":        maximum,
            "q1":         q1,
            "q3":         q3,
            "iqr":        iqr,
            "asymetrie":  asymetrie,
            "aplatiss":   aplatiss,
            "cv":         cv,
            "outliers":   outliers,
        }

        # Affichage
        print(f"\n  {col.upper()}")
        _separateur()
        _info("  N valide",           n)
        _info("  Moyenne",            moyenne)
        _info("  Médiane",            mediane)
        _info("  Écart-type",         ecart_type)
        _info("  Min / Max",          f"{minimum} / {maximum}")
        _info("  Q1 / Q3",            f"{q1} / {q3}")
        _info("  IQR",                iqr)
        _info("  Asymétrie",          asymetrie)
        _info("  Aplatissement",      aplatiss)
        if cv is not None:
            _info("  Coeff. variation", f"{cv}%")
        _info("  Outliers détectés",  outliers)

        # Interprétation automatique
        print()
        print("  Interprétation :")
        if abs(asymetrie) < 0.5:
            print("    Distribution approximativement symétrique")
        elif asymetrie > 0.5:
            print("    Distribution asymétrique à droite (queue longue vers les grandes valeurs)")
        else:
            print("    Distribution asymétrique à gauche (queue longue vers les petites valeurs)")

        if outliers > 0:
            print(f"    {outliers} valeur(s) aberrante(s) détectée(s) — vérification recommandée")

    return resultats


# =============================
# 4. STATISTIQUES CATÉGORIELLES
# =============================

def stats_categories(df, types):
    """
    Calcule les fréquences et modalités
    pour toutes les colonnes catégorielles.
    Retourne un dict de résultats.
    """
    _titre("VARIABLES CATÉGORIELLES")

    cols_cat = [col for col, t in types.items() if t == "categorie"]

    if not cols_cat:
        print("  Aucune variable catégorielle détectée.")
        return {}

    resultats = {}

    for col in cols_cat:
        serie     = df[col].dropna()
        n         = len(serie)
        n_total   = len(df[col])
        manquants = n_total - n

        if n == 0:
            print(f"\n  {col} — aucune donnée valide.")
            continue

        modalites  = list(serie.unique())
        n_modalites = len(modalites)
        mode       = serie.mode()[0]
        freq       = serie.value_counts()
        freq_pct   = serie.value_counts(normalize=True) * 100

        resultats[col] = {
            "n":           n,
            "manquants":   manquants,
            "modalites":   modalites,
            "n_modalites": n_modalites,
            "mode":        mode,
            "frequences":  {
                k: {
                    "n":   int(freq[k]),
                    "pct": round(float(freq_pct[k]), 1),
                }
                for k in freq.index
            },
        }

        # Affichage
        print(f"\n  {col.upper()}")
        _separateur()
        _info("  N valide",      n)
        _info("  Manquants",     manquants)
        _info("  Modalités",     n_modalites)
        _info("  Mode",          mode)
        print()
        print(f"  {'Modalité':<22} {'N':<8} {'%'}")
        _separateur()
        for k in freq.index:
            pct = round(float(freq_pct[k]), 1)
            barre = "█" * int(pct / 5)
            print(f"  {str(k):<22} {int(freq[k]):<8} {pct}%  {barre}")

    return resultats


# =============================
# 5. STATISTIQUES CROISÉES
# =============================

def stats_croisees(df, col_ligne, col_colonne):
    """
    Tableau croisé entre deux variables catégorielles.
    Usage : stats_croisees(df, "sexe", "resultat")
    Retourne (tableau_n, tableau_pct)
    """
    _titre(f"TABLEAU CROISÉ — {col_ligne.upper()} × {col_colonne.upper()}")

    if col_ligne not in df.columns or col_colonne not in df.columns:
        _erreur(f"Colonne introuvable : {col_ligne} ou {col_colonne}")
        return None, None

    try:
        tableau_n   = pd.crosstab(df[col_ligne], df[col_colonne])
        tableau_pct = pd.crosstab(
            df[col_ligne], df[col_colonne], normalize="index"
        ) * 100
        tableau_pct = tableau_pct.round(1)

        print()
        print(f"  Effectifs :")
        print(tableau_n.to_string(index=True))
        print()
        print(f"  Pourcentages (par ligne) :")
        print(tableau_pct.to_string(index=True))

        return tableau_n, tableau_pct

    except Exception as e:
        _erreur(str(e))
        return None, None


# =============================
# 6. PIPELINE PRINCIPAL
# =============================

def analyser(df):
    """
    Pipeline complet de statistiques descriptives.
    Usage : resultats = analyser(df)
    Retourne un dict complet des résultats.
    """
    if df is None:
        _erreur("DataFrame vide — analyse impossible.")
        return None

    print()
    print("=" * 52)
    print("  ORGANON — ANALYSE STATISTIQUE DESCRIPTIVE")
    print("=" * 52)

    # Détection des types
    types = detecter_types(df)

    # Aperçu
    apercu(df, types)

    # Numériques
    res_num = stats_numeriques(df, types)

    # Catégories
    res_cat = stats_categories(df, types)

    resultats = {
        "types":      types,
        "numeriques": res_num,
        "categories": res_cat,
    }

    print()
    print("=" * 52)
    print("  [ STATS ] Analyse terminée ✓")
    print("=" * 52)
    print()

    return resultats