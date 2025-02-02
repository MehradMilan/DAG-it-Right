import sys
import os
import random
import argparse
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.generation.graph_generator import generate_synthetic_graph, convert_to_dag
from src.generation.graph_annotator import annotate_graph
from src.utils.graph_io import export_graph, load_graph
from src.utils.graph_visualizer import visualize_graph
from src.utils.downloader import read_urls, download_dataset, download_all
from src.benchmark.heft import heft_schedule, visualize_schedule
from src.benchmark.edf import edf_schedule, visualize_edf
from src.benchmark.heft_star import heft_star_schedule
from src.benchmark.main import (
    benchmark_algorithms_with_params,
    plot_comparison_per_network,
    plot_comparison_per_algorithm,
    plot_average_per_network,
)
from src.benchmark.plotter import (
    plot_gang_impact_on_makespan,
    plot_gang_task_percentage,
    plot_makespan_comparison,
    plot_utilization_comparison,
    plot_core_utilization_distribution,
    plot_scheduling_efficiency,
    plot_topology_influence_on_scheduling,
)


def main():
    parser = argparse.ArgumentParser(description="DAG Scheduling Benchmarks CLI")

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    gen_parser = subparsers.add_parser("generate", help="Generate a synthetic graph")
    gen_parser.add_argument(
        "--graph-type",
        type=str,
        required=True,
        choices=["barabasi_albert", "watts_strogatz", "erdos_renyi"],
        help="Type of graph to generate.",
    )
    gen_parser.add_argument("--nodes", type=int, default=100, help="Number of nodes.")
    gen_parser.add_argument(
        "--params",
        type=str,
        default='{"m": 3}',
        help='Graph model parameters as a JSON string (e.g., \'{"m": 3, "p": 0.1}\')',
    )
    gen_parser.add_argument(
        "--output", type=str, default="output_dag.gml", help="Output filename."
    )
    gen_parser.add_argument(
        "--visualize", action="store_true", help="Visualize the generated DAG."
    )
    gen_parser.add_argument(
        "--benchmark", action="store_true", help="Print benchmark result."
    )
    gen_parser.add_argument(
        "--num-proc", type=int, default=3, help="Number of processors."
    )

    download_parser = subparsers.add_parser("download", help="Download datasets")
    download_parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="Type of dataset to download (e.g., social_networks, biological_networks).",
    )

    benchmark_parser = subparsers.add_parser(
        "benchmark", help="Benchmark Scheduling Algorithm"
    )
    benchmark_parser.add_argument(
        "--input", type=str, required=True, help="Graph input"
    )
    benchmark_parser.add_argument(
        "--num-proc", type=int, default=3, help="Number of processors."
    )
    benchmark_parser.add_argument(
        "--visualize", action="store_true", help="Visualize the generated DAG."
    )

    process_parser = subparsers.add_parser("process", help="Process a single dataset")
    process_parser.add_argument(
        "--input", type=str, required=True, help="Path to the input dataset file."
    )
    process_parser.add_argument(
        "--format",
        type=str,
        required=True,
        choices=["edgelist", "mtx", "gml"],
        help="Format of the input dataset.",
    )
    process_parser.add_argument(
        "--output", type=str, required=True, help="Path to save the processed DAG."
    )

    batch_parser = subparsers.add_parser(
        "batch-process", help="Process multiple datasets"
    )
    batch_parser.add_argument(
        "--type",
        type=str,
        required=True,
        help="Type of datasets to process (e.g., social_networks, biological_networks).",
    )
    batch_benchmark = subparsers.add_parser(
        "batch-benchmark", help="Benchmark multiple networks"
    )

    args = parser.parse_args()

    if args.command == "benchmark":
        processors = [
            {"speed": random.choice([0.5, 1.0, 1.5, 2.0, 2.5])}
            for _ in range(args.num_proc)
        ]
        saved_graph = load_graph(args.input)
        visualize_schedule(heft_star_schedule(saved_graph, processors)[0])
        visualize_schedule(heft_schedule(saved_graph, processors)[0])
        visualize_schedule(edf_schedule(saved_graph, processors)[0])

    if args.command == "batch-benchmark":
        param_sets = {
            "barabasi_albert": [{"m": 3}, {"m": 5}, {"m": 8}],
            "watts_strogatz": [
                {"k": 4, "p": 0.1},
                {"k": 6, "p": 0.3},
                {"k": 8, "p": 0.5},
            ],
            "erdos_renyi": [{"p": 0.1}, {"p": 0.5}, {"p": 0.9}, {"p": 1.0}],
        }

        graph_sizes = {
            "barabasi_albert": list(range(100, 1100, 100)),
            "watts_strogatz": list(range(10, 200, 20)),
            "erdos_renyi": list(range(10, 200, 20)),
        }

        resources = [{"speed": 1.0}, {"speed": 1.5}, {"speed": 0.5}]

        algorithms = {
            "EDF": edf_schedule,
            "HEFT": heft_schedule,
            "HEFT*": heft_star_schedule,
        }

        for graph_type, params in param_sets.items():
            print(f"Running benchmarks for {graph_type}...")
            sizes = graph_sizes[graph_type]
            results = benchmark_algorithms_with_params(
                graph_type, sizes, params, resources, algorithms
            )
            plot_comparison_per_network(graph_type, sizes, results, params)

        all_results = {}
        graph_sizes = {
            "barabasi_albert": list(range(10, 200, 20)),
            "watts_strogatz": list(range(10, 200, 20)),
            "erdos_renyi": list(range(10, 200, 20)),
        }
        for graph_type, params in param_sets.items():
            print(f"Running benchmarks for {graph_type}...")
            sizes = graph_sizes[graph_type]
            results = benchmark_algorithms_with_params(
                graph_type, sizes, params, resources, algorithms
            )
            all_results[graph_type] = results

        print("Plotting comparison across algorithms...")
        plot_comparison_per_algorithm(graph_sizes, all_results, param_sets, algorithms, param_sets.keys())

        print("Plotting averaged results across all parameters...")
        plot_average_per_network(graph_sizes, all_results, list(algorithms.keys()), param_sets.keys())

        print("Plotting Makespan Comparison Across All Networks...")
        plot_makespan_comparison(graph_sizes, all_results, param_sets)

        print("Plotting Utilization Comparison Across All Networks...")
        plot_utilization_comparison(graph_sizes, all_results, param_sets)

        print("Plotting GANG Task Percentage Across All Networks...")
        plot_gang_task_percentage(graph_sizes, all_results, param_sets)

        print("Plotting GANG Task Impact on Makespan...")
        plot_gang_impact_on_makespan(graph_sizes, all_results, param_sets)

        print("Plotting Scheduling Efficiency Across DAG Models...")
        plot_scheduling_efficiency(graph_sizes, all_results, param_sets)

        print("Plotting Core Utilization Distribution...")
        plot_core_utilization_distribution(graph_sizes, all_results, param_sets)

        print("Plotting Network Topology Influence on Scheduling...")
        plot_topology_influence_on_scheduling(graph_sizes, all_results, param_sets)

    if args.command == "generate":
        try:
            try:
                params = json.loads(args.params)
            except json.JSONDecodeError:
                print("Error: Invalid JSON format for --params.")
                exit(1)

            G = generate_synthetic_graph(
                graph_type=args.graph_type, n=args.nodes, params=params
            )
            dag = convert_to_dag(G)
            annotated_dag = annotate_graph(dag)

            export_graph(annotated_dag, args.output, is_generated=True)

            if args.visualize:
                visualize_graph(annotated_dag, title="Generated DAG")

            if args.benchmark:
                resources = [
                    {"speed": random.choice([0.5, 1.0, 1.5, 2.0, 2.5])}
                    for _ in range(args.num_proc)
                ]
                visualize_schedule(heft_schedule(annotated_dag, resources)[0])
                visualize_schedule(edf_schedule(annotated_dag, resources)[0])

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
                print(
                    f"Error: Input file '{input_file}' not found. Please download it first."
                )
                continue
            print(f"Processing {dataset['name']}...")
            G = load_graph(input_file, dataset["format"])
            dag = convert_to_dag(G)
            annotated_dag = annotate_graph(dag)
            export_graph(annotated_dag, output_file, is_generated=False)


if __name__ == "__main__":
    main()
