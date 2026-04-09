"""
algorithms.py — MinHeap, Dijkstra, A* y reconstrucción de camino.
"""

import heapq
import math


# ─── UTILIDADES ────────────────────────────────────────────────

def haversine_m(G, a, b):
    """Distancia en metros entre dos nodos (heurística correcta para A*)."""
    lat1, lon1 = math.radians(G.nodes[a]["y"]), math.radians(G.nodes[a]["x"])
    lat2, lon2 = math.radians(G.nodes[b]["y"]), math.radians(G.nodes[b]["x"])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    aa = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    return 6_371_000 * 2 * math.asin(math.sqrt(aa))


def _best_edge(G, u, v):
    """Devuelve la clave del edge (u,v,k) con menor weight en un MultiDiGraph."""
    edges  = G[u][v]
    best_k = min(edges, key=lambda k: edges[k].get("weight", float("inf")))
    return best_k, edges[best_k]


# ─── ESTRUCTURAS ───────────────────────────────────────────────

class MinHeap:
    def __init__(self):   self.h = []
    def push(self, x):    heapq.heappush(self.h, x)
    def pop(self):        return heapq.heappop(self.h)
    @property
    def empty(self):      return not self.h


# ─── ALGORITMOS (generadores paso a paso) ──────────────────────

def dijkstra_gen(G, orig, dest):
    """Dijkstra paso a paso. Yield (step, found)."""
    for n in G.nodes:
        G.nodes[n].update(_dist=float("inf"), _prev=None,
                          _vis=False, _state="unvis")
    for e in G.edges(keys=True):
        G.edges[e]["_state"] = "unvis"

    G.nodes[orig]["_dist"]  = 0
    G.nodes[orig]["_state"] = "origin"
    G.nodes[dest]["_state"] = "dest"

    pq   = MinHeap()
    pq.push((0.0, orig))
    step = 0

    while not pq.empty:
        d, u = pq.pop()
        if G.nodes[u]["_vis"]:
            continue
        if u == dest:
            yield step, True
            return
        G.nodes[u]["_vis"] = True
        if u not in (orig, dest):
            G.nodes[u]["_state"] = "visited"

        for v in G.successors(u):
            if G.nodes[v]["_vis"]:
                continue
            k, edata = _best_edge(G, u, v)
            G.edges[u, v, k]["_state"] = "active"
            nd = G.nodes[u]["_dist"] + edata.get("weight", 1.0)
            if nd < G.nodes[v]["_dist"]:
                G.nodes[v]["_dist"] = nd
                G.nodes[v]["_prev"] = u
                pq.push((nd, v))

        step += 1
        yield step, False


def astar_gen(G, orig, dest):
    """A* paso a paso con heurística Haversine. Yield (step, found)."""
    for n in G.nodes:
        G.nodes[n].update(_g=float("inf"), _prev=None,
                          _vis=False, _state="unvis")
    for e in G.edges(keys=True):
        G.edges[e]["_state"] = "unvis"

    G.nodes[orig]["_g"]     = 0
    G.nodes[orig]["_state"] = "origin"
    G.nodes[dest]["_state"] = "dest"

    # Velocidad media para convertir heurística a misma unidad que weight (seg)
    avg_speed_ms = 40 * 1000 / 3600   # 40 km/h en m/s

    def h(n):
        return haversine_m(G, n, dest) / avg_speed_ms

    pq       = MinHeap()
    open_set = {orig: 0.0}
    pq.push((h(orig), orig))
    step = 0

    while not pq.empty:
        f, u = pq.pop()
        if G.nodes[u]["_vis"]:
            continue
        if u == dest:
            yield step, True
            return
        G.nodes[u]["_vis"] = True
        if u not in (orig, dest):
            G.nodes[u]["_state"] = "visited"

        g_u = G.nodes[u]["_g"]

        for v in G.successors(u):
            if G.nodes[v]["_vis"]:
                continue
            k, edata = _best_edge(G, u, v)
            G.edges[u, v, k]["_state"] = "active"
            ng = g_u + edata.get("weight", 1.0)
            if ng < G.nodes[v].get("_g", float("inf")):
                G.nodes[v]["_g"]    = ng
                G.nodes[v]["_prev"] = u
                pq.push((ng + h(v), v))

        step += 1
        yield step, False


# ─── RECONSTRUCCIÓN ────────────────────────────────────────────

def rebuild_path(G, orig, dest):
    """Reconstruye camino y devuelve (km, avg_speed, mins_est)."""
    dist_m, speeds, curr = 0.0, [], dest
    while curr != orig:
        prev = G.nodes[curr].get("_prev")
        if prev is None:
            break
        k, edata = _best_edge(G, prev, curr)
        G.edges[prev, curr, k]["_state"] = "path"
        dist_m += edata.get("length", 0)
        speeds.append(edata.get("maxspeed", 40))
        curr = prev
    avg  = sum(speeds) / len(speeds) if speeds else 40
    km   = dist_m / 1000
    mins = (km / avg * 60) if avg else 0
    return km, avg, mins
