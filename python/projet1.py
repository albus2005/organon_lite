# =============================
# ORGANON DATA SOLUTIONS
# Projet 1 — Prévalence du paludisme
# Enfants < 5 ans — Bukavu
# =============================

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from config import COLORS, PALETTE
from utils import charger_csv, nettoyer, appliquer_style, exporter, resume
from utils import charger_csv, nettoyer, appliquer_style, exporter, exporter_png, resume

# =============================
# 1. CHARGEMENT ET NETTOYAGE
# =============================

df, rapport = nettoyer(charger_csv("projet1.csv"))
resume(df)


# =============================
# 2. CALCULS
# =============================

total        = len(df)
positifs     = len(df[df["resultat"] == "Paludisme"])
negatifs     = len(df[df["resultat"] == "Sain"])
prevalence   = round((positifs / total) * 100, 1)

print(f"\n=== PRÉVALENCE ===")
print(f"Total patients  : {total}")
print(f"Cas positifs    : {positifs}")
print(f"Cas négatifs    : {negatifs}")
print(f"Prévalence      : {prevalence}%")


# =============================
# 3. GRAPHIQUE 1 — Prévalence globale
# =============================

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


# =============================
# 4. GRAPHIQUE 2 — Par quartier
# =============================

par_quartier = (
    df.groupby(["quartier", "resultat"])
    .size()
    .reset_index(name="count")
)

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


# =============================
# 5. GRAPHIQUE 3 — Hémoglobine
# =============================

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


# =============================
# 6. GRAPHIQUE 4 — Par sexe
# =============================

par_sexe = (
    df[df["resultat"] == "Paludisme"]
    .groupby("sexe")
    .size()
    .reset_index(name="count")
)

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

exporter(fig1, "graph1a.html")
exporter_png(fig1, "graph1a.png")

exporter(fig2, "graph1b.html")
exporter_png(fig2, "graph1b.png")

exporter(fig3, "graph1c.html")
exporter_png(fig3, "graph1c.png")

exporter(fig4, "graph1d.html")
exporter_png(fig4, "graph1d.png")

print("\n✓ Projet 1 terminé — 4 graphiques exportés.")