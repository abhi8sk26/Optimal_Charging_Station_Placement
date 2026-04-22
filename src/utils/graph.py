import networkx as nx

def create_grid_graph(grid):
    row, col = grid.shape
    G = nx.Graph()
    direction = [(-1,0), (1,0), (0,-1), (0,1)]

    for i in range(row):
        for j in range(col):
            G.add_node((i, j))
            for a, b in direction:
                x = i + a
                y = j + b
                if x in range(row) and y in range(col):
                    G.add_edge((i, j), (x, y))
    return G