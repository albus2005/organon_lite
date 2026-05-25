# =============================
# ORGANON DATA SOLUTIONS
# Configuration globale
# =============================

# Couleurs de la charte graphique
COLORS = {
    "primary":    "#CD7F32",  # Bronze
    "secondary":  "#FFD700",  # Or
    "dark":       "#1A1A2E",  # Bleu nuit
    "anthracite": "#374151",  # Gris anthracite
    "light":      "#F9F7F4",  # Fond clair
    "white":      "#FFFFFF",
    "text":       "#374151",
}

# Palette séquentielle pour graphiques multi-séries
PALETTE = [
    "#CD7F32",
    "#FFD700",
    "#374151",
    "#1A1A2E",
    "#B86E28",
    "#C0C0C0",
]

# Typographie
FONTS = {
    "family": "Georgia, serif",
    "title_size": 20,
    "axis_size": 13,
    "label_size": 11,
}

# Style global Plotly
LAYOUT = {
    "font": {
        "family": FONTS["family"],
        "color":  COLORS["dark"],
        "size":   FONTS["axis_size"],
    },
    "paper_bgcolor": COLORS["white"],
    "plot_bgcolor":  COLORS["light"],
    "title": {
        "font": {
            "size":   FONTS["title_size"],
            "color":  COLORS["dark"],
            "family": FONTS["family"],
        },
        "x": 0.5,
        "xanchor": "center",
    },
    "colorway": PALETTE,
    "margin": {"t": 80, "b": 60, "l": 60, "r": 40},
}

# Dossiers
# Dossiers
import os

# Dossier python/
PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))

# Racine du projet organon_lite/
BASE_DIR = os.path.dirname(PYTHON_DIR)

PATHS = {
    "data":       os.path.join(PYTHON_DIR, "data", ""),
    "graphiques": os.path.join(BASE_DIR, "graphiques", ""),
}

print("DATA :", PATHS["data"])
print("GRAPH:", PATHS["graphiques"])

# Signature
ORGANON_SIGNATURE = "Organon Data Solutions"

# =============================
# 6. EXPORTER EN PNG
# =============================

def exporter_png(fig, nom_fichier):
    """
    Exporte la figure en PNG dans graphiques/
    Usage : exporter_png(fig, "graph1a.png")
    """
    dossier = os.path.join(BASE_DIR, "graphiques")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, nom_fichier)
    fig.write_image(
        chemin,
        width=1000,
        height=600,
        scale=2,
    )
    print(f"✓ PNG exporté : {chemin}")

