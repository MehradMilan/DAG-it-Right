import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import argparse
from src.generation.graph_generator import generate_synthetic_graph, convert_to_dag
from src.generation.graph_annotator import annotate_graph
from src.utils.graph_io import export_graph
from src.utils.graph_visualizer import visualize_graph

def main():
    parser = argparse.ArgumentParser(description="DAG Scheduling Benchmarks CLI")
    parser.add_argument("--graph-type", type=str, required=True,
                        choices=["barabasi_albert", "watts_strogatz", "erdos_renyi"],
                        help="Type of graph to generate.")
    parser.add_argument("--nodes", type=int, default=100, help="Number of nodes.")
    parser.add_argument("--param", type=int, default=3, help="Graph model parameter.")
    parser.add_argument("--output", type=str, default="output_dag.gml", help="Output filename.")
    parser.add_argument("--visualize", action="store_true", help="Visualize the generated DAG.")
    
    args = parser.parse_args()

    try: 
        G = generate_synthetic_graph(graph_type=args.graph_type, n=args.nodes, param=args.param)
        dag = convert_to_dag(G)
        annotated_dag = annotate_graph(dag)

        export_graph(annotated_dag, args.output)  

        if args.visualize:
            visualize_graph(annotated_dag, title="Generated DAG")

    except ValueError as e:
        print(f"Error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
