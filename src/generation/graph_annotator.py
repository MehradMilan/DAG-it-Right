import random

def annotate_graph(dag):
    for node in dag.nodes():
        dag.nodes[node]['weight'] = random.randint(1, 10)
        dag.nodes[node]['num_cores'] = random.randint(1, 3) # GANG replication factor
    for u, v in dag.edges():
        dag.edges[u, v]['weight'] = random.uniform(0.1, 1.0)
    return dag
