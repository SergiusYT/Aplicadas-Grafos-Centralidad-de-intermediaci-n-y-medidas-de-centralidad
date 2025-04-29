import networkx as nx
import matplotlib.pyplot as plt

# Crear el grafo dirigido
G = nx.DiGraph()

# Añadir nodos (usuarios)
usuarios = ['Alice', 'Bridget', 'Charles', 'Doug', 'Mark', 'Michael']
G.add_nodes_from(usuarios)

# Añadir aristas (relaciones de gestión)
conexiones = [
    ('Alice', 'Bridget'),
    ('Alice', 'Charles'),
    ('Alice', 'Doug'),
    ('Mark', 'Alice'),
    ('Charles', 'Michael')
]
G.add_edges_from(conexiones)

# Dibujar el grafo
plt.figure(figsize=(8, 6))
pos = nx.spring_layout(G, seed=42)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1500, arrowstyle='-|>', arrowsize=20, font_size=12, font_weight='bold')
plt.title("Red Social de Usuarios", fontsize=16)
plt.show()

# --- Cálculos de Centralidades ---

# 1. Centralidad de Grado (entrada y salida)
grado_entrada = dict(G.in_degree())
grado_salida = dict(G.out_degree())

# 2. Centralidad de Cercanía
cercania = nx.closeness_centrality(G)

# 3. Centralidad de Eigenvector
try:
    eigenvector = nx.eigenvector_centrality(G)
except nx.PowerIterationFailedConvergence:
    eigenvector = {nodo: 0 for nodo in G.nodes()}
    print("\nAdvertencia: La centralidad de eigenvector no convergió, posiblemente por la estructura del grafo.")

# 4. Centralidad de Intermediación (Betweenness)
intermediacion = nx.betweenness_centrality(G, normalized=False)

# --- Mostrar los resultados ---

print("\nResultados de Centralidad por Usuario:\n")
print(f"{'Usuario':<10} {'Entrada':<8} {'Salida':<8} {'Cercanía':<10} {'Eigenvector':<12} {'Intermediación'}")
print("-" * 65)

for usuario in G.nodes():
    print(f"{usuario:<10} {grado_entrada[usuario]:<8} {grado_salida[usuario]:<8} {cercania[usuario]:<10.4f} {eigenvector[usuario]:<12.4f} {intermediacion[usuario]:.2f}")
