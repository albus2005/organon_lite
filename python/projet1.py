# =============================
# ORGANON DATA SOLUTIONS
# Projet 1 — Prévalence du paludisme
# Enfants < 5 ans — Bukavu
# =============================

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from config import COLORS, PALETTE, PATHS
from utils import (
    charger_csv, nettoyer, resume,
    style_matplotlib, appliquer_style,
    exporter, exporter_png,
    exporter_excel, exporter_pdf
)
import os

# =============================
# 1. CHARGEMENT ET NETTOYAGE
# =============================

df, rapport = nettoyer(charger_csv("projet1.csv"))
resume(df)

# =============================
# 2. CALCULS
# =============================

total      = len(df)
positifs   = len(df[df["resultat"] == "Paludisme"])
negatifs   = len(df[df["resultat"] == "Sain"])
prevalence = round((positifs / total) * 100, 1)

hemoglobine_positifs = round(
    df[df["resultat"] == "Paludisme"]["hemoglobine"].mean(), 2
)
hemoglobine_negatifs = round(
    df[df["resultat"] == "Sain"]["hemoglobine"].mean(), 2
)

hospitalises = len(df[df["hospitalise"] == "Oui"])

print(f"\n=== PRÉVALENCE ===")
print(f"Total          : {total}")
print(f"Positifs       : {positifs} ({prevalence}%)")
print(f"Négatifs       : {negatifs}")
print(f"Hospitalisés   : {hospitalises}")
print(f"Hb positifs    : {hemoglobine_positifs} g/dL")
print(f"Hb négatifs    : {hemoglobine_negatifs} g/dL")

# =============================
# 3. STYLE MATPLOTLIB
# =============================

style_matplotlib()

# =============================
# 4. GRAPHIQUE 1 — Prévalence
#    Plotly HTML + Matplotlib PNG
# =============================

# Plotly
fig1 = go.Figure(data=[
    go.Pie(
        labels=["Paludisme", "Sain"],
        values=[positifs, negatifs],
        hole=0.5,
        marker=dict(colors=[COLORS["primary"], COLORS["anthracite"]]),
        textinfo="label+percent",
        textfont=dict(size=13),
    )
])
fig1 = appliquer_style(
    fig1,
    f"Prévalence du paludisme — Enfants < 5 ans (n={total})"
)
fig1.add_annotation(
    text=f"<b>{prevalence}%</b>",
    x=0.5, y=0.5,
    showarrow=False,
    font=dict(size=28, color=COLORS["primary"]),
)
exporter(fig1, "graph1a.html")

# Matplotlib PNG
fig, ax = plt.subplots(figsize=(7, 7))
wedges, texts, autotexts = ax.pie(
    [positifs, negatifs],
    labels=["Paludisme", "Sain"],
    colors=[COLORS["primary"], COLORS["anthracite"]],
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops=dict(width=0.5),
    textprops=dict(fontsize=12),
)
for at in autotexts:
    at.set_color("white")
    at.set_fontweight("bold")
ax.text(
    0, 0, f"{prevalence}%",
    ha="center", va="center",
    fontsize=22, fontweight="bold",
    color=COLORS["primary"],
)
ax.set_title(
    f"Prévalence du paludisme\nEnfants < 5 ans (n={total})",
    fontsize=14, color=COLORS["dark"], pad=20,
)
exporter_png(fig, "graph1a.png")


# =============================
# 5. GRAPHIQUE 2 — Par quartier
#    Plotly HTML + Matplotlib PNG
# =============================

par_quartier = (
    df.groupby(["quartier", "resultat"])
    .size()
    .reset_index(name="count")
)

# Plotly
fig2 = px.bar(
    par_quartier,
    x="quartier",
    y="count",
    color="resultat",
    barmode="group",
    color_discrete_map={
        "Paludisme": COLORS["primary"],
        "Sain":      COLORS["anthracite"],
    },
    labels={
        "quartier": "Quartier",
        "count":    "Nombre de cas",
        "resultat": "Résultat",
    },
)
fig2 = appliquer_style(fig2, "Distribution des cas par quartier — Bukavu")
exporter(fig2, "graph1b.html")

