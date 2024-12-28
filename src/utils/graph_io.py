import networkx as nx

OUTPUT_DIR = "data/output/"

def export_graph(dag, filename):
    nx.write_gml(dag, OUTPUT_DIR + filename)
    print(f"Graph saved to {filename}")

def import_graph(filename):
    return nx.read_gml(filename)
