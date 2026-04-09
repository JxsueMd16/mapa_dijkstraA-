"""
map_loader.py — Versión final para OSMnx 2.1.0
Descarga la región completa de una vez para garantizar conectividad.
"""

import networkx as nx
import osmnx as ox
from config import CITIES

def load_graph(status_cb=None):
    def notify(msg):
        if status_cb: status_cb(msg)

    # 1. En lugar de descargar por separado, creamos una lista de los nombres
    # Esto obliga a OSMnx a descargar un solo bloque que contenga todo.
    places = list(CITIES.values())
    
    notify("⏳ Descargando región (Cobán, Carchá, Chamelco)…")
    # Al pasar una lista, OSMnx crea un solo grafo conectado
    G = ox.graph_from_place(places, network_type="drive")

    # 2. Proyectar y Consolidar
    notify("🔧 Optimizando red de carreteras…")
    G = ox.project_graph(G)
    # Consolidamos intersecciones para limpiar geometrías duplicadas
    G = ox.simplification.consolidate_intersections(G, tolerance=15, rebuild_graph=True)
    
    # Regresamos a coordenadas geográficas para el renderer
    G = ox.project_graph(G, to_crs="EPSG:4326")

    # 3. Limpieza de componentes
    notify("🧹 Eliminando tramos aislados…")
    # Usamos la nueva ruta de la función en la v2.1.0
    G = ox.truncate.largest_component(G, strongly=True)

    # 4. Procesar pesos y velocidades
    notify("🔧 Calculando pesos finales…")
    for u, v, k, data in G.edges(keys=True, data=True):
        ms = 40
        v_speed = data.get("maxspeed", 40)
        
        # Limpieza de velocidad
        if isinstance(v_speed, list):
            try: ms = min(int(x) for x in v_speed if str(x).isdigit())
            except: ms = 40
        elif isinstance(v_speed, str):
            try: ms = int(v_speed.split()[0].replace('km/h', ''))
            except: ms = 40
        elif isinstance(v_speed, (int, float)):
            ms = int(v_speed)
            
        ms = max(10, ms)
        dist = data.get("length", 1)
        
        # Peso = tiempo (segundos)
        G.edges[u, v, k]["maxspeed"] = ms
        G.edges[u, v, k]["weight"] = dist / (ms * 1000 / 3600)
        G.edges[u, v, k]["_state"] = "unvis"

    # 5. Inicializar atributos de nodos
    for n in G.nodes:
        G.nodes[n].update({
            "_state": "unvis",
            "_prev": None,
            "_vis": False,
            "_dist": float("inf"),
            "_g": float("inf")
        })

    return G