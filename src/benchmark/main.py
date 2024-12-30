from .heft import *
from .edf import *
from src.generation.graph_generator import generate_synthetic_graph, convert_to_dag
from src.generation.graph_annotator import annotate_graph

import matplotlib.pyplot as plt

# Function to run benchmarks
def benchmark_algorithms(graph_type ,graph_sizes, resources, algorithms):
    """
    Benchmark EDF and HEFT scheduling algorithms over various graph sizes.
    
    Parameters:
    - graph_sizes: List of integers representing the number of nodes in each graph.
    - resources: List of resource dictionaries with speed attributes.
    - algorithms: Dictionary with algorithm names as keys and functions as values.
    
    Returns:
    - results: Dictionary with algorithm names as keys and results as values.
    """
    results = {alg: {'makespan': [], 'utilization': []} for alg in algorithms.keys()}

    for size in graph_sizes:
        # Generate and annotate DAG
        dag = generate_synthetic_graph(graph_type, n=size, param=3)
        dag = convert_to_dag(dag)
        annotated_dag = annotate_graph(dag)
        
        for alg_name, alg_func in algorithms.items():
            schedule, makespan, utilization = alg_func(annotated_dag, resources)
            results[alg_name]['makespan'].append(makespan)
            avg_utilization = sum(utilization.values()) / len(utilization)
            results[alg_name]['utilization'].append(avg_utilization)

    return results

# Plotting function
def plot_results(gt, graph_sizes, results):
    """
    Plot makespan and resource utilization for given results.
    
    Parameters:
    - graph_sizes: List of graph sizes (number of nodes).
    - results: Dictionary with algorithm names as keys and results as values.
    """
    fig, axes = plt.subplots(2, 1, figsize=(10, 10))

    # Plot makespan
    for alg_name, metrics in results.items():
        axes[0].plot(graph_sizes, metrics['makespan'], label=f"{alg_name} Makespan")
    axes[0].set_title(str.upper(gt) + ": Makespan vs Graph Size")
    axes[0].set_xlabel("Graph Size (Number of Nodes)")
    axes[0].set_ylabel("Makespan")
    axes[0].legend()
    axes[0].grid()

    # Plot resource utilization
    for alg_name, metrics in results.items():
        axes[1].plot(graph_sizes, metrics['utilization'], label=f"{alg_name} Utilization")
    axes[1].set_title("Resource Utilization vs Graph Size")
    axes[1].set_xlabel("Graph Size (Number of Nodes)")
    axes[1].set_ylabel("Average Resource Utilization")
    axes[1].legend()
    axes[1].grid()

    plt.tight_layout()
    plt.show()

