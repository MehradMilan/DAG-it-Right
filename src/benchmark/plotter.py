import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np


def plot_makespan_comparison(graph_sizes, results, param_sets):
    plt.figure(figsize=(10, 6))

    all_data = []

    for graph_type in graph_sizes:
        for alg_name in results[graph_type]:
            for params in param_sets[graph_type]:
                param_str = str(params)
                if param_str in results[graph_type][alg_name]:
                    makespan_values = results[graph_type][alg_name][param_str][
                        "makespan"
                    ]
                    for value in makespan_values:
                        all_data.append([graph_type, alg_name, value])

    df = pd.DataFrame(all_data, columns=["Graph Type", "Algorithm", "Makespan"])
    sns.boxplot(x="Graph Type", y="Makespan", hue="Algorithm", data=df)

    plt.xlabel("Graph Type")
    plt.ylabel("Makespan")
    plt.title("Makespan Comparison Across Algorithms")
    plt.legend()
    plt.grid()
    plt.show()


def plot_utilization_comparison(graph_sizes, results, param_sets):
    plt.figure(figsize=(10, 6))

    all_data = []

    for graph_type in graph_sizes:
        for alg_name in results[graph_type]:
            for params in param_sets[graph_type]:
                param_str = str(params)
                if param_str in results[graph_type][alg_name]:
                    utilization_values = results[graph_type][alg_name][param_str][
                        "utilization"
                    ]
                    avg_utilization = sum(utilization_values) / len(utilization_values)
                    all_data.append([graph_type, alg_name, avg_utilization])

    df = pd.DataFrame(all_data, columns=["Graph Type", "Algorithm", "Utilization"])
    pivot_table = df.pivot_table(
        index="Graph Type", columns="Algorithm", values="Utilization", aggfunc="mean"
    )

    sns.heatmap(pivot_table, annot=True, cmap="coolwarm", fmt=".2f")

    plt.xlabel("Algorithm")
    plt.ylabel("Graph Type")
    plt.title("Resource Utilization Heatmap")
    plt.show()


def plot_gang_task_percentage(graph_sizes, results, param_sets):
    plt.figure(figsize=(10, 6))

    gang_data = {alg: [] for alg in ["EDF", "HEFT", "HEFT*"]}

    for graph_type in graph_sizes:
        for alg_name in results[graph_type]:
            avg_gang = []
            for params in param_sets[graph_type]:
                param_str = str(params)
                if param_str in results[graph_type][alg_name]:
                    gang_values = results[graph_type][alg_name][param_str][
                        "gang_percentage"
                    ]
                    avg_gang.append(sum(gang_values) / len(gang_values))
            if avg_gang:
                gang_data[alg_name].append(sum(avg_gang) / len(avg_gang))

    labels = list(graph_sizes.keys())
    x = np.arange(len(labels))

    plt.bar(x, gang_data["EDF"], width=0.3, label="EDF", alpha=0.7)
    plt.bar(x + 0.3, gang_data["HEFT"], width=0.3, label="HEFT", alpha=0.7)
    plt.bar(x + 0.6, gang_data["HEFT*"], width=0.3, label="HEFT*", alpha=0.7)

    plt.xticks(x + 0.3, labels)
    plt.xlabel("Graph Type")
    plt.ylabel("Percentage of GANG Tasks")
    plt.title("GANG Task Distribution Across Algorithms")
    plt.legend()
    plt.show()


def plot_gang_impact_on_makespan(graph_sizes, results, param_sets):
    plt.figure(figsize=(10, 6))

    all_data = []

    for graph_type in graph_sizes:
        for alg_name in results[graph_type]:
            for params in param_sets[graph_type]:
                param_str = str(params)
                if param_str in results[graph_type][alg_name]:
                    gang_values = results[graph_type][alg_name][param_str][
                        "gang_percentage"
                    ]
                    makespan_values = results[graph_type][alg_name][param_str][
                        "makespan"
                    ]

                    if gang_values and makespan_values:
                        avg_gang_percentage = sum(gang_values) / len(gang_values)
                        avg_makespan = sum(makespan_values) / len(makespan_values)
                        all_data.append([alg_name, avg_gang_percentage, avg_makespan])

    df = pd.DataFrame(all_data, columns=["Algorithm", "GANG Percentage", "Makespan"])

    sns.lmplot(
        x="GANG Percentage",
        y="Makespan",
        hue="Algorithm",
        data=df,
        markers=["o", "s", "D"],
        height=6,
        aspect=1.2,
    )

    plt.xlabel("Percentage of GANG Tasks")
    plt.ylabel("Makespan")
    plt.title("Impact of GANG Tasks on Makespan (Regression)")
    plt.show()


