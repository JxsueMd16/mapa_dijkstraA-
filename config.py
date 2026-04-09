"""
config.py — VERSIÓN FINAL INTEGRADA
Incluye las 6 ciudades con todos los POIs originales y recalibración de límites.
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
CITY_BOUNDS = {
    "Cobán":         (-90.420, -90.340, 15.440, 15.510),
    "Carchá":        (-90.340, -90.270, 15.440, 15.520),
    "Chamelco":      (-90.360, -90.290, 15.395, 15.460),
    "Santa Cruz":    (-90.440, -90.410, 15.355, 15.390), 
    "San Cristóbal": (-90.495, -90.455, 15.345, 15.385), 
    "Tactic":        (-90.395, -90.320, 15.305, 15.340), 
}

CITY_LABEL_POS = {
    "Cobán":         (-90.379, 15.490),
    "Carchá":        (-90.308, 15.492),
    "Chamelco":      (-90.335, 15.440),
    "Santa Cruz":    (-90.430, 15.375),
    "San Cristóbal": (-90.479, 15.365),
    "Tactic":        (-90.351, 15.319),
}

# ─── POIs (Puntos de Interés) ──────────────────────────────────
POI = {
    # Cobán
    "Cobán — Parque Central":          (15.470234338732254, -90.37339146203715),
    "Cobán — Hospital Regional":       (15.47822973376058,  -90.37246007256836),
    "Cobán — Univ. Mariano Gálvez":    (15.471347642204115, -90.39514827003397),
    "Cobán — Plaza Magdalena":         (15.47085543463715,  -90.38559395466915),
    # Carchá
    "Carchá — Gran Carchá":            (15.476916688930459, -90.31149170200257),
    "Carchá — Parque":                 (15.48042344163784,  -90.30844941375157),
    "Carchá — Estadio":                (15.468787860742056, -90.31544164856894),
    # Chamelco
    "Chamelco — Parque Central":       (15.423663825445923, -90.33113862381677),
    "Chamelco — Univ. Rafael Landívar":(15.427733680891148, -90.33739796408203),
    "Chamelco — Municipalidad":        (15.427978358128525, -90.3320083396905),
    # San Cristóbal
    "San Cristóbal — Parque Central":  (15.365697354842979, -90.47922795243296),
    "San Cristóbal — El Petencito":    (15.365602261659005, -90.46979474401186),
    "San Cristóbal — Calzado Cobán":   (15.363694587338477, -90.48565166154708),
    # Santa Cruz
    "Santa Cruz — Parque Central":     (15.374815390035623, -90.43047519598323),
    "Santa Cruz — Park Hotel":         (15.374020885191536, -90.42381384105845),
    # Tactic
    "Tactic — Chi Ixim":               (15.310785410392926, -90.35159205780666),
    "Tactic — Parque Central":         (15.319189667906471, -90.35171191640386),
    "Tactic — La Granja":              (15.324348071946568, -90.38136117259802),
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