import eel
import networkx as nx
from grafo import construir_grafo

# Iniciar Eel
eel.init('web')

G = construir_grafo()
infectados = {'A'}
bloqueados = set()
objetivo = 'H'

# 💡 Fijar posiciones UNA SOLA VEZ
posiciones = nx.spring_layout(G, seed=42)

@eel.expose
def obtener_estado():
    nodos = []
    for nodo in G.nodes:
        color = 'green'
        if nodo in infectados:
            color = 'red'
        elif any(vecino in infectados for vecino in G.neighbors(nodo)):
            color = 'orange'
        nodos.append({
            'id': nodo,
            'x': posiciones[nodo][0],
            'y': posiciones[nodo][1],
            'color': color
        })
    edges = [{'from': u, 'to': v} for u, v in G.edges]
    return {'nodes': nodos, 'edges': edges}


# Calcula una vez en la carga del grafo
centralidad_grado = nx.degree_centrality(G)
centralidad_intermediacion = nx.betweenness_centrality(G)

@eel.expose
def obtener_centralidades():
    data = {}
    for nodo in G.nodes:
        data[nodo] = {
            'grado': round(centralidad_grado[nodo], 3),
            'intermediacion': round(centralidad_intermediacion[nodo], 3)
        }
    return data



@eel.expose
def actualizar_posicion(nodo, x, y):
    posiciones[nodo] = (x / 500, y / 500)  # Divide por 500 para mantener la escala original


puntuacion = 0

@eel.expose
def siguiente_paso(bloqueo=None):
    global puntuacion
    if bloqueo and bloqueo in G.nodes:
        if centralidad_intermediacion[bloqueo] > 0.1:
            puntuacion += 10
        else:
            puntuacion -= 5
        G.remove_node(bloqueo)
        bloqueados.add(bloqueo)

    # Propagación...
    nuevos = set()
    for nodo in infectados:
        nuevos.update([v for v in G.neighbors(nodo) if v not in infectados and v not in bloqueados])
    infectados.update(nuevos)

    if objetivo in infectados:
        puntuacion -= 20
        return "hackeo"
    if not nuevos:
        puntuacion += 15
        return "detenido"
    return "continuar"

@eel.expose
def obtener_estadisticas():
    return {
        'infectados': len(infectados),
        'bloqueados': len(bloqueados),
        'puntuacion': puntuacion,
        'nodo_critico': max(centralidad_intermediacion, key=centralidad_intermediacion.get)
    }

eel.start('index.html', size=(1000, 800))