def plot_scheduling_efficiency(graph_sizes, results, param_sets):
    plt.figure(figsize=(10, 6))

    all_data = []

    for graph_type in graph_sizes:
        for alg_name in results[graph_type]:
            for params in param_sets[graph_type]:
                param_str = str(params)
                if param_str in results[graph_type][alg_name]:
                    makespan_values = results[graph_type][alg_name][param_str][
                        "makespan"
                    ]
                    avg_makespan = sum(makespan_values) / len(makespan_values)
                    all_data.append([graph_type, alg_name, avg_makespan])

    df = pd.DataFrame(all_data, columns=["Graph Type", "Algorithm", "Makespan"])

    pivot_table = df.pivot_table(
        index="Graph Type", columns="Algorithm", values="Makespan", aggfunc="mean"
    )

    sns.heatmap(pivot_table, annot=True, cmap="coolwarm", fmt=".2f")

    plt.xlabel("Algorithm")
    plt.ylabel("Graph Type")
    plt.title("Scheduling Efficiency Across DAG Models")
    plt.show()


import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt


def plot_core_utilization_distribution(graph_sizes, results, param_sets):
    plt.figure(figsize=(10, 6))

    all_data = []

    for graph_type in graph_sizes:
        for alg_name in results[graph_type]:
            for params in param_sets[graph_type]:
                param_str = str(params)
                if param_str in results[graph_type][alg_name]:
                    utilization_values = results[graph_type][alg_name][param_str][
                        "utilization"
                    ]
                    for value in utilization_values:
                        all_data.append([graph_type, alg_name, value])

    df = pd.DataFrame(all_data, columns=["Graph Type", "Algorithm", "Utilization"])

    sns.boxplot(x="Algorithm", y="Utilization", hue="Graph Type", data=df)

    plt.xlabel("Algorithm")
    plt.ylabel("Core Utilization")
    plt.title("Core Utilization Across Algorithms")
    plt.legend()
    plt.show()


def plot_topology_influence_on_scheduling(graph_sizes, results, param_sets):
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection="3d")

    x_data, y_data, z_data = [], [], []
    algorithm_mapping = {
        "EDF": 0,
        "HEFT": 1,
        "HEFT*": 2,
    }  # Convert algorithm names to numeric values

    for graph_type in graph_sizes:
        for alg_name in results[graph_type]:
            for params in param_sets[graph_type]:
                param_str = str(params)
                if param_str in results[graph_type][alg_name]:
                    makespan_values = results[graph_type][alg_name][param_str][
                        "makespan"
                    ]
                    avg_makespan = sum(makespan_values) / len(makespan_values)

                    # Convert graph complexity (e.g., edges/nodes ratio) to a numerical feature
                    complexity = len(graph_sizes[graph_type]) / max(
                        graph_sizes[graph_type]
                    )

                    x_data.append(complexity)
                    y_data.append(
                        algorithm_mapping[alg_name]
                    )  # Convert algorithm name to a number
                    z_data.append(avg_makespan)

    scatter = ax.scatter(x_data, y_data, z_data, c=z_data, cmap="coolwarm")

    ax.set_xlabel("Graph Complexity")
    ax.set_ylabel("Algorithm (0=EDF, 1=HEFT, 2=HEFT*)")
    ax.set_zlabel("Makespan")
    ax.set_title("Network Topology Influence on Scheduling")

    fig.colorbar(scatter, ax=ax, label="Makespan")
    plt.show()