# Matplotlib PNG
quartiers  = par_quartier["quartier"].unique()
pal_cas    = par_quartier[par_quartier["resultat"] == "Paludisme"]["count"].values
sain_cas   = par_quartier[par_quartier["resultat"] == "Sain"]["count"].values
x          = range(len(quartiers))
width      = 0.35

fig, ax = plt.subplots(figsize=(9, 6))
bars1 = ax.bar(
    [i - width/2 for i in x], pal_cas, width,
    label="Paludisme", color=COLORS["primary"]
)
bars2 = ax.bar(
    [i + width/2 for i in x], sain_cas, width,
    label="Sain", color=COLORS["anthracite"]
)
ax.set_xticks(list(x))
ax.set_xticklabels(quartiers)
ax.set_xlabel("Quartier")
ax.set_ylabel("Nombre de cas")
ax.set_title("Distribution des cas par quartier — Bukavu", pad=20)
ax.legend()
for bar in bars1:
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.1,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=10,
    )
for bar in bars2:
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.1,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=10,
    )
exporter_png(fig, "graph1b.png")


# =============================
# 6. GRAPHIQUE 3 — Hémoglobine
#    Plotly HTML + Matplotlib PNG
# =============================

# Plotly
fig3 = px.box(
    df,
    x="resultat",
    y="hemoglobine",
    color="resultat",
    color_discrete_map={
        "Paludisme": COLORS["primary"],
        "Sain":      COLORS["anthracite"],
    },
    labels={
        "resultat":    "Résultat",
        "hemoglobine": "Hémoglobine (g/dL)",
    },
    points="all",
)
fig3 = appliquer_style(
    fig3,
    "Taux d'hémoglobine selon le statut palustre"
)
exporter(fig3, "graph1c.html")

# Matplotlib PNG
fig, ax = plt.subplots(figsize=(8, 6))
groupes = [
    df[df["resultat"] == "Paludisme"]["hemoglobine"].values,
    df[df["resultat"] == "Sain"]["hemoglobine"].values,
]
bp = ax.boxplot(
    groupes,
    labels=["Paludisme", "Sain"],
    patch_artist=True,
    medianprops=dict(color=COLORS["dark"], linewidth=2),
)
bp["boxes"][0].set_facecolor(COLORS["primary"])
bp["boxes"][1].set_facecolor(COLORS["anthracite"])
for box in bp["boxes"]:
    box.set_alpha(0.7)

# Points individuels
for i, groupe in enumerate(groupes, 1):
    ax.scatter(
        [i] * len(groupe),
        groupe,
        color=COLORS["secondary"],
        s=30, zorder=3, alpha=0.8,
    )

ax.set_ylabel("Hémoglobine (g/dL)")
ax.set_title("Taux d'hémoglobine selon le statut palustre", pad=20)
ax.axhline(
    y=11,
    color="red", linestyle="--", alpha=0.5,
    label="Seuil anémie (11 g/dL)"
)
ax.legend()
exporter_png(fig, "graph1c.png")


# =============================
# 7. GRAPHIQUE 4 — Par sexe
#    Plotly HTML + Matplotlib PNG
# =============================

par_sexe = (
    df[df["resultat"] == "Paludisme"]
    .groupby("sexe")
    .size()
    .reset_index(name="count")
)

# Plotly
fig4 = px.bar(
    par_sexe,
    x="sexe",
    y="count",
    color="sexe",
    color_discrete_map={
        "M": COLORS["primary"],
        "F": COLORS["secondary"],
    },
    labels={
        "sexe":  "Sexe",
        "count": "Cas de paludisme",
    },
)
fig4 = appliquer_style(fig4, "Cas de paludisme par sexe")
exporter(fig4, "graph1d.html")

