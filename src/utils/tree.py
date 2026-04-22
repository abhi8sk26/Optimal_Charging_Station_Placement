import networkx as nx
from collections import deque

def create_bfs_tree(G, target):
    queue = deque([target])
    visited = set([target])
    bfs_tree = nx.DiGraph()
    bfs_tree.add_node(target)
    
    while queue:
        curr_node = queue.popleft()
        for neighbor in G.neighbors(curr_node):
            if neighbor not in visited:
                visited.add(neighbor)
                bfs_tree.add_edge(curr_node, neighbor)
                queue.append(neighbor)
    
    return bfs_tree