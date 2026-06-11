# Pathfinding · A* vs Dijkstra

Visualizador interactivo de algoritmos de búsqueda de rutas sobre mapas reales. Compara en tiempo real cómo A* y Dijkstra encuentran el camino más corto entre dos puntos usando datos reales de OpenStreetMap.

> Proyecto desarrollado para el curso de Inteligencia Artificial — Universidad Mariano Gálvez de Guatemala.

---

## ¿Qué hace?

- Descarga y procesa grafos de calles reales con **OSMnx**
- Implementa **Dijkstra** y **A\*** desde cero con MinHeap propio
- Anima el proceso de exploración de nodos en tiempo real
- Muestra distancias y rutas calculadas sobre el mapa
- Soporta múltiples ciudades configurables

---

## Estructura

```
pathfinding_project/
├── main.py          # Punto de entrada
├── app.py           # Ventana principal (tkinter) y lógica de UI
├── algorithms.py    # Dijkstra, A*, MinHeap, reconstrucción de camino
├── map_loader.py    # Descarga y preprocesamiento del grafo OSMnx
├── renderer.py      # Dibujo del mapa (draw_map y fast_update)
├── config.py        # Colores, POIs, límites de ciudades, constantes
└── requirements.txt
```

---

## Instalación

### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### macOS / Linux
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

> **macOS con Homebrew:** si usás `brew install python`, instalá también `brew install python-tk`.  
> La primera ejecución descarga el mapa (~30–60 s). Las siguientes son más rápidas por caché de OSMnx.

---

## Stack

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![OSMnx](https://img.shields.io/badge/OSMnx-OpenStreetMap-green?style=flat-square)
![NetworkX](https://img.shields.io/badge/NetworkX-informational?style=flat-square)
![Tkinter](https://img.shields.io/badge/Tkinter-UI-blue?style=flat-square)

| Dependencia | Uso |
|---|---|
| `osmnx` | Descarga y procesamiento de grafos de calles reales |
| `networkx` | Estructura de grafo y utilidades |
| `matplotlib` | Renderizado del mapa |
| `numpy` | Cálculos numéricos |
| `scikit-learn` | Utilidades de distancia y geometría |

---

## Algoritmos implementados

**Dijkstra** — Explora todos los nodos por costo acumulado. Garantiza el camino óptimo pero visita más nodos.

**A\*** — Usa una heurística (distancia euclidiana al destino) para guiar la búsqueda. Más eficiente que Dijkstra en la mayoría de casos.

Ambos están implementados desde cero en `algorithms.py` usando un MinHeap propio, sin depender de implementaciones externas.

---

## Contacto

[![Gmail](https://img.shields.io/badge/josuemorandelacruz16@gmail.com-D14836?style=flat-square&logo=gmail&logoColor=white)](mailto:josuemorandelacruz16@gmail.com)
