import tkinter as tk
from tkinter import messagebox

# ---------------- GRAFO ----------------

grafo = {
    "A": {"B": 97.28, "C": 112.51},
    "B": {"A": 97.28, "F": 70.01, "VA": 11.58},
    "C": {"A": 112.51, "N": 59.60, "VA": 29.69, "D": 29.58, "M": 72.23},
    "D": {"VA": 11.58, "R2": 69.39, "C": 29.58},
    "E": {"F": 47.32, "VA": 36.06, "R2": 53.27},
    "F": {"B": 70.06, "E": 47.32, "R2": 92.04, "R1": 72.30},
    "G": {"R1": 36.51},
    "H": {"R1": 46.52, "I": 38.95},
    "I": {"H": 38.95, "J": 68.39},
    "J": {"I": 68.39, "K": 21.39},
    "K": {"J": 21.39, "R2": 40.37},
    "L": {"R2": 47.25, "R3": 45.80, "M": 32.12},
    "M": {"L": 32.12, "C": 72.23, "N": 34.74},
    "N": {"C": 59.60, "M": 34.74, "R3": 81.93, "U": 65.11, "T": 62.14},
    "O": {"R2": 101.33, "P": 45.65, "Q": 46.43, "R3": 49.18, "S": 84.00},
    "P": {"O": 45.65},
    "Q": {"O": 46.43},
    "R": {"R3": 90.79},
    "S": {"O": 84.00},
    "T": {"N": 62.14, "R3": 64.74},
    "U": {"N": 65.11, "V": 41.42},
    "V": {"U": 41.42},
    "R1": {"G": 36.51, "F": 72.30, "H": 46.52},
    "R2": {"D": 69.39, "E": 53.27, "F": 92.04, "K": 40.37, "L": 47.25, "O": 101.33},
    "R3": {"L": 45.80, "N": 81.93, "O": 49.18, "R": 90.79, "T": 64.74},
    "VA": {"B": 11.58, "C": 29.69, "D": 11.58, "E": 36.06}
}

# ---------------- ALGORITMOS ----------------

def dijkstra(grafo, origen):
    dist = {n: float("inf") for n in grafo}
    prev = {n: None for n in grafo}
    visitados = set()

    dist[origen] = 0

    while len(visitados) < len(grafo):
        actual = None
        menor = float("inf")

        for n in grafo:
            if n not in visitados and dist[n] < menor:
                menor = dist[n]
                actual = n

        if actual is None:
            break

        visitados.add(actual)

        for vecino, peso in grafo[actual].items():
            nueva = dist[actual] + peso
            if nueva < dist[vecino]:
                dist[vecino] = nueva
                prev[vecino] = actual

    return dist, prev


def reconstruir(prev, origen, destino):
    camino = []
    actual = destino
    while actual:
        camino.insert(0, actual)
        actual = prev[actual]
    return camino if camino[0] == origen else []


def diametro_grafo(grafo):
    diam = 0
    extremos = ("", "")
    for o in grafo:
        dist, _ = dijkstra(grafo, o)
        for d in dist:
            if dist[d] != float("inf") and dist[d] > diam:
                diam = dist[d]
                extremos = (o, d)
    return diam, extremos

# ---------------- INTERFAZ ----------------

def calcular():
    origen = entry_origen.get().strip()
    destino = entry_destino.get().strip()

    if origen not in grafo or destino not in grafo:
        messagebox.showerror("Error", "Nodo inválido")
        return

    dist, prev = dijkstra(grafo, origen)
    camino = reconstruir(prev, origen, destino)
    diam, ext = diametro_grafo(grafo)

    salida.delete("1.0", tk.END)
    salida.insert(tk.END, f"Origen: {origen}\n")
    salida.insert(tk.END, f"Destino: {destino}\n\n")
    salida.insert(tk.END, f"Distancia mínima: {dist[destino]:.2f} m\n")
    salida.insert(tk.END, f"Camino más corto: {' -> '.join(camino)}\n\n")
    salida.insert(tk.END, f"Diámetro del grafo: {diam:.2f} m\n")
    salida.insert(tk.END, f"Nodos extremos: {ext[0]} y {ext[1]}")

# ---------------- VENTANA ----------------

root = tk.Tk()
root.title("Dijkstra - Grafo UPA")
root.geometry("1100x700")

canvas = tk.Canvas(root, width=700, height=600)
canvas.pack(side="left")

img = tk.PhotoImage(file="grafo.png")
canvas.create_image(0, 0, anchor="nw", image=img)

panel = tk.Frame(root)
panel.pack(side="right", padx=20)

tk.Label(panel, text="Nodo Origen").pack()
entry_origen = tk.Entry(panel)
entry_origen.pack()

tk.Label(panel, text="Nodo Destino").pack()
entry_destino = tk.Entry(panel)
entry_destino.pack()

tk.Button(panel, text="Calcular", command=calcular).pack(pady=10)

salida = tk.Text(panel, width=40, height=25)
salida.pack()

root.mainloop()
