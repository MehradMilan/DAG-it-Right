import networkx as nx
import os

OUTPUT_DIR = os.getcwd() + '/data/output/graphs/'

def export_graph(dag, filename, is_generated=True):
    if is_generated:
        save_address =  OUTPUT_DIR + 'generated/'
    else:
        save_address =  OUTPUT_DIR + 'dataset/'
    os.makedirs(os.path.dirname(save_address), exist_ok=True)
    nx.write_gml(dag, save_address + filename)
    print(f"Graph saved to {filename}")

def load_graph(file_path, file_format="gml"):
    if file_format == "edgelist":
        return nx.read_edgelist(file_path)
    elif file_format == "mtx":
        return nx.read_graphml(file_path)
    elif file_format == "gml":
        return nx.read_gml(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_format}")