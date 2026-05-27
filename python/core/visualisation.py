# =============================
# ORGANON DATA SOLUTIONS
# core/visualisation.py
# =============================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import COLORS, PALETTE, FONTS, PATHS, ORGANON_SIGNATURE


# =============================
# UTILITAIRES CONSOLE
# =============================

def _separateur():
    print("  " + "-" * 50)

def _titre(texte):
    print(f"\n[ {texte} ]")

def _info(label, valeur):
    print(f"  {label:<30}: {valeur}")

def _ok(texte):
    print(f"  {texte} ✓")

def _erreur(texte):
    print(f"  ERREUR — {texte}")


# =============================
# STYLE GLOBAL MATPLOTLIB
# =============================

def _style():
    """Applique la charte graphique Organon à matplotlib."""
    plt.rcParams.update({
        "figure.facecolor":  COLORS["white"],
        "axes.facecolor":    COLORS["light"],
        "axes.edgecolor":    "#E5E7EB",
        "axes.labelcolor":   COLORS["dark"],
        "axes.titlesize":    FONTS["title_size"],
        "axes.labelsize":    FONTS["axis_size"],
        "axes.grid":         True,
        "grid.color":        "#E5E7EB",
        "grid.linestyle":    "--",
        "grid.alpha":        0.7,
        "xtick.color":       COLORS["text"],
        "ytick.color":       COLORS["text"],
        "xtick.labelsize":   FONTS["label_size"],
        "ytick.labelsize":   FONTS["label_size"],
        "font.family":       "serif",
        "text.color":        COLORS["dark"],
        "figure.titlesize":  FONTS["title_size"],
    })


def _sauvegarder(fig, nom_fichier, dossier=None):
    """
    Sauvegarde une figure matplotlib en PNG.
    Ajoute la signature Organon.
    """
    if dossier is None:
        dossier = PATHS["graphiques"]

    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier)

    fig.text(
        0.99, 0.01,
        ORGANON_SIGNATURE,
        ha="right", va="bottom",
        fontsize=8,
        color=COLORS["primary"],
        style="italic",
        transform=fig.transFigure,
    )

    fig.savefig(
        chemin,
        dpi=200,
        bbox_inches="tight",
        facecolor=COLORS["white"],
    )
    plt.close(fig)
    _ok(f"exporté → {chemin}")
    return chemin


def _sauvegarder_html(fig_plotly, nom_fichier, dossier=None):
    """
    Sauvegarde une figure Plotly en HTML interactif.
    """
    if dossier is None:
        dossier = PATHS["graphiques"]

    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier)

    fig_plotly.write_html(
        chemin,
        include_plotlyjs="cdn",
        full_html=True,
    )
    _ok(f"exporté → {chemin}")
    return chemin


# =============================
# GRAPHIQUES — NUMÉRIQUES
# =============================

def histogramme(df, col, titre=None, dossier=None):
    """Histogramme avec courbe de densité."""
    _style()
    titre = titre or f"Distribution — {col}"
    fig, ax = plt.subplots(figsize=(9, 6))

    serie = df[col].dropna()
    ax.hist(
        serie,
        bins="auto",
        color=COLORS["primary"],
        edgecolor=COLORS["white"],
        alpha=0.85,
        density=True,
    )

    # Courbe densité
    try:
        from scipy.stats import gaussian_kde
        kde  = gaussian_kde(serie)
        x    = np.linspace(serie.min(), serie.max(), 300)
        ax.plot(x, kde(x), color=COLORS["dark"], linewidth=2, label="Densité")
        ax.legend()
    except ImportError:
        pass

    ax.axvline(serie.mean(),   color=COLORS["secondary"], linestyle="--",
               linewidth=1.5, label=f"Moyenne : {round(serie.mean(),2)}")
    ax.axvline(serie.median(), color=COLORS["anthracite"], linestyle=":",
               linewidth=1.5, label=f"Médiane : {round(serie.median(),2)}")
    ax.legend()
    ax.set_title(titre, pad=20)
    ax.set_xlabel(col)
    ax.set_ylabel("Densité")

    nom = f"{col}_histogramme.png"
    return _sauvegarder(fig, nom, dossier)


