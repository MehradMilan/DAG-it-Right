import sys
import os
import random
import argparse

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generation.graph_generator import generate_synthetic_graph, convert_to_dag
from src.generation.graph_annotator import annotate_graph
from src.utils.graph_io import export_graph, load_graph
from src.utils.graph_visualizer import visualize_graph
from src.utils.downloader import read_urls, download_dataset, download_all
from src.benchmark.heft import heft_schedule, visualize_schedule


def main():
    parser = argparse.ArgumentParser(description="DAG Scheduling Benchmarks CLI")
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    gen_parser = subparsers.add_parser("generate", help="Generate a synthetic graph")
    gen_parser.add_argument("--graph-type", type=str, required=True,
                             choices=["barabasi_albert", "watts_strogatz", "erdos_renyi"],
                             help="Type of graph to generate.")
    gen_parser.add_argument("--nodes", type=int, default=100, help="Number of nodes.")
    gen_parser.add_argument("--param", type=int, default=3, help="Graph model parameter.")
    gen_parser.add_argument("--output", type=str, default="output_dag.gml", help="Output filename.")
    gen_parser.add_argument("--visualize", action="store_true", help="Visualize the generated DAG.")
    gen_parser.add_argument("--benchmark", action="store_true", help="Print benchmark result.")
    gen_parser.add_argument("--num-proc", type=int, default=3, help="Number of processors.")

    download_parser = subparsers.add_parser("download", help="Download datasets")
    download_parser.add_argument("--type", type=str, required=True,
                                  help="Type of dataset to download (e.g., social_networks, biological_networks).")
    
    benchmark_parser = subparsers.add_parser("benchmark", help="Benchmark Scheduling Algorithm")
    benchmark_parser.add_argument("--input", type=str, required=True,
                                  help="Graph input")
    benchmark_parser.add_argument("--num-proc", type=int, default=3, help="Number of processors.")
    benchmark_parser.add_argument("--visualize", action="store_true", help="Visualize the generated DAG.")
    

    process_parser = subparsers.add_parser("process", help="Process a single dataset")
    process_parser.add_argument("--input", type=str, required=True, help="Path to the input dataset file.")
    process_parser.add_argument("--format", type=str, required=True, choices=["edgelist", "mtx", "gml"],
                                 help="Format of the input dataset.")
    process_parser.add_argument("--output", type=str, required=True, help="Path to save the processed DAG.")

    batch_parser = subparsers.add_parser("batch-process", help="Process multiple datasets")
    batch_parser.add_argument("--type", type=str, required=True,
                               help="Type of datasets to process (e.g., social_networks, biological_networks).")

    args = parser.parse_args()

    if args.command == "benchmark":
        processors = [{'speed': random.choice([0.5, 1.0, 1.5, 2.0, 2.5])} for _ in range(args.num_proc)]
        saved_graph = load_graph(args.input)
        visualize_schedule(heft_schedule(saved_graph, processors))

    if args.command == "generate":
        try:
            G = generate_synthetic_graph(graph_type=args.graph_type, n=args.nodes, param=args.param)
            dag = convert_to_dag(G)
            annotated_dag = annotate_graph(dag)

            export_graph(annotated_dag, args.output, is_generated=True)

            if args.visualize:
                visualize_graph(annotated_dag, title="Generated DAG")

            if args.benchmark:
                processors = [{'speed': random.choice([0.5, 1.0, 1.5, 2.0, 2.5])} for _ in range(args.num_proc)]
                visualize_schedule(heft_schedule(annotated_dag, processors))

        except ValueError as e:
            print(f"Error: {e}")
            exit(1)

    elif args.command == "download":
        urls = read_urls()
        if args.type not in urls:
            print(f"Error: Dataset type '{args.type}' not found in urls.json.")
            return
        download_all(urls[args.type], output_dir="data/input/dataset")

    elif args.command == "process":
        if not os.path.exists(args.input):
            print(f"Error: Input file '{args.input}' does not exist.")
            return
        G = load_graph(args.input, args.format)
        dag = convert_to_dag(G)
        annotated_dag = annotate_graph(dag)
        export_graph(annotated_dag, args.output, is_generated=False)

    elif args.command == "batch-process":
        urls = read_urls()
        if args.type not in urls:
            print(f"Error: Dataset type '{args.type}' not found in urls.json.")
            return
        for dataset in urls[args.type]:
            input_file = f"data/input/dataset/{os.path.basename(dataset['name'])}.txt"
            output_file = f"{dataset['name'].replace(' ', '_')}_dag.gml"
            if not os.path.exists(input_file):
                print(f"Error: Input file '{input_file}' not found. Please download it first.")
                continue
            print(f"Processing {dataset['name']}...")
            G = load_graph(input_file, dataset['format'])
            dag = convert_to_dag(G)
            annotated_dag = annotate_graph(dag)
            export_graph(annotated_dag, output_file, is_generated=False)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()