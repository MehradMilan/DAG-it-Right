import networkx as nx

def generate_synthetic_graph(graph_type="barabasi_albert", n=100, params={"m": 3, "k": 4, "p":0.1}):
    if graph_type == "barabasi_albert":
        return nx.barabasi_albert_graph(n=n, m=params.get("m", 3))
    elif graph_type == "watts_strogatz":
        return nx.watts_strogatz_graph(n=n, k=params.get("k", 4), p=params.get("p", 0.1))
    elif graph_type == "erdos_renyi":
        return nx.erdos_renyi_graph(n=n, p=params.get("p", 0.1))

def convert_to_dag(G):
    dag = nx.DiGraph()
    for edge in G.edges():
        if edge[0] < edge[1]:
            dag.add_edge(edge[0], edge[1])
    return dag