def boxplot(df, col, col_groupe=None, titre=None, dossier=None):
    """
    Boxplot simple ou groupé.
    col_groupe : variable catégorielle pour grouper.
    """
    _style()
    titre = titre or (
        f"Boxplot — {col} selon {col_groupe}"
        if col_groupe else f"Boxplot — {col}"
    )
    fig, ax = plt.subplots(figsize=(9, 6))

    if col_groupe:
        groupes    = df[col_groupe].dropna().unique()
        donnees    = [df[df[col_groupe] == g][col].dropna().values for g in groupes]
        couleurs   = PALETTE[:len(groupes)]
        bp = ax.boxplot(
            donnees,
            labels=groupes,
            patch_artist=True,
            medianprops=dict(color=COLORS["dark"], linewidth=2),
        )
        for patch, couleur in zip(bp["boxes"], couleurs):
            patch.set_facecolor(couleur)
            patch.set_alpha(0.75)

        # Points individuels
        for i, (groupe, couleur) in enumerate(zip(donnees, couleurs), 1):
            ax.scatter(
                [i] * len(groupe), groupe,
                color=COLORS["secondary"],
                s=25, zorder=3, alpha=0.7,
            )
    else:
        serie = df[col].dropna()
        bp    = ax.boxplot(
            serie,
            patch_artist=True,
            medianprops=dict(color=COLORS["dark"], linewidth=2),
        )
        bp["boxes"][0].set_facecolor(COLORS["primary"])
        bp["boxes"][0].set_alpha(0.75)
        ax.scatter(
            [1] * len(serie), serie,
            color=COLORS["secondary"],
            s=25, zorder=3, alpha=0.7,
        )

    ax.set_title(titre, pad=20)
    ax.set_ylabel(col)

    suffix = f"_par_{col_groupe}" if col_groupe else ""
    nom    = f"{col}{suffix}_boxplot.png"
    return _sauvegarder(fig, nom, dossier)


def courbe_densite(df, col, col_groupe=None, titre=None, dossier=None):
    """Courbe de densité simple ou groupée."""
    try:
        from scipy.stats import gaussian_kde
    except ImportError:
        _erreur("scipy non installé — pip install scipy")
        return None

    _style()
    titre = titre or f"Densité — {col}"
    fig, ax = plt.subplots(figsize=(9, 6))

    if col_groupe:
        groupes = df[col_groupe].dropna().unique()
        for i, groupe in enumerate(groupes):
            serie = df[df[col_groupe] == groupe][col].dropna()
            if len(serie) < 2:
                continue
            kde = gaussian_kde(serie)
            x   = np.linspace(serie.min(), serie.max(), 300)
            ax.plot(x, kde(x), color=PALETTE[i % len(PALETTE)],
                    linewidth=2, label=str(groupe))
            ax.fill_between(x, kde(x), alpha=0.15,
                            color=PALETTE[i % len(PALETTE)])
        ax.legend()
    else:
        serie = df[col].dropna()
        kde   = gaussian_kde(serie)
        x     = np.linspace(serie.min(), serie.max(), 300)
        ax.plot(x, kde(x), color=COLORS["primary"], linewidth=2)
        ax.fill_between(x, kde(x), alpha=0.2, color=COLORS["primary"])

    ax.set_title(titre, pad=20)
    ax.set_xlabel(col)
    ax.set_ylabel("Densité")

    suffix = f"_par_{col_groupe}" if col_groupe else ""
    nom    = f"{col}{suffix}_densite.png"
    return _sauvegarder(fig, nom, dossier)


# =============================
# GRAPHIQUES — CATÉGORIELLES
# =============================

def barres(df, col, horizontal=False, titre=None, dossier=None):
    """Barres de fréquences pour variable catégorielle."""
    _style()
    titre = titre or f"Fréquences — {col}"
    fig, ax = plt.subplots(figsize=(9, 6))

    freq     = df[col].value_counts()
    freq_pct = df[col].value_counts(normalize=True) * 100
    couleurs = PALETTE[:len(freq)]

    if horizontal:
        bars = ax.barh(freq.index, freq.values, color=couleurs)
        for bar, pct in zip(bars, freq_pct.values):
            ax.text(
                bar.get_width() + 0.1,
                bar.get_y() + bar.get_height() / 2,
                f"{int(bar.get_width())} ({round(pct,1)}%)",
                va="center", fontsize=10,
            )
        ax.set_xlabel("Effectif")
        ax.set_ylabel(col)
    else:
        bars = ax.bar(freq.index, freq.values, color=couleurs)
        for bar, pct in zip(bars, freq_pct.values):
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.1,
                f"{int(bar.get_height())} ({round(pct,1)}%)",
                ha="center", fontsize=10,
            )
        ax.set_xlabel(col)
        ax.set_ylabel("Effectif")

    ax.set_title(titre, pad=20)

    orient = "horiz" if horizontal else "vert"
    nom    = f"{col}_barres_{orient}.png"
    return _sauvegarder(fig, nom, dossier)


