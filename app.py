"""
app.py — Clase principal App (ventana tkinter + lógica de UI).
"""

import random
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import networkx as nx
import osmnx as ox

from config import (
    BG, BG2, TEXT, TEXT2, ACCENT,
    COL_VISITED, COL_ORIGIN, COL_DEST,
    INIT_XLIM, INIT_YLIM,
    POI,
)
from algorithms import dijkstra_gen, astar_gen, rebuild_path
from map_loader import load_graph
from renderer import draw_map, fast_update


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A* vs Dijkstra — Cobán · Carchá · Chamelco")
        self.configure(bg=BG)
        self.geometry("1320x860")
        self.minsize(1050, 700)

        self.G            = None
        self.orig_node    = None
        self.dest_node    = None
        self.anim_after   = None
        self.running      = False
        self.gen          = None
        self.step_count   = 0
        self.vis_count    = 0
        self.current_algo = None
        self._lc          = None
        self._pc          = None

        self._build_ui()
        self._status("⏳  Descargando mapa… primera vez ~30–60 s")
        threading.Thread(target=self._load_map, daemon=True).start()

    # ── UI ─────────────────────────────────────────────────────
    def _build_ui(self):
        hdr = tk.Frame(self, bg=BG, pady=8)
        hdr.pack(fill="x", padx=18)
        tk.Label(hdr, text="A* vs Dijkstra",
                 font=("Helvetica", 20, "bold"),
                 fg=TEXT, bg=BG).pack(side="left")
        tk.Label(hdr, text="  Cobán · Carchá · Chamelco",
                 font=("Helvetica", 13), fg=TEXT2, bg=BG).pack(side="left")

        main = tk.Frame(self, bg=BG)
        main.pack(fill="both", expand=True, padx=8)

        # ── Sidebar ──────────────────────
        sb = tk.Frame(main, bg=BG2, width=258, padx=13, pady=12)
        sb.pack(side="left", fill="y", padx=(0, 6))
        sb.pack_propagate(False)

        def sec(t):
            tk.Label(sb, text=t.upper(), font=("Helvetica", 8, "bold"),
                     fg=TEXT2, bg=BG2).pack(anchor="w", pady=(10, 2))

        sec("Origen")
        self.var_orig = tk.StringVar(value="Cobán — Parque Central")
        ttk.Combobox(sb, textvariable=self.var_orig,
                     values=list(POI.keys()),
                     state="readonly", width=27).pack(anchor="w", fill="x")

        sec("Destino")
        self.var_dest = tk.StringVar(value="Carchá — Parque")
        ttk.Combobox(sb, textvariable=self.var_dest,
                     values=list(POI.keys()),
                     state="readonly", width=27).pack(anchor="w", fill="x")

        tk.Button(sb, text="↺  Puntos aleatorios",
                  command=self._random_pts,
                  font=("Helvetica", 9), bg=BG, fg=TEXT2,
                  relief="flat", cursor="hand2").pack(anchor="w", pady=(4, 0))

        sec("Velocidad animación")
        sf = tk.Frame(sb, bg=BG2); sf.pack(fill="x")
        tk.Label(sf, text="Lenta", fg=TEXT2, bg=BG2,
                 font=("Helvetica", 8)).pack(side="left")
        self.speed_var = tk.IntVar(value=5)
        tk.Scale(sf, from_=1, to=10, orient="horizontal",
                 variable=self.speed_var, bg=BG2, fg=TEXT,
                 troughcolor="#21262d", highlightthickness=0,
                 showvalue=False).pack(side="left", fill="x", expand=True)
        tk.Label(sf, text="Rápida", fg=TEXT2, bg=BG2,
                 font=("Helvetica", 8)).pack(side="left")

        sec("Algoritmo")
        self.btn_d = tk.Button(sb, text="▶  Dijkstra",
                               command=lambda: self._start("dijkstra"),
                               font=("Helvetica", 12, "bold"),
                               bg="#b85200", fg="white",
                               activebackground="#d36206",
                               relief="flat", pady=8,
                               cursor="hand2", state="disabled")
        self.btn_d.pack(fill="x", pady=(2, 3))

        self.btn_a = tk.Button(sb, text="▶  A*",
                               command=lambda: self._start("astar"),
                               font=("Helvetica", 12, "bold"),
                               bg="#1255a0", fg="white",
                               activebackground="#1a7cd8",
                               relief="flat", pady=8,
                               cursor="hand2", state="disabled")
        self.btn_a.pack(fill="x", pady=(0, 3))

        self.btn_stop = tk.Button(sb, text="⏹  Detener",
                                  command=self._stop,
                                  font=("Helvetica", 9),
                                  bg=BG, fg=TEXT2,
                                  relief="flat", cursor="hand2",
                                  state="disabled")
        self.btn_stop.pack(fill="x")

        tk.Button(sb, text="🔍  Resetear vista",
                  command=self._reset_view,
                  font=("Helvetica", 9), bg=BG, fg=TEXT2,
                  relief="flat", cursor="hand2").pack(fill="x", pady=(8, 0))

        sec("Estadísticas")
        sf2 = tk.Frame(sb, bg=BG2); sf2.pack(fill="x")
        self.s_algo = self._stat(sf2, "Algoritmo")
        self.s_iter = self._stat(sf2, "Iteraciones")
        self.s_vis  = self._stat(sf2, "Visitados")
        self.s_dist = self._stat(sf2, "Distancia")
        self.s_time = self._stat(sf2, "Tiempo est.")
        self.s_cpu  = self._stat(sf2, "Cómputo")

        sec("Leyenda")
        from config import (COL_UNVIS, COL_VISITED, COL_ACTIVE,
                            COL_PATH, CITY_COLORS)
        for col, lbl in [
            (COL_UNVIS,   "No visitado"),
            (COL_VISITED, "Visitado"),
            (COL_ACTIVE,  "Frontera activa"),
            (COL_PATH,    "Camino final"),
            (COL_ORIGIN,  "Origen"),
            (COL_DEST,    "Destino"),
            (CITY_COLORS["Cobán"],    "Cobán"),
            (CITY_COLORS["Carchá"],   "Carchá"),
            (CITY_COLORS["Chamelco"], "Chamelco"),
        ]:
            r = tk.Frame(sb, bg=BG2); r.pack(anchor="w", pady=1)
            tk.Label(r, width=2, height=1, bg=col).pack(side="left", padx=(0, 6))
            tk.Label(r, text=lbl, fg=TEXT2, bg=BG2,
                     font=("Helvetica", 9)).pack(side="left")

        # ── Mapa ─────────────────────────────────
        mf = tk.Frame(main, bg=BG)
        mf.pack(side="left", fill="both", expand=True)

        self.fig = plt.figure(figsize=(10, 7.8), facecolor=BG)
        self.ax  = self.fig.add_subplot(111)
        self.ax.set_facecolor(BG)
        self.ax.set_axis_off()
        self.fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

        self.canvas_mpl = FigureCanvasTkAgg(self.fig, master=mf)
        self.canvas_mpl.get_tk_widget().pack(fill="both", expand=True)

        tf = tk.Frame(mf, bg="#1c2128"); tf.pack(fill="x", side="bottom")
        toolbar = NavigationToolbar2Tk(self.canvas_mpl, tf)
        toolbar.config(background="#1c2128")
        for ch in toolbar.winfo_children():
            try: ch.config(bg="#1c2128", fg=TEXT2)
            except: pass
        toolbar.update()

        self.canvas_mpl.mpl_connect("scroll_event", self._on_scroll)

        sb3 = tk.Frame(self, bg=BG2, pady=4)
        sb3.pack(fill="x", side="bottom")
        self.status_var = tk.StringVar(value="Iniciando…")
        tk.Label(sb3, textvariable=self.status_var,
                 fg=TEXT2, bg=BG2,
                 font=("Helvetica", 10)).pack(side="left", padx=12)

    def _stat(self, p, label):
        r = tk.Frame(p, bg=BG2); r.pack(fill="x", pady=1)
        tk.Label(r, text=label+":", fg=TEXT2, bg=BG2,
                 font=("Helvetica", 9), width=14, anchor="w").pack(side="left")
        l = tk.Label(r, text="—", fg=TEXT, bg=BG2,
                     font=("Helvetica", 9, "bold"))
        l.pack(side="left"); return l

    def _status(self, msg):
        self.status_var.set(msg)

    # ── ZOOM / PAN ─────────────────────────────
    def _on_scroll(self, ev):
        if ev.xdata is None: return
        f  = 0.82 if ev.button == "up" else 1.22
        xl, yl = self.ax.get_xlim(), self.ax.get_ylim()
        self.ax.set_xlim([ev.xdata + (x - ev.xdata)*f for x in xl])
        self.ax.set_ylim([ev.ydata + (y - ev.ydata)*f for y in yl])
        self.canvas_mpl.draw_idle()

    def _reset_view(self):
        self.ax.set_xlim(INIT_XLIM)
        self.ax.set_ylim(INIT_YLIM)
        self.canvas_mpl.draw_idle()

    # ── CARGA DEL MAPA ─────────────────────────
    def _load_map(self):
        try:
            G = load_graph(status_cb=lambda m: self.after(0, lambda msg=m: self._status(msg)))
            self.G = G
            self.after(0, self._on_map_loaded)
        except Exception as ex:
            import traceback; traceback.print_exc()
            msg = str(ex)
            self.after(0, lambda m=msg: self._status(f"❌ Error: {m}"))
            self.after(0, lambda m=msg: messagebox.showerror("Error cargando mapa", m))

    def _on_map_loaded(self):
        n_nodes = len(self.G.nodes)
        n_edges = len(self.G.edges)
        self._draw_map()
        self.btn_d.config(state="normal")
        self.btn_a.config(state="normal")
        self._status(
            f"✅  Mapa listo — {n_nodes} nodos · {n_edges} aristas. "
            "Scroll = zoom · Arrastrá = pan")

    # ── DIBUJO ─────────────────────────────────
    def _draw_map(self):
        self._lc, self._pc = draw_map(
            self.G, self.ax, self.canvas_mpl,
            self.var_orig, self.var_dest
        )

    def _fast_update(self):
        ok = fast_update(self.G, self.ax, self.canvas_mpl, self._lc, self._pc)
        if not ok:
            self._draw_map()

    # ── CONTROLES ──────────────────────────────
    def _reset_state(self):
        if not self.G: return
        for u, v, k in self.G.edges(keys=True):
            self.G.edges[u, v, k]["_state"] = "unvis"
        for n in self.G.nodes:
            self.G.nodes[n]["_state"] = "unvis"
            self.G.nodes[n]["_prev"]  = None
            self.G.nodes[n]["_vis"]   = False
            self.G.nodes[n]["_dist"]  = float("inf")
            self.G.nodes[n]["_g"]     = float("inf")
        self.step_count = self.vis_count = 0
        for l in [self.s_algo, self.s_iter, self.s_vis,
                  self.s_dist, self.s_time, self.s_cpu]:
            l.config(text="—", fg=TEXT)

    def _random_pts(self):
        keys = list(POI.keys())
        o, d = random.sample(keys, 2)
        self.var_orig.set(o); self.var_dest.set(d)
        if self.G:
            self._stop(); self._reset_state(); self._draw_map()

    def _start(self, algo):
        if not self.G: return
        self._stop(); self._reset_state()

        on = self.var_orig.get(); dn = self.var_dest.get()
        if on == dn:
            messagebox.showwarning("Atención", "Elegí origen y destino diferentes.")
            return

        olat, olon = POI[on]; dlat, dlon = POI[dn]
        try:
            self.orig_node = ox.nearest_nodes(self.G, olon, olat)
            self.dest_node = ox.nearest_nodes(self.G, dlon, dlat)
        except Exception as ex:
            messagebox.showerror("Error buscando nodos", str(ex)); return

        if not nx.has_path(self.G.to_undirected(), self.orig_node, self.dest_node):
            messagebox.showwarning(
                "Sin ruta",
                "No existe camino entre origen y destino en el grafo.\n"
                "Probá con otros puntos.")
            return

        self.G.nodes[self.orig_node]["_state"] = "origin"
        self.G.nodes[self.dest_node]["_state"] = "dest"

        self.gen = (dijkstra_gen if algo == "dijkstra" else astar_gen)(
            self.G, self.orig_node, self.dest_node)
        self.current_algo = algo
        self.running      = True
        self.step_count   = self.vis_count = 0
        self.t_start      = time.time()

        col = COL_VISITED if algo == "dijkstra" else "#4fa3ff"
        self.s_algo.config(
            text="Dijkstra" if algo == "dijkstra" else "A*", fg=col)

        self.btn_d.config(state="disabled")
        self.btn_a.config(state="disabled")
        self.btn_stop.config(state="normal")

        self._draw_map()
        aname = "Dijkstra" if algo == "dijkstra" else "A*"
        self._status(f"▶  {aname} ejecutándose…  Scroll = zoom · Arrastrá = mover")
        self._tick()

    def _tick(self):
        if not self.running: return
        spd   = self.speed_var.get()
        steps = max(1, spd * 4)
        delay = max(16, 90 - spd * 8)

        found = False
        for _ in range(steps):
            try:
                step, found = next(self.gen)
                self.step_count = step
                self.vis_count  = sum(
                    1 for n in self.G.nodes
                    if self.G.nodes[n].get("_state") == "visited")
                if found: break
            except StopIteration:
                found = True; break

        self.s_iter.config(text=str(self.step_count))
        self.s_vis.config(text=str(self.vis_count))
        self.G.nodes[self.orig_node]["_state"] = "origin"
        self.G.nodes[self.dest_node]["_state"] = "dest"
        self._fast_update()

        if found:
            elapsed = time.time() - self.t_start
            km, _, mins = rebuild_path(self.G, self.orig_node, self.dest_node)
            self.G.nodes[self.orig_node]["_state"] = "origin"
            self.G.nodes[self.dest_node]["_state"] = "dest"
            self._draw_map()
            self.s_dist.config(text=f"{km:.2f} km")
            self.s_time.config(text=f"{mins:.1f} min")
            self.s_cpu.config(text=f"{elapsed:.2f} s")
            name = "Dijkstra" if self.current_algo == "dijkstra" else "A*"
            self._status(
                f"✅  {name} terminado — {self.step_count} iter · "
                f"{km:.2f} km · {mins:.1f} min estimados")
            self._stop()
        else:
            self.anim_after = self.after(delay, self._tick)

    def _stop(self):
        self.running = False
        if self.anim_after:
            self.after_cancel(self.anim_after); self.anim_after = None
        en = "normal" if self.G else "disabled"
        self.btn_d.config(state=en)
        self.btn_a.config(state=en)
        self.btn_stop.config(state="disabled")
