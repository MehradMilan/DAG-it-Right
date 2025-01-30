import matplotlib.pyplot as plt
from collections import defaultdict
import networkx as nx

def calculate_bottom_level(dag):
    bottom_level = {}

    def compute_bottom_level(node):
        if node in bottom_level:
            return bottom_level[node]
        successors = list(dag.successors(node))
        if not successors:
            bottom_level[node] = dag.nodes[node]['weight']
        else:
            bottom_level[node] = dag.nodes[node]['weight'] + max(
                compute_bottom_level(child) + dag.edges[node, child]['weight']
                for child in successors
            )
        return bottom_level[node]

    for node in dag.nodes:
        compute_bottom_level(node)

    return bottom_level

def find_available_cores(resource_availability, required_cores, start_time):
    available_sets = []
    for i in range(len(resource_availability) - required_cores + 1):
        if all(resource_availability[j] <= start_time for j in range(i, i + required_cores)):
            available_sets.append(list(range(i, i + required_cores)))
    return available_sets

def calculate_centrality(dag):
    return nx.betweenness_centrality(dag)  # Compute centrality scores

def heft_schedule(dag, num_cores):
    bottom_level = calculate_bottom_level(dag)
    centrality = calculate_centrality(dag)  # New centrality calculation

    # Prioritize tasks based on bottom level + centrality
    tasks = sorted(dag.nodes, key=lambda node: (bottom_level[node], centrality[node]), reverse=True)

    schedule = defaultdict(list)
    task_allocation = {}
    task_start_times = {}
    resource_availability = [0] * num_cores

    for task in tasks:
        required_cores = dag.nodes[task]['num_cores']
        best_time = float('inf')
        best_cores = None

        for start_time in set(resource_availability):
            available_sets = find_available_cores(resource_availability, required_cores, start_time)
            for core_set in available_sets:
                est = start_time
                for pred in dag.predecessors(task):
                    if pred in task_allocation:
                        pred_end_time = task_start_times[pred][1]
                        if not set(task_allocation[pred]).issubset(set(core_set)):
                            pred_end_time += dag.edges[pred, task]['weight']
                        est = max(est, pred_end_time)

                exec_time = dag.nodes[task]['weight']
                eft = est + exec_time

                if eft < best_time:
                    best_time = eft
                    best_cores = core_set

        task_allocation[task] = best_cores
        task_start_times[task] = (best_time - dag.nodes[task]['weight'], best_time)
        for core in best_cores:
            resource_availability[core] = best_time
            schedule[core].append((task, task_start_times[task][0], task_start_times[task][1]))

        print(f"Task {task} (Centrality {centrality[task]:.3f}) assigned to Cores {best_cores} at time {task_start_times[task][0]}-{task_start_times[task][1]}")

    makespan = max(resource_availability)
    print(f"Makespan: {makespan}")

    utilization = {}
    for core_id, tasks in schedule.items():
        active_time = sum(end - start for _, start, end in tasks)
        utilization[core_id] = active_time / makespan if makespan > 0 else 0.0

    for core_id, util in utilization.items():
        print(f"Core {core_id} utilization: {util:.2%}")

    return schedule, makespan, utilization

def visualize_schedule(schedule):
    print(schedule)
    _, ax = plt.subplots(figsize=(10, 6))
    colors = ['red', 'blue', 'green', 'orange', 'purple']

    for resource_id, tasks in schedule.items():
        for task, start, end in tasks:
            ax.barh(resource_id, end - start, left=start, color=colors[resource_id % len(colors)], edgecolor='black')
            ax.text((start + end) / 2, resource_id, f"T{task}", color='white', ha='center', va='center', fontsize=10)

    ax.set_yticks(range(len(schedule)))
    ax.set_yticklabels([f"Resource {i}" for i in range(len(schedule))])
    ax.set_xlabel("Time")
    ax.set_ylabel("Resources")
    ax.set_title("Scheduling Result")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.show()