def donut(df, col, titre=None, dossier=None):
    """Donut chart pour variable catégorielle."""
    _style()
    titre  = titre or f"Répartition — {col}"
    freq   = df[col].value_counts()
    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts = ax.pie(
        freq.values,
        labels=freq.index,
        colors=PALETTE[:len(freq)],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops=dict(width=0.5),
        textprops=dict(fontsize=12),
    )
    for at in autotexts:
        at.set_color("white")
        at.set_fontweight("bold")

    ax.set_title(titre, pad=20)
    nom = f"{col}_donut.png"
    return _sauvegarder(fig, nom, dossier)


def barres_groupees(df, col_x, col_groupe, titre=None, dossier=None):
    """Barres groupées — deux variables catégorielles."""
    _style()
    titre   = titre or f"{col_x} × {col_groupe}"
    tableau = pd.crosstab(df[col_x], df[col_groupe])
    groupes = tableau.columns
    x       = np.arange(len(tableau.index))
    width   = 0.8 / len(groupes)

    fig, ax = plt.subplots(figsize=(10, 6))

    for i, groupe in enumerate(groupes):
        offset = (i - len(groupes) / 2 + 0.5) * width
        bars   = ax.bar(
            x + offset,
            tableau[groupe],
            width,
            label=str(groupe),
            color=PALETTE[i % len(PALETTE)],
        )
        for bar in bars:
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05,
                str(int(bar.get_height())),
                ha="center", fontsize=9,
            )

    ax.set_xticks(x)
    ax.set_xticklabels(tableau.index)
    ax.set_xlabel(col_x)
    ax.set_ylabel("Effectif")
    ax.set_title(titre, pad=20)
    ax.legend(title=col_groupe)

    nom = f"{col_x}_x_{col_groupe}_barres_groupees.png"
    return _sauvegarder(fig, nom, dossier)


def barres_empilees(df, col_x, col_groupe, titre=None, dossier=None):
    """Barres empilées — proportions."""
    _style()
    titre   = titre or f"{col_x} × {col_groupe} (proportions)"
    tableau = pd.crosstab(df[col_x], df[col_groupe], normalize="index") * 100
    groupes = tableau.columns
    x       = np.arange(len(tableau.index))

    fig, ax = plt.subplots(figsize=(10, 6))
    bas     = np.zeros(len(tableau))

    for i, groupe in enumerate(groupes):
        vals = tableau[groupe].values
        ax.bar(
            x, vals, bottom=bas,
            label=str(groupe),
            color=PALETTE[i % len(PALETTE)],
        )
        for j, (v, b) in enumerate(zip(vals, bas)):
            if v > 5:
                ax.text(
                    x[j], b + v / 2,
                    f"{round(v,1)}%",
                    ha="center", va="center",
                    fontsize=9, color="white",
                    fontweight="bold",
                )
        bas += vals

    ax.set_xticks(x)
    ax.set_xticklabels(tableau.index)
    ax.set_xlabel(col_x)
    ax.set_ylabel("Proportion (%)")
    ax.set_title(titre, pad=20)
    ax.legend(title=col_groupe)

    nom = f"{col_x}_x_{col_groupe}_empilees.png"
    return _sauvegarder(fig, nom, dossier)


# =============================
# RECOMMANDATIONS
# =============================

# Ce que le programme recommande selon le type
RECOMMANDATIONS = {
    "numerique": {
        1: ("Histogramme",      "distribution des valeurs",        histogramme),
        2: ("Boxplot",          "médiane, IQR, outliers",          boxplot),
        3: ("Courbe densité",   "forme de la distribution",        courbe_densite),
        4: ("Barres",           "si la variable est discrète",     barres),
    },
    "categorie": {
        1: ("Barres verticales",   "fréquences par modalité",      barres),
        2: ("Barres horizontales", "si les labels sont longs",     barres),
        3: ("Donut",               "proportions",                  donut),
    },
    "numerique_x_categorie": {
        1: ("Boxplot groupé",      "comparer distributions",       boxplot),
        2: ("Courbe densité",      "comparer formes",              courbe_densite),
    },
    "categorie_x_categorie": {
        1: ("Barres groupées",     "comparer effectifs",           barres_groupees),
        2: ("Barres empilées",     "comparer proportions",         barres_empilees),
    },
}


