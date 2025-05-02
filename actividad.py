"""                         Atrapa al Hacker
Imagina que eres parte de un equipo de ciberseguridad encargado de proteger una red de servidores
de una empresa internacional. Un hacker ha logrado infiltrarse y está intentando enviar un mensaje
secreto desde un servidor inicial (A) hasta su contacto final (H), pasando por diferentes nodos intermedios.
Cada nodo representa un servidor que podría estar comprometido. Tu misión es identificar qué servidor (nodo)
es el punto clave de la red: aquel que si se desconecta, impediría que el mensaje llegue a su destino.

Para lograrlo, el juego se desarrollara así:

  1. Se muestra en pantalla una red de servidores (grafo) con conexiones representadas visualmente.

  2. El mensaje del hacker debe ir desde el servidor A hasta el servidor H.

  3. Cada uno eligira un nodo que considera crítico: el que al eliminarlo cortaría la comunicación.

  4. El programa calcula y muestra la centralidad de intermediación de todos los nodos, explicando cuál era realmente más importante.

  5. Luego se elimina el nodo elegido y se verifica si el hacker aún puede comunicarse o si la red quedó bloqueada.



"""
import networkx as nx
import matplotlib.pyplot as plt
import random

G = nx.Graph()
edges = [
    # Entrada con bifurcaciones
    ('A','B'), ('A','C'), ('A','D'),
    ('B','E'), ('B','F'), ('C','F'), ('C','G'), ('D','G'), ('D','H1'),
    # Camino intermedio alternativo
    ('E','I'), ('F','J'), ('G','J'),
    # Convergencia en K
    ('I','K'), ('J','K'),
    # Nodo trampa
    ('H1','Z'), ('Z','K'),
    # Salidas desde K
    ('K','L'), ('K','M'), ('K','N'),
    # Final hacia H
    ('L','H'), ('M','H'), ('N','H'),
    # Rutas engañosas
    ('F','X'), ('X','Y'), ('Y','K'),
    ('G','W'), ('W','K'),
    # Caminos distractores
    ('B','P'), ('P','Q'), ('Q','R'), ('R','S'), ('S','K'),
    ('J','T'), ('T','U'), ('U','V'), ('V','K'),
    ('M','AA'), ('AA','AB'), ('AB','AC'), ('AC','K'),
    ('Z','AD'), ('AD','AE'), ('AE','AF'), ('AF','K'),
]
G.add_edges_from(edges)

# Visualización inicial
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(18,14))
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=1300, font_size=12, edge_color='gray')
plt.title("Red de servidores (A a H)")
plt.show()

# Calcular y mostrar centralidad de intermediación en orden aleatorio
betweenness = nx.betweenness_centrality(G)
items = list(betweenness.items())
random.shuffle(items)

print("\n🔍 Centralidad de intermediación de los nodos (en orden aleatorio):")
for node, value in items:
    print(f" - Nodo {node}: {value:.4f}")

# Elección del jugador
eleccion = input("\n🤔 ¿Qué nodo crees que es más importante para impedir el mensaje del hacker? Escribe un nodo (A-Z u otros): ").upper()

if eleccion in betweenness:
    print(f"\n📌 Elegiste el nodo {eleccion} con una centralidad de {betweenness[eleccion]:.4f}")
else:
    print("\n❌ Ese nodo no existe en la red.")
    exit()

# Simular desconexión y verificar comunicación
G_removed = G.copy()
G_removed.remove_node(eleccion)
print(f"\n🚫 Nodo {eleccion} eliminado de la red...")

if nx.has_path(G_removed, 'A', 'H'):
    print("📡 El hacker AÚN puede comunicarse con su contacto final.")
else:
    print("✅ ¡El mensaje ha sido bloqueado! No hay ruta disponible de A a H.")

# Visualización tras eliminación
plt.figure(figsize=(18,14))
nx.draw(G_removed, pos, with_labels=True, node_color='lightcoral', node_size=1300, font_size=12, edge_color='gray')
plt.title("Red tras eliminación del nodo")
plt.show()