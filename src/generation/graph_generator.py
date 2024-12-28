import networkx as nx

def generate_synthetic_graph(graph_type="barabasi_albert", n=100, param=3):
    if graph_type == "barabasi_albert":
        if not isinstance(param, int):
            raise ValueError("Parameter 'param' must be an integer for Barabási-Albert graph.")
        return nx.barabasi_albert_graph(n=n, m=int(param))
    elif graph_type == "watts_strogatz":
        return nx.watts_strogatz_graph(n=n, k=param, p=0.3)
    elif graph_type == "erdos_renyi":
        return nx.erdos_renyi_graph(n=n, p=param)
    else:
        raise ValueError("Invalid graph type.")

def convert_to_dag(G):
    dag = nx.DiGraph()
    for edge in G.edges():
        if edge[0] < edge[1]:
            dag.add_edge(edge[0], edge[1])
    return dag