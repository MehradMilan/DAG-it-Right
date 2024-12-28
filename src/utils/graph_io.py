import networkx as nx
import os

OUTPUT_DIR = os.getcwd()

def export_graph(dag, filename):
    nx.write_gml(dag, OUTPUT_DIR + filename)
    print(f"Graph saved to {filename}")

def import_graph(filename):
    return nx.read_gml(filename)
