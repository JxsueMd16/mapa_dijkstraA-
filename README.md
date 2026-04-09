# A* vs Dijkstra — Cobán · Carchá · Chamelco

## Estructura del proyecto

```
pathfinding_project/
├── main.py          # Punto de entrada — correr esto
├── app.py           # Ventana principal (tkinter) y lógica de UI
├── algorithms.py    # Dijkstra, A*, MinHeap, reconstrucción de camino
├── map_loader.py    # Descarga y preprocesamiento del grafo OSMnx
├── renderer.py      # Dibujo del mapa (draw_map y fast_update)
├── config.py        # Colores, POIs, límites de ciudades, constantes
└── requirements.txt
```

## Instalación

```bash
pip install -r requirements.txt
```

## Uso

```bash
python main.py
```

## Notas para macOS

- `tkinter` viene incluido en Python oficial de python.org.  
  Si usás Homebrew (`brew install python`), instalá también: `brew install python-tk`.
- La primera ejecución descarga el mapa (~30–60 s), las siguientes son más rápidas gracias al caché de osmnx.
