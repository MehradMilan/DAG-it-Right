import matplotlib.pyplot as plt
import networkx as nx

def visualize_graph(dag, title="Directed Acyclic Graph"):
    pos = nx.spring_layout(dag)
    node_weights = nx.get_node_attributes(dag, 'weight')
    edge_weights = {k: round(w, 2) for k, w in nx.get_edge_attributes(dag, 'weight').items()}

    plt.figure(figsize=(10, 6))
    nx.draw(dag, pos, with_labels=True, node_color="lightblue", node_size=700)
    nx.draw_networkx_edge_labels(dag, pos, edge_labels=edge_weights)
    plt.title(title)
    plt.show()