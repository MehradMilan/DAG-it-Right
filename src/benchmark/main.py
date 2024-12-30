from .heft import *
from .edf import *
from src.generation.graph_generator import generate_synthetic_graph, convert_to_dag
from src.generation.graph_annotator import annotate_graph

import matplotlib.pyplot as plt

def benchmark_algorithms_with_params(graph_type, graph_sizes, param_sets, resources, algorithms):
    results = {
        alg: {str(params): {'makespan': [], 'utilization': []} for params in param_sets}
        for alg in algorithms.keys()
    }

    for size in graph_sizes:
        for params in param_sets:
            try:
                dag = generate_synthetic_graph(graph_type, n=size, params=params)
                dag = convert_to_dag(dag)
                annotated_dag = annotate_graph(dag)

                for alg_name, alg_func in algorithms.items():
                    schedule, makespan, utilization = alg_func(annotated_dag, resources)
                    results[alg_name][str(params)]['makespan'].append(makespan)
                    avg_utilization = sum(utilization.values()) / len(utilization)
                    results[alg_name][str(params)]['utilization'].append(avg_utilization)
            except ValueError as e:
                print(f"Skipping graph with size={size} and params={params} due to: {e}")

    return results

def plot_comparison_per_network(graph_type, graph_sizes, results, param_sets):
    fig, axes = plt.subplots(2, len(param_sets), figsize=(15, 8), sharey="row")
    
    for i, params in enumerate(param_sets):
        for alg_name, metrics in results.items():
            axes[0, i].plot(graph_sizes, metrics[str(params)]['makespan'], label=f"{alg_name}")
            axes[1, i].plot(graph_sizes, metrics[str(params)]['utilization'], label=f"{alg_name}")
        
        axes[0, i].set_title(f"{graph_type.upper()} (Params: {params})")
        axes[0, i].set_xlabel("Graph Size (Nodes)")
        axes[0, i].set_ylabel("Makespan")
        axes[0, i].grid()
        axes[1, i].set_xlabel("Graph Size (Nodes)")
        axes[1, i].set_ylabel("Resource Utilization")
        axes[1, i].grid()
    
    axes[0, 0].legend()
    axes[1, 0].legend()
    plt.tight_layout()
    plt.show()

def plot_comparison_per_algorithm(graph_sizes, results, param_sets, algorithms, network_models):
    fig, axes = plt.subplots(2, len(algorithms), figsize=(15, 8), sharey="row")

    for i, alg_name in enumerate(algorithms):
        for graph_type in network_models:
            for params in param_sets[graph_type]:
                param_str = str(params)
                if graph_type in results and alg_name in results[graph_type] and param_str in results[graph_type][alg_name]:
                    axes[0, i].plot(
                        graph_sizes[graph_type],
                        results[graph_type][alg_name][param_str]['makespan'],
                        label=f"{graph_type} (Params: {params})",
                        linestyle='-', marker='o'
                    )
                    axes[1, i].plot(
                        graph_sizes[graph_type],
                        results[graph_type][alg_name][param_str]['utilization'],
                        label=f"{graph_type} (Params: {params})",
                        linestyle='--', marker='x'
                    )
        
        axes[0, i].set_title(f"{alg_name} - Makespan")
        axes[0, i].set_xlabel("Graph Size (Nodes)")
        axes[0, i].set_ylabel("Makespan")
        axes[0, i].grid()
        axes[1, i].set_title(f"{alg_name} - Resource Utilization")
        axes[1, i].set_xlabel("Graph Size (Nodes)")
        axes[1, i].set_ylabel("Utilization")
        axes[1, i].grid()
    
    axes[0, 0].legend()
    axes[1, 0].legend()
    plt.tight_layout()
    plt.show()

def plot_average_per_network(graph_sizes, results, algorithms, network_models):
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))

    for row, metric in enumerate(["makespan", "utilization"]):
        for col, alg_name in enumerate(algorithms):
            for graph_type in network_models:
                avg_metric = {size: 0 for size in graph_sizes[graph_type]}
                count = 0

                for param_str, metrics in results[graph_type][alg_name].items():
                    count += 1
                    for i, size in enumerate(graph_sizes[graph_type]):
                        avg_metric[size] += metrics[metric][i]

                avg_metric = {size: value / count for size, value in avg_metric.items()}

                axes[row, col].plot(
                    graph_sizes[graph_type],
                    list(avg_metric.values()),
                    label=f"{graph_type}",
                    marker='o'
                )

            axes[row, col].set_title(f"{alg_name} - {metric.capitalize()}")
            axes[row, col].set_xlabel("Graph Size (Nodes)")
            if metric == "makespan":
                axes[row, col].set_ylabel("Average Makespan")
            else:
                axes[row, col].set_ylabel("Average Utilization")
            axes[row, col].grid()
            axes[row, col].legend()

    plt.tight_layout()
    plt.show()
