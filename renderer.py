"""
renderer.py — Funciones de dibujo del mapa (draw_map y fast_update).
"""

import matplotlib.patheffects as pe
from matplotlib.collections import LineCollection, PathCollection
from matplotlib.colors import to_rgba

import osmnx as ox

from config import (
    BG, CITY_BOUNDS, CITY_COLORS, CITY_LABEL_POS,
    COL_UNVIS, COL_VISITED, COL_ACTIVE, COL_PATH,
    COL_ORIGIN, COL_DEST,
    ALPHA_DIM, ALPHA_ON,
    INIT_XLIM, INIT_YLIM,
    POI,
)


def edge_color(state):
    """Devuelve (color, alpha, linewidth) según el estado del arco."""
    return {
        "unvis":   (COL_UNVIS,   ALPHA_DIM, 0.5),
        "visited": (COL_VISITED, ALPHA_ON,  0.9),
        "active":  (COL_ACTIVE,  ALPHA_ON,  1.3),
        "path":    (COL_PATH,    ALPHA_ON,  2.8),
    }.get(state, (COL_UNVIS, ALPHA_DIM, 0.5))


def city_of(G, n):
    """Devuelve el nombre de la ciudad a la que pertenece el nodo n."""
    x, y = G.nodes[n]["x"], G.nodes[n]["y"]
    for c, (x0, x1, y0, y1) in CITY_BOUNDS.items():
        if x0 <= x <= x1 and y0 <= y <= y1:
            return c
    return None


def draw_map(G, ax, canvas, var_orig, var_dest):
    """
    Dibuja el mapa completo desde cero.
    Devuelve (_lc, _pc) — referencias a LineCollection y PathCollection
    para reutilizar en fast_update().
    """
    prev_xlim = ax.get_xlim()
    prev_ylim = ax.get_ylim()

    ax.cla()
    ax.set_facecolor(BG)
    ax.set_axis_off()

    ec, ns, nc = [], [], []

    for u, v, k in G.edges(keys=True):
        col, alp, _ = edge_color(G.edges[u, v, k].get("_state", "unvis"))
        r, g, b, _  = to_rgba(col)
        ec.append((r, g, b, alp))

    for n in G.nodes:
        st = G.nodes[n].get("_state", "unvis")
        if   st == "origin":  nc.append(COL_ORIGIN);  ns.append(90)
        elif st == "dest":    nc.append(COL_DEST);    ns.append(90)
        elif st == "visited": nc.append(COL_VISITED); ns.append(3)
        else:
            c = city_of(G, n)
            nc.append(CITY_COLORS.get(c, "#1e3a4a"))
            ns.append(2)

    ox.plot_graph(G, ax=ax,
                  node_size=ns, node_color=nc,
                  edge_color=ec,
                  bgcolor=BG, show=False, close=False)

    _lc = next((o for o in ax.collections if isinstance(o, LineCollection)), None)
    _pc = next((o for o in ax.collections if isinstance(o, PathCollection)), None)

    # Etiquetas de ciudades
    for city, (lon, lat) in CITY_LABEL_POS.items():
        ax.text(lon, lat, city,
                color=CITY_COLORS[city],
                fontsize=14, fontweight="bold", ha="center",
                path_effects=[pe.withStroke(linewidth=3, foreground=BG)],
                zorder=12)

    # POIs
    orig_name = var_orig.get()
    dest_name = var_dest.get()
    for name, (lat, lon) in POI.items():
        is_o = name == orig_name
        is_d = name == dest_name
        col  = COL_ORIGIN if is_o else (COL_DEST if is_d else "#445566")
        sz   = 110 if (is_o or is_d) else 30
        ax.scatter(lon, lat, color=col, s=sz,
                   zorder=10 if (is_o or is_d) else 4,
                   edgecolors="white" if (is_o or is_d) else "none",
                   linewidths=0.8)
        if is_o or is_d:
            tag   = "ORIGEN" if is_o else "DESTINO"
            short = name.split("—")[-1].strip()
            ax.text(lon, lat + 0.0022, f"{tag}\n{short}",
                    color=col, fontsize=7.5, fontweight="bold",
                    ha="center", zorder=11,
                    path_effects=[pe.withStroke(linewidth=2, foreground=BG)])

    if prev_xlim and prev_xlim != (0.0, 1.0):
        ax.set_xlim(prev_xlim)
        ax.set_ylim(prev_ylim)
    else:
        ax.set_xlim(INIT_XLIM)
        ax.set_ylim(INIT_YLIM)

    canvas.draw_idle()
    return _lc, _pc


def fast_update(G, ax, canvas, lc, pc):
    """
    Actualiza solo colores/tamaños sin redibujar todo el grafo.
    Si lc o pc son None, delega a draw_map.
    Devuelve False si no pudo actualizar (señal para redibujar).
    """
    if lc is None or pc is None:
        return False

    ec, ns, nc = [], [], []
    for u, v, k in G.edges(keys=True):
        col, alp, _ = edge_color(G.edges[u, v, k].get("_state", "unvis"))
        r, g, b, _  = to_rgba(col)
        ec.append((r, g, b, alp))

    for n in G.nodes:
        st = G.nodes[n].get("_state", "unvis")
        if   st == "origin":  nc.append(COL_ORIGIN);  ns.append(90)
        elif st == "dest":    nc.append(COL_DEST);    ns.append(90)
        elif st == "visited": nc.append(COL_VISITED); ns.append(3)
        else:
            c = city_of(G, n)
            nc.append(CITY_COLORS.get(c, "#1e3a4a"))
            ns.append(2)

    lc.set_colors(ec)
    pc.set_facecolor(nc)
    pc.set_sizes(ns)
    canvas.draw_idle()
    return True