def _afficher_recommandations(type_var):
    """Affiche les recommandations pour un type de variable."""
    recs = RECOMMANDATIONS.get(type_var, {})
    if not recs:
        return

    print()
    print("  Recommandés :")
    for num, (nom, desc, _) in recs.items():
        print(f"    {num}. {nom:<25} — {desc}")
    print(f"    0. Ignorer cette variable")


def _choisir_graphique(type_var):
    """
    Affiche les recommandations et retourne
    la liste des fonctions choisies.
    """
    _afficher_recommandations(type_var)
    print()
    choix_raw = input("  Votre choix (ex: 1,2) : ").strip()

    if not choix_raw or choix_raw == "0":
        return []

    recs    = RECOMMANDATIONS.get(type_var, {})
    choix   = []
    for c in choix_raw.split(","):
        c = c.strip()
        try:
            num = int(c)
            if num == 0:
                return []
            if num in recs:
                choix.append(recs[num])
            else:
                print(f"  Option ignorée : {c}")
        except ValueError:
            print(f"  Ignoré : {c}")

    return choix


# =============================
# PIPELINE PRINCIPAL
# =============================

def visualiser(df, types, dossier=None):
    """
    Pipeline interactif de visualisation.
    Pour chaque variable, recommande des graphiques
    et laisse l'utilisateur choisir.

    Usage :
      from core.visualisation import visualiser
      fichiers = visualiser(df, types, dossier="graphiques/projet1")
    """
    if df is None or types is None:
        _erreur("DataFrame ou types manquants.")
        return []

    _titre("VISUALISATION")
    print(f"  Variables détectées : {len(types)}")

    fichiers_produits = []

    for col, type_col in types.items():
        _separateur()
        print(f"\n  Variable : {col}  ({type_col})")

        if type_col in ["numerique", "categorie"]:
            choix = _choisir_graphique(type_col)

            for nom_graph, desc, fonction in choix:
                print(f"\n  {col} — {nom_graph} : en cours...")

                try:
                    if type_col == "numerique":
                        chemin = fonction(df, col, dossier=dossier)
                    else:
                        chemin = fonction(df, col, dossier=dossier)

                    if chemin:
                        fichiers_produits.append(chemin)
                except Exception as e:
                    _erreur(f"{col} — {nom_graph} : {e}")

        elif type_col == "date":
            print("  Variable date — visualisation non encore supportée.")

    # Croisements
    _separateur()
    print("\n  Voulez-vous produire des graphiques croisés ?")
    print("  (comparaison entre deux variables)")
    croiser = input("  Oui / Non : ").strip().lower()

    if croiser in ["oui", "o", "yes", "y"]:
        cols = list(df.columns)
        print("\n  Colonnes disponibles :")
        for i, col in enumerate(cols, 1):
            print(f"    {i}. {col:<22} ({types.get(col, '?')})")

        print()
        try:
            c1 = int(input("  Première variable  (numéro) : ").strip()) - 1
            c2 = int(input("  Deuxième variable  (numéro) : ").strip()) - 1
            col1 = cols[c1]
            col2 = cols[c2]
            t1   = types.get(col1)
            t2   = types.get(col2)

            if t1 == "numerique" and t2 == "categorie":
                choix = _choisir_graphique("numerique_x_categorie")
                for nom_graph, desc, fonction in choix:
                    print(f"\n  {col1} × {col2} — {nom_graph} : en cours...")
                    try:
                        chemin = fonction(df, col1, col_groupe=col2, dossier=dossier)
                        if chemin:
                            fichiers_produits.append(chemin)
                    except Exception as e:
                        _erreur(f"{col1} × {col2} : {e}")

            elif t1 == "categorie" and t2 == "categorie":
                choix = _choisir_graphique("categorie_x_categorie")
                for nom_graph, desc, fonction in choix:
                    print(f"\n  {col1} × {col2} — {nom_graph} : en cours...")
                    try:
                        chemin = fonction(df, col1, col2, dossier=dossier)
                        if chemin:
                            fichiers_produits.append(chemin)
                    except Exception as e:
                        _erreur(f"{col1} × {col2} : {e}")

            else:
                print("  Combinaison non supportée pour l'instant.")

        except (ValueError, IndexError) as e:
            _erreur(f"Sélection invalide : {e}")

    print()
    print("=" * 52)
    print(f"  [ VISUALISATION ] Terminé ✓")
    print(f"  Graphiques produits : {len(fichiers_produits)}")
    print("=" * 52)
    print()

    return fichiers_produits