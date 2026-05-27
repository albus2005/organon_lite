# =============================
# ORGANON DATA SOLUTIONS
# Configuration globale
# =============================

import os

# =============================
# CHEMINS
# =============================

# Dossier python/
PYTHON_DIR = os.path.dirname(os.path.abspath(__file__))

# Racine du projet
BASE_DIR = os.path.dirname(PYTHON_DIR)

PATHS = {
    "python":      PYTHON_DIR,
    "base":        BASE_DIR,
    "graphiques":  os.path.join(BASE_DIR, "graphiques"),
    "rapports":    os.path.join(BASE_DIR, "rapports"),
    "projets":     os.path.join(PYTHON_DIR, "projets"),
}

# =============================
# COULEURS
# =============================

COLORS = {
    "primary":    "#CD7F32",  # Bronze
    "secondary":  "#FFD700",  # Or
    "dark":       "#1A1A2E",  # Bleu nuit
    "anthracite": "#374151",  # Gris anthracite
    "light":      "#F9F7F4",  # Fond clair
    "white":      "#FFFFFF",
    "text":       "#374151",
}

PALETTE = [
    "#CD7F32",
    "#FFD700",
    "#374151",
    "#1A1A2E",
    "#B86E28",
    "#C0C0C0",
]

# =============================
# TYPOGRAPHIE
# =============================

FONTS = {
    "family":     "Georgia, serif",
    "title_size": 20,
    "axis_size":  13,
    "label_size": 11,
}

# =============================
# STYLE PLOTLY GLOBAL
# =============================

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
        "x":       0.5,
        "xanchor": "center",
    },
    "colorway": PALETTE,
    "margin": {"t": 80, "b": 60, "l": 60, "r": 40},
}

# =============================
# SIGNATURE
# =============================

ORGANON_SIGNATURE = "Organon Data Solutions — Bukavu"

# =============================
# CONFIRMATION
# =============================

print("╔══════════════════════════════════════╗")
print("║     ORGANON DATA SOLUTIONS           ║")
print("║     Configuration chargée ✓          ║")
print("╚══════════════════════════════════════╝")