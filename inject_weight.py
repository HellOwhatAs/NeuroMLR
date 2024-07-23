from functools import reduce
import networkx, pickle
import os
from typing import List


def inject_weight(transformed_graph: networkx.DiGraph, dataset: str) -> bool:
    gs: List[networkx.DiGraph] = []
    if not os.path.exists(f'pkls/{dataset}'): return False
    for fname in os.listdir(f'pkls/{dataset}'):
        if not fname.endswith(".pkl"): continue
        with open(f'pkls/{dataset}/{fname}', 'rb') as f:
            gs.append(pickle.load(f))
    if len(gs) == 0: return False

    def func(g1: networkx.DiGraph, g2: networkx.DiGraph):
        for u, v in g1.edges:
            for key in g1[u][v]:
                g1[u][v][key] += g2[u][v][key]
        return g1

    g = reduce(func, gs[1:], gs[0].copy())

    for u, v in g.edges:
        transformed_graph[u][v]['average_weight'] = float('inf') if g[u][v]["count"] == 0 else g[u][v]["accumulated_weight"] / g[u][v]["count"]
    return True