# Matplotlib PNG
fig, ax = plt.subplots(figsize=(7, 6))
sexes    = par_sexe["sexe"].values
valeurs  = par_sexe["count"].values
couleurs = [COLORS["primary"] if s == "M" else COLORS["secondary"] for s in sexes]
bars = ax.bar(sexes, valeurs, color=couleurs, width=0.4)
for bar in bars:
    ax.text(
        bar.get_x() + bar.get_width()/2,
        bar.get_height() + 0.1,
        str(int(bar.get_height())),
        ha="center", va="bottom", fontsize=12,
        fontweight="bold",
    )
ax.set_xlabel("Sexe")
ax.set_ylabel("Cas de paludisme")
ax.set_title("Cas de paludisme par sexe", pad=20)
patch_m = mpatches.Patch(color=COLORS["primary"], label="Masculin")
patch_f = mpatches.Patch(color=COLORS["secondary"], label="Féminin")
ax.legend(handles=[patch_m, patch_f])
exporter_png(fig, "graph1d.png")


# =============================
# 8. EXPORT EXCEL
# =============================

exporter_excel(df, "projet1_donnees.xlsx", "Paludisme Bukavu")


# =============================
# 9. RAPPORT PDF
# =============================

graphiques_path = PATHS["graphiques"]

sections = [
    {
        "type": "titre",
        "texte": "1. Contexte et objectifs"
    },
    {
        "type": "paragraphe",
        "texte": (
            "Cette étude analyse la prévalence du paludisme chez les enfants "
            "de moins de 5 ans dans trois quartiers de Bukavu : Bagira, Kadutu "
            "et Ibanda. Les données ont été collectées auprès de 30 patients "
            "âgés de 6 à 59 mois, avec mesure du TDR, du taux d'hémoglobine "
            "et du statut d'hospitalisation."
        )
    },
    {
        "type": "titre",
        "texte": "2. Résultats principaux"
    },
    {
        "type": "tableau",
        "entetes": ["Indicateur", "Valeur"],
        "data": [
            ["Total patients",              str(total)],
            ["Cas positifs (Paludisme)",    f"{positifs} ({prevalence}%)"],
            ["Cas négatifs (Sains)",        str(negatifs)],
            ["Hospitalisés",                str(hospitalises)],
            ["Hb moyenne — positifs",       f"{hemoglobine_positifs} g/dL"],
            ["Hb moyenne — négatifs",       f"{hemoglobine_negatifs} g/dL"],
        ]
    },
    {
        "type": "titre",
        "texte": "3. Visualisations"
    },
    {
        "type": "image",
        "chemin": os.path.join(graphiques_path, "graph1a.png")
    },
    {
        "type": "image",
        "chemin": os.path.join(graphiques_path, "graph1b.png")
    },
    {
        "type": "saut"
    },
    {
        "type": "image",
        "chemin": os.path.join(graphiques_path, "graph1c.png")
    },
    {
        "type": "image",
        "chemin": os.path.join(graphiques_path, "graph1d.png")
    },
    {
        "type": "titre",
        "texte": "4. Interprétation"
    },
    {
        "type": "paragraphe",
        "texte": (
            f"Une prévalence de {prevalence}% confirme une charge palustre élevée "
            "dans la population pédiatrique de Bukavu. Le quartier de Bagira "
            "concentre le plus grand nombre de cas positifs, suggérant des "
            "conditions environnementales favorables à la transmission."
        )
    },
    {
        "type": "paragraphe",
        "texte": (
            f"Les enfants positifs au TDR présentent un taux d'hémoglobine moyen "
            f"de {hemoglobine_positifs} g/dL, en dessous du seuil d'anémie de "
            "11 g/dL, indiquant une anémie palustre fréquente dans ce groupe."
        )
    },
]

exporter_pdf(
    "rapport_projet1.pdf",
    "Prévalence du paludisme chez les enfants de moins de 5 ans à Bukavu",
    "Organon Data Solutions — 2026",
    sections,
)

print("\n✓ Projet 1 terminé.")
print(f"  HTML     : graphiques/graph1a-d.html")
print(f"  PNG      : graphiques/graph1a-d.png")
print(f"  Excel    : graphiques/projet1_donnees.xlsx")
print(f"  PDF      : rapports/rapport_projet1.pdf")