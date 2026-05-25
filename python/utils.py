# =============================
# ORGANON DATA SOLUTIONS
# Fonctions utilitaires
# =============================

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from config import COLORS, LAYOUT, PATHS, FONTS, ORGANON_SIGNATURE
import os


# =============================
# 1. CHARGEMENT DES DONNÉES
# =============================

def charger_csv(nom_fichier):
    """
    Charge un CSV depuis le dossier data/
    Usage : df = charger_csv("projet1.csv")
    """
    chemin = os.path.join(PATHS["data"], nom_fichier)
    try:
        df = pd.read_csv(chemin, encoding="utf-8")
        print(f"✓ {nom_fichier} chargé — {df.shape[0]} lignes, {df.shape[1]} colonnes")
        return df
    except FileNotFoundError:
        print(f"✗ Fichier introuvable : {chemin}")
        return None
    except Exception as e:
        print(f"✗ Erreur : {e}")
        return None


# =============================
# 2. NETTOYAGE DE BASE
# =============================

def nettoyer(df):
    """
    Nettoyage standard :
    - Supprime les doublons
    - Supprime les lignes entièrement vides
    - Normalise les noms de colonnes
    Retourne le df nettoyé + un rapport
    """
    rapport = {}

    rapport["lignes_avant"] = df.shape[0]
    rapport["doublons"]     = df.duplicated().sum()

    df = df.drop_duplicates()
    df = df.dropna(how="all")

    # Normalise les colonnes — minuscules, sans espaces
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("é", "e")
        .str.replace("è", "e")
        .str.replace("ê", "e")
        .str.replace("à", "a")
        .str.replace("ô", "o")
    )

    rapport["lignes_apres"] = df.shape[0]
    rapport["colonnes"]     = list(df.columns)

    print(f"✓ Nettoyage terminé")
    print(f"  Lignes avant  : {rapport['lignes_avant']}")
    print(f"  Doublons supprimés : {rapport['doublons']}")
    print(f"  Lignes après  : {rapport['lignes_apres']}")
    print(f"  Colonnes      : {rapport['colonnes']}")

    return df, rapport


# =============================
# 3. APPLIQUER LE STYLE GLOBAL
# =============================

def appliquer_style(fig, titre):
    """
    Applique la charte graphique Organon à une figure Plotly.
    Ajoute le titre et la signature.
    Usage : fig = appliquer_style(fig, "Mon graphique")
    """
    fig.update_layout(
        **LAYOUT,
        title_text=titre,
        xaxis=dict(
            gridcolor="#E5E7EB",
            linecolor="#E5E7EB",
            tickfont=dict(size=FONTS["label_size"]),
        ),
        yaxis=dict(
            gridcolor="#E5E7EB",
            linecolor="#E5E7EB",
            tickfont=dict(size=FONTS["label_size"]),
        ),
    )

    # Signature en bas du graphique
    fig.add_annotation(
        text=ORGANON_SIGNATURE,
        xref="paper", yref="paper",
        x=1, y=-0.12,
        showarrow=False,
        font=dict(
            size=9,
            color=COLORS["primary"],
            family=FONTS["family"],
        ),
        xanchor="right",
    )

    return fig


# =============================
# 4. EXPORTER LE GRAPHIQUE
# =============================

def exporter(fig, nom_fichier):
    """
    Exporte la figure en HTML dans graphiques/
    Usage : exporter(fig, "graph1.html")
    """
    os.makedirs(PATHS["graphiques"], exist_ok=True)
    chemin = os.path.join(PATHS["graphiques"], nom_fichier)
    fig.write_html(
        chemin,
        include_plotlyjs="cdn",
        full_html=True,
    )
    print(f"✓ Graphique exporté : {chemin}")


# =============================
# 5. RÉSUMÉ STATISTIQUE
# =============================

def resume(df):
    """
    Affiche un résumé statistique rapide du dataframe.
    Usage : resume(df)
    """
    print("\n=== RÉSUMÉ STATISTIQUE ===")
    print(f"Dimensions : {df.shape[0]} lignes × {df.shape[1]} colonnes")
    print(f"\nTypes de colonnes :\n{df.dtypes}")
    print(f"\nValeurs manquantes :\n{df.isnull().sum()}")
    print(f"\nStatistiques :\n{df.describe()}")
    print("==========================\n")
    
    # =============================
# 6. EXPORTER EN PNG
# =============================

def exporter_png(fig, nom_fichier):
    """
    Exporte la figure en PNG dans graphiques/
    Usage : exporter_png(fig, "graph1a.png")
    """
    os.makedirs(PATHS["graphiques"], exist_ok=True)
    chemin = os.path.join(PATHS["graphiques"], nom_fichier)
    fig.write_image(
        chemin,
        width=1000,
        height=600,
        scale=2,
    )
    print(f"✓ PNG exporté : {chemin}")