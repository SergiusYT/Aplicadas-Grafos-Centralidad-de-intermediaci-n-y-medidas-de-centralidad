import networkx as nx

def construir_grafo():
    G = nx.Graph()
    edges = [
        ('A','B'), ('A','C'), ('A','D'),
        ('B','E'), ('B','F'), ('C','F'), ('C','G'), ('D','G'), ('D','H1'),
        ('E','I'), ('F','J'), ('G','J'),
        ('I','K'), ('J','K'), ('H1','Z'), ('Z','K'),
        ('K','L'), ('K','M'), ('K','N'), ('L','H'), ('M','H'), ('N','H'),
        ('F','X'), ('X','Y'), ('Y','K'), ('G','W'), ('W','K'),
        # Agrega más complejidad:
        ('L','O'), ('O','P'), ('P','Q'), ('Q','R'), ('R','S'), ('S','T'),
        ('T','U'), ('U','V'), ('V','W'), ('Y','T'), ('M','R'), ('N','O')
    ]
    G.add_edges_from(edges)
    return G
