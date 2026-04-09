"""
config.py — VERSIÓN FINAL RECALIBRADA
Incluye coordenadas exactas de San Cristóbal, Santa Cruz y Tactic.
"""

# ─── COLORES Y ESTILOS ──────────────────────────────────────────
BG, BG2, TEXT, TEXT2, ACCENT = "#0d1117", "#161b22", "#e6edf3", "#8b949e", "#1f6feb"
COL_UNVIS, COL_VISITED, COL_ACTIVE, COL_PATH = "#1e2d3d", "#d36206", "#e8a900", "#00e5ff"
COL_ORIGIN, COL_DEST = "#ff4d4d", "#44ff88"
ALPHA_DIM, ALPHA_ON = 0.30, 1.0

CITY_COLORS = {
    "Cobán":         "#4f9eff",
    "Carchá":        "#ff9f4f",
    "Chamelco":      "#b07fff",
    "Santa Cruz":    "#ff4f8b",
    "San Cristóbal": "#4fff8b",
    "Tactic":        "#fcfc4d",
}

# ─── LÍMITES GEOGRÁFICOS (West, East, South, North) ───────────
# Ajustados para incluir puntos como La Granja en Tactic y El Petencito en San Cris
CITY_BOUNDS = {
    "Cobán":         (-90.420, -90.340, 15.440, 15.510),
    "Carchá":        (-90.340, -90.270, 15.440, 15.520),
    "Chamelco":      (-90.360, -90.290, 15.395, 15.460),
    "Santa Cruz":    (-90.440, -90.410, 15.365, 15.390), # Bajamos el South a 15.365
    "San Cristóbal": (-90.495, -90.455, 15.355, 15.385), # Ajustado para Calzado Cobán y Petencito
    "Tactic":        (-90.395, -90.320, 15.305, 15.340), # Expandido al West para La Granja
}

CITY_LABEL_POS = {
    "Cobán":         (-90.379, 15.490),
    "Carchá":        (-90.308, 15.492),
    "Chamelco":      (-90.335, 15.440),
    "Santa Cruz":    (-90.430, 15.375),
    "San Cristóbal": (-90.479, 15.365),
    "Tactic":        (-90.351, 15.319),
}

# ─── POIs EXACTOS ─────────────────────────────────────────────
POI = {
    # SAN CRISTOBAL
    "San Cristóbal — Parque Central":  (15.365697, -90.479227),
    "San Cristóbal — El Petencito":    (15.365602, -90.469794),
    "San Cristóbal — Calzado Cobán":   (15.363694, -90.485651),
    # SANTA CRUZ
    "Santa Cruz — Parque Central":     (15.374815, -90.430475),
    "Santa Cruz — Park Hotel":         (15.374020, -90.423813),
    # TACTIC
    "Tactic — Chi Ixim":               (15.310785, -90.351592),
    "Tactic — Parque Central":         (15.319189, -90.351711),
    "Tactic — La Granja":              (15.324348, -90.381361),
    # Cobán, Carchá, Chamelco (Originales)
    "Cobán — Parque Central":          (15.470234, -90.373391),
    "Carchá — Parque":                 (15.480423, -90.308449),
    "Chamelco — Parque Central":       (15.423663, -90.331138),
}

# ─── VISTA INICIAL ────────────────────────────────────────────
INIT_XLIM = (-90.510, -90.265)
INIT_YLIM = (15.300, 15.530)

CITIES = {
    "Cobán":         "Cobán, Alta Verapaz, Guatemala",
    "Carchá":        "San Pedro Carchá, Alta Verapaz, Guatemala",
    "Chamelco":      "San Juan Chamelco, Alta Verapaz, Guatemala",
    "Santa Cruz":    "Santa Cruz Verapaz, Alta Verapaz, Guatemala",
    "San Cristóbal": "San Cristóbal Verapaz, Alta Verapaz, Guatemala",
    "Tactic":        "Tactic, Alta Verapaz, Guatemala",
}