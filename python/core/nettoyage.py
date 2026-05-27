# =============================
# ORGANON DATA SOLUTIONS
# core/nettoyage.py
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
    print("  " + "-" * 42)

def _titre(texte):
    print(f"\n[ {texte} ]")

def _info(label, valeur):
    print(f"  {label:<30}: {valeur}")

def _erreur(texte):
    print(f"  ERREUR — {texte}")

def _ok(texte):
    print(f"  {texte} ✓")


# =============================
# LOADERS
# =============================

def _charger_csv(chemin):
    try:
        try:
            df = pd.read_csv(chemin, encoding="utf-8")
            _info("Encodage", "utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(chemin, encoding="latin-1")
            _info("Encodage", "latin-1")
        return df
    except Exception as e:
        _erreur(str(e))
        return None


def _charger_excel(chemin):
    try:
        df = pd.read_excel(chemin)
        _info("Encodage", "utf-8")
        return df
    except Exception as e:
        _erreur(str(e))
        return None


# Registre des loaders — extensible
LOADERS = {
    ".csv":  _charger_csv,
    ".xlsx": _charger_excel,
    ".xls":  _charger_excel,
}


def enregistrer_loader(extension, fonction):
    """
    Enregistre un nouveau loader de format.
    Usage : enregistrer_loader(".json", ma_fonction_json)
    """
    LOADERS[extension.lower()] = fonction
    _ok(f"Loader enregistré : {extension}")


# =============================
# CHARGEMENT
# =============================

def charger(chemin):
    """
    Charge un fichier selon son extension.
    Utilise le registre LOADERS.
    Usage : df = charger("python/projets/p1/data/projet1.csv")
    Retourne un DataFrame ou None si erreur.
    """
    _titre("CHARGEMENT")

    if not os.path.exists(chemin):
        _erreur(f"Fichier introuvable : {chemin}")
        return None

    extension = os.path.splitext(chemin)[1].lower()

    if extension not in LOADERS:
        _erreur(f"Format non supporté : {extension}")
        _info("Formats disponibles", str(list(LOADERS.keys())))
        return None

    _info("Fichier", os.path.basename(chemin))
    _info("Format détecté", extension)

    df = LOADERS[extension](chemin)

    if df is None:
        return None

    _info("Lignes", df.shape[0])
    _info("Colonnes", df.shape[1])

    return df


# =============================
# NETTOYAGE AUTOMATIQUE
# =============================

def _normaliser_colonnes(df):
    """Normalise les noms de colonnes."""
    remplacements = {
        "é": "e", "è": "e", "ê": "e", "ë": "e",
        "à": "a", "â": "a", "ä": "a",
        "ô": "o", "ö": "o",
        "î": "i", "ï": "i",
        "ù": "u", "û": "u", "ü": "u",
        "ç": "c",
    }
    cols = df.columns.str.strip().str.lower()
    for accent, remplacement in remplacements.items():
        cols = cols.str.replace(accent, remplacement, regex=False)
    cols = cols.str.replace(r"\s+", "_", regex=True)
    cols = cols.str.replace(r"[^\w]", "_", regex=True)
    df.columns = cols
    return df


def nettoyer_auto(df):
    """
    Nettoyage automatique sans intervention.
    Retourne (df_nettoyé, rapport)
    """
    _titre("NETTOYAGE AUTO")

    if df is None:
        _erreur("DataFrame vide — nettoyage impossible.")
        return None, None

    rapport = {}
    rapport["lignes_avant"] = df.shape[0]
    rapport["colonnes_avant"] = list(df.columns)

    # Normalisation colonnes
    df = _normaliser_colonnes(df)
    rapport["colonnes_apres"] = list(df.columns)

    # Doublons
    doublons = int(df.duplicated().sum())
    df = df.drop_duplicates()
    rapport["doublons_supprimes"] = doublons

    # Lignes vides
    lignes_vides = int(df.isnull().all(axis=1).sum())
    df = df.dropna(how="all")
    rapport["lignes_vides_supprimees"] = lignes_vides

    rapport["lignes_apres"] = df.shape[0]

    # Valeurs manquantes
    manquantes = df.isnull().sum()
    rapport["valeurs_manquantes"] = {
        col: int(manquantes[col])
        for col in df.columns
        if manquantes[col] > 0
    }

    # Types
    rapport["types"] = {
        col: str(df[col].dtype)
        for col in df.columns
    }

    # Affichage
    _info("Lignes chargées", rapport["lignes_avant"])
    _info("Doublons supprimés", rapport["doublons_supprimes"])
    _info("Lignes vides supprimées", rapport["lignes_vides_supprimees"])
    _info("Lignes finales", rapport["lignes_apres"])
    _separateur()

    print("  Colonnes normalisées :")
    print(f"    {', '.join(rapport['colonnes_apres'])}")
    _separateur()

    if rapport["valeurs_manquantes"]:
        print("  Valeurs manquantes :")
        for col, n in rapport["valeurs_manquantes"].items():
            pct = round(n / rapport["lignes_apres"] * 100, 1)
            print(f"    - {col:<22}: {n} ({pct}%)")
    else:
        _info("Valeurs manquantes", "aucune")
    _separateur()

    print("  Types détectés :")
    for col, dtype in rapport["types"].items():
        print(f"    - {col:<22}: {dtype}")

    print(f"\n[ NETTOYAGE AUTO ] Terminé ✓")

    return df, rapport


# =============================
# MENU MANUEL
# =============================

def _menu_manuel():
    """
    Affiche le menu et retourne la liste
    des options choisies.
    Permet de choisir plusieurs options.
    """
    print()
    print("=" * 44)
    print("  [ ACTION REQUISE ] Modifications manuelles")
    print("  Choisissez une ou plusieurs options")
    print("  Séparez par des virgules  ex: 1,3")
    print("-" * 44)
    print("  1. Corriger les types de colonnes")
    print("  2. Standardiser les valeurs texte")
    print("  3. Remplacer les valeurs manquantes")
    print("  4. Supprimer des colonnes")
    print("  5. Renommer des colonnes")
    print("  6. Continuer sans modifications")
    print("=" * 44)

    choix_raw = input("  Votre choix : ").strip()

    if not choix_raw or choix_raw == "6":
        return []

    choix = []
    for c in choix_raw.split(","):
        c = c.strip()
        if c in ["1", "2", "3", "4", "5"]:
            if int(c) not in choix:
                choix.append(int(c))
        elif c != "6":
            print(f"  Option ignorée : '{c}'")

    return choix


# =============================
# CORRECTIONS MANUELLES
# =============================

def _corriger_types(df):
    """Corrige les types de colonnes."""
    _titre("CORRECTION DES TYPES")

    print("  Colonnes disponibles :")
    for i, col in enumerate(df.columns, 1):
        print(f"    {i}. {col:<22} — type actuel : {df[col].dtype}")

    col_raw = input("\n  Colonnes à corriger (ex: 1,3) : ").strip()
    if not col_raw:
        print("  Aucune correction effectuée.")
        return df

    colonnes = []
    for c in col_raw.split(","):
        c = c.strip()
        try:
            idx = int(c) - 1
            if 0 <= idx < len(df.columns):
                colonnes.append(df.columns[idx])
            else:
                print(f"  Numéro invalide : {c}")
        except ValueError:
            print(f"  Ignoré : {c}")

    types_dispo = {
        "1": ("int",   "Entier"),
        "2": ("float", "Décimal"),
        "3": ("str",   "Texte"),
        "4": ("bool",  "Booléen"),
    }

    print()
    print("  Types disponibles :")
    print("    1. Entier    2. Décimal    3. Texte    4. Booléen")

    for col in colonnes:
        choix = input(f"  Nouveau type pour '{col}' : ").strip()
        if choix not in types_dispo:
            print(f"  Type ignoré pour '{col}'")
            continue
        type_cible, type_nom = types_dispo[choix]
        try:
            if type_cible == "int":
                df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
            elif type_cible == "float":
                df[col] = pd.to_numeric(df[col], errors="coerce")
            elif type_cible == "str":
                df[col] = df[col].astype(str)
            elif type_cible == "bool":
                df[col] = df[col].astype(bool)
            _ok(f"{col} → {type_nom}")
        except Exception as e:
            _erreur(f"{col} : {e}")

    return df


def _standardiser_texte(df):
    """Standardise les valeurs texte."""
    _titre("STANDARDISATION TEXTE")

    cols_texte = [col for col in df.columns if df[col].dtype == object]
    if not cols_texte:
        print("  Aucune colonne texte détectée.")
        return df

    print("  Colonnes texte disponibles :")
    for i, col in enumerate(cols_texte, 1):
        exemples = list(df[col].dropna().unique()[:4])
        print(f"    {i}. {col:<22} — ex: {exemples}")

    col_raw = input("\n  Colonnes à standardiser (ex: 1,2) : ").strip()
    if not col_raw:
        print("  Aucune standardisation effectuée.")
        return df

    print()
    print("  Opérations disponibles (combinables) :")
    print("    1. Première lettre majuscule  (oui → Oui)")
    print("    2. Tout en majuscules         (oui → OUI)")
    print("    3. Tout en minuscules         (OUI → oui)")
    print("    4. Supprimer espaces inutiles")

    ops_raw = input("  Opérations (ex: 1,4) : ").strip()
    ops = [
        o.strip()
        for o in ops_raw.split(",")
        if o.strip() in ["1", "2", "3", "4"]
    ]

    # Validation — 1,2,3 s'excluent
    casse = [o for o in ops if o in ["1", "2", "3"]]
    if len(casse) > 1:
        print(f"  Attention — options de casse incompatibles. On garde : {casse[0]}")
        ops = [o for o in ops if o not in casse[1:]]

    for c in col_raw.split(","):
        c = c.strip()
        try:
            idx = int(c) - 1
            col = cols_texte[idx]
            if "4" in ops:
                df[col] = df[col].str.strip()
            if "1" in ops:
                df[col] = df[col].str.capitalize()
            elif "2" in ops:
                df[col] = df[col].str.upper()
            elif "3" in ops:
                df[col] = df[col].str.lower()
            _ok(f"{col} standardisé")
        except IndexError:
            _erreur(f"Numéro invalide : {c}")
        except Exception as e:
            _erreur(f"{col} : {e}")

    return df


def _remplacer_manquantes(df):
    """Remplace les valeurs manquantes."""
    _titre("VALEURS MANQUANTES")

    manquantes = {
        col: int(df[col].isnull().sum())
        for col in df.columns
        if df[col].isnull().sum() > 0
    }

    if not manquantes:
        print("  Aucune valeur manquante détectée.")
        return df

    cols_manquantes = list(manquantes.keys())
    print("  Colonnes avec valeurs manquantes :")
    for i, col in enumerate(cols_manquantes, 1):
        print(f"    {i}. {col:<22} — {manquantes[col]} valeurs manquantes")

    col_raw = input("\n  Colonnes à traiter (ex: 1,2) : ").strip()
    if not col_raw:
        print("  Aucun remplacement effectué.")
        return df

    print()
    print("  Méthodes disponibles :")
    print("    1. Moyenne        (colonnes numériques)")
    print("    2. Médiane        (colonnes numériques)")
    print("    3. Mode           (toutes colonnes)")
    print("    4. Valeur fixe")
    print("    5. Supprimer les lignes concernées")

    methode = input("  Méthode : ").strip()

    for c in col_raw.split(","):
        c = c.strip()
        try:
            idx = int(c) - 1
            col = cols_manquantes[idx]
            if methode == "1":
                if not pd.api.types.is_numeric_dtype(df[col]):
                    _erreur(f"{col} n'est pas numérique")
                    continue
                val = round(df[col].mean(), 2)
                df[col] = df[col].fillna(val)
                _ok(f"{col} → moyenne ({val})")
            elif methode == "2":
                if not pd.api.types.is_numeric_dtype(df[col]):
                    _erreur(f"{col} n'est pas numérique")
                    continue
                val = round(df[col].median(), 2)
                df[col] = df[col].fillna(val)
                _ok(f"{col} → médiane ({val})")
            elif methode == "3":
                val = df[col].mode()[0]
                df[col] = df[col].fillna(val)
                _ok(f"{col} → mode ({val})")
            elif methode == "4":
                val = input(f"  Valeur pour '{col}' : ").strip()
                df[col] = df[col].fillna(val)
                _ok(f"{col} → {val}")
            elif methode == "5":
                avant = len(df)
                df = df.dropna(subset=[col])
                _ok(f"{col} → {avant - len(df)} lignes supprimées")
            else:
                _erreur(f"Méthode inconnue — '{col}' ignoré")
        except IndexError:
            _erreur(f"Numéro invalide : {c}")
        except Exception as e:
            _erreur(f"{col} : {e}")

    return df


def _supprimer_colonnes(df):
    """Supprime des colonnes."""
    _titre("SUPPRESSION DE COLONNES")

    print("  Colonnes disponibles :")
    for i, col in enumerate(df.columns, 1):
        print(f"    {i}. {col}")

    col_raw = input("\n  Colonnes à supprimer (ex: 1,3) : ").strip()
    if not col_raw:
        print("  Aucune suppression effectuée.")
        return df

    a_supprimer = []
    for c in col_raw.split(","):
        c = c.strip()
        try:
            idx = int(c) - 1
            if 0 <= idx < len(df.columns):
                a_supprimer.append(df.columns[idx])
            else:
                _erreur(f"Numéro invalide : {c}")
        except ValueError:
            _erreur(f"Ignoré : {c}")

    if a_supprimer:
        df = df.drop(columns=a_supprimer)
        _ok(f"Supprimées : {a_supprimer}")

    return df


def _renommer_colonnes(df):
    """Renomme des colonnes."""
    _titre("RENOMMER DES COLONNES")

    print("  Colonnes disponibles :")
    for i, col in enumerate(df.columns, 1):
        print(f"    {i}. {col}")

    col_raw = input("\n  Colonnes à renommer (ex: 1,3) : ").strip()
    if not col_raw:
        print("  Aucun renommage effectué.")
        return df

    renommage = {}
    for c in col_raw.split(","):
        c = c.strip()
        try:
            idx = int(c) - 1
            col = df.columns[idx]
            nouveau = input(f"  Nouveau nom pour '{col}' : ").strip()
            if nouveau:
                renommage[col] = nouveau
            else:
                print(f"  Nom vide — '{col}' ignoré")
        except IndexError:
            _erreur(f"Numéro invalide : {c}")
        except Exception as e:
            _erreur(str(e))

    if renommage:
        df = df.rename(columns=renommage)
        _ok("Renommage effectué")

    return df


# =============================
# PIPELINE PRINCIPAL
# =============================

OPERATIONS = {
    1: ("Corriger les types",         _corriger_types),
    2: ("Standardiser le texte",      _standardiser_texte),
    3: ("Remplacer les manquantes",   _remplacer_manquantes),
    4: ("Supprimer des colonnes",     _supprimer_colonnes),
    5: ("Renommer des colonnes",      _renommer_colonnes),
}


def pipeline_nettoyage(chemin):
    """
    Pipeline complet de nettoyage.
    Usage : df, rapport = pipeline_nettoyage("chemin/fichier.csv")

    Étapes :
      1. Chargement
      2. Nettoyage automatique
      3. Menu modifications manuelles
      4. Retourne df propre + rapport
    """
    # Chargement
    df = charger(chemin)
    if df is None:
        return None, None

    # Nettoyage auto
    df, rapport = nettoyer_auto(df)
    if df is None:
        return None, None

    # Menu manuel
    choix = _menu_manuel()

    if not choix:
        print("\n  Aucune modification manuelle.")
    else:
        for op in choix:
            if op in OPERATIONS:
                nom, fonction = OPERATIONS[op]
                df = fonction(df)
                if df is None:
                    _erreur(f"Opération échouée : {nom}")
                    return None, rapport

    # Rapport final
    rapport["lignes_finales"]   = len(df)
    rapport["colonnes_finales"] = list(df.columns)

    print()
    print("=" * 44)
    print("  [ PIPELINE ] Nettoyage terminé ✓")
    _info("  Lignes finales",   rapport["lignes_finales"])
    _info("  Colonnes finales", len(rapport["colonnes_finales"]))
    print("=" * 44)
    print()

    return df, rapport