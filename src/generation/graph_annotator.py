import random

def annotate_graph(dag):
    num_cores = [1, 2, 3]
    weights = [0.7, 0.2, 0.1]  # Adjust weights to increase GANG tasks count
    for node in dag.nodes():
        dag.nodes[node]['weight'] = random.randint(1, 10)
        dag.nodes[node]['num_cores'] = random.choices(num_cores, weights, k=1)[0] # GANG tasks replication factor
    for u, v in dag.edges():
        dag.edges[u, v]['weight'] = random.uniform(0.1, 1.0)
    return dag
