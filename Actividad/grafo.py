import networkx as nx

def construir_grafo():
    G = nx.Graph()

    # Núcleos principales: Centros de datos / servidores críticos
    edges = [
        ('A1','A2'), ('A1','A3'), ('A2','A4'), ('A3','A5'), ('A4','A6'), ('A5','A7'), 
        ('A6','A8'), ('A7','A9'), ('A8','A10'), ('A9','A11'), ('A10','A12'), ('A11','A13'),

        # Clúster 1
        ('A2','B1'), ('B1','B2'), ('B2','B3'), ('B3','B4'), ('B4','B5'),
        ('B1','B6'), ('B6','B7'), ('B7','B8'), ('B8','B9'), ('B9','B10'),
        ('B5','B11'), ('B11','B12'),

        # Clúster 2
        ('A3','C1'), ('C1','C2'), ('C2','C3'), ('C3','C4'), ('C4','C5'),
        ('C2','C6'), ('C6','C7'), ('C7','C8'), ('C8','C9'), ('C9','C10'),

        # Clúster 3
        ('A4','D1'), ('D1','D2'), ('D2','D3'), ('D3','D4'), ('D4','D5'),
        ('D2','D6'), ('D6','D7'), ('D7','D8'), ('D8','D9'), ('D9','D10'),

        # Clúster 4
        ('A5','E1'), ('E1','E2'), ('E2','E3'), ('E3','E4'), ('E4','E5'),
        ('E2','E6'), ('E6','E7'), ('E7','E8'), ('E8','E9'), ('E9','E10'),

        # Backbone redundante
        ('B12','C10'), ('C10','D10'), ('D10','E10'),
        ('B6','D6'), ('C4','E4'), ('A12','E9'),

        # Caminos extras para enredos
        ('A6','F1'), ('F1','F2'), ('F2','F3'), ('F3','F4'), ('F4','F5'),
        ('F3','F6'), ('F6','F7'), ('F7','F8'), ('F8','F9'), ('F9','F10'),

        # Más ramas de complejidad
        ('A7','G1'), ('G1','G2'), ('G2','G3'), ('G3','G4'), ('G4','G5'),
        ('G3','G6'), ('G6','G7'), ('G7','G8'), ('G8','G9'), ('G9','G10'),

        ('A9','H1'), ('H1','H2'), ('H2','H3'), ('H3','H4'), ('H4','H5'),

        ('H5','Z'),

        # Más conexiones cruzadas para hacerlo más real
        ('F10','H2'), ('E10','F5'), ('C7','H3'), ('G5','H1'), ('D4','G2'), ('B3','E1'),

        # Subnet de trampas
        ('T1','T2'), ('T2','T3'), ('T3','T4'), ('T4','T5'),
        ('T3','T6'), ('T6','T7'), ('T7','T8'), ('T8','T9'), ('T9','T10'),

        ('T5','D10'), ('T10','H4'), ('T1','A1'), ('T6','B10'),

        # Más servidores aislados pero críticos
        ('X1','X2'), ('X2','X3'), ('X3','X4'), ('X4','X5'), 
        ('X5','Z'), ('X3','F1'),

        # Cadenas adicionales (para visualización inmensa)
        ('Y1','Y2'), ('Y2','Y3'), ('Y3','Y4'), ('Y4','Y5'),
        ('Y5','Y6'), ('Y6','Y7'), ('Y7','Y8'), ('Y8','Y9'), ('Y9','Y10'),

        ('Y1','B2'), ('Y10','G9')
    ]

    G.add_edges_from(edges)
    return G
