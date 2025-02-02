import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx


def edf_schedule(dag, resources):
    topological_order = list(nx.topological_sort(dag))

    schedule = {resource: [] for resource in range(len(resources))}
    resource_availability = [0] * len(resources)
    task_finish_times = {}

    for task in topological_order:
        earliest_start = 0
        for parent in dag.predecessors(task):
            if parent not in task_finish_times:
                raise ValueError(
                    f"Predecessor task {parent} has not been scheduled before task {task}."
                )
            earliest_start = max(earliest_start, task_finish_times[parent])

        best_resource = None
        best_finish_time = float("inf")

        for resource_id, resource in enumerate(resources):
            resource_ready_time = max(
                resource_availability[resource_id], earliest_start
            )
            exec_time = dag.nodes[task]["weight"] / resource["speed"]
            finish_time = resource_ready_time + exec_time

            if finish_time < best_finish_time:
                best_finish_time = finish_time
                best_resource = resource_id

        start_time = max(resource_availability[best_resource], earliest_start)
        end_time = (
            start_time + dag.nodes[task]["weight"] / resources[best_resource]["speed"]
        )
        schedule[best_resource].append((task, start_time, end_time))

        task_finish_times[task] = end_time
        resource_availability[best_resource] = end_time

        print(
            f"Task {task} assigned to Resource {best_resource} at time {start_time}-{end_time}"
        )

    makespan = max(task_finish_times.values())

    utilization = {}
    for resource_id, tasks in schedule.items():
        active_time = sum(end - start for _, start, end in tasks)
        utilization[resource_id] = active_time / makespan if makespan > 0 else 0.0

    return schedule, makespan, utilization


def visualize_edf(schedule):
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = plt.cm.tab20.colors
    resource_ids = list(schedule.keys())

    for resource_id in resource_ids:
        tasks = schedule[resource_id]
        for task_id, start, end in tasks:
            ax.barh(
                resource_id,
                end - start,
                left=start,
                color=colors[task_id % len(colors)],
                edgecolor="black",
                align="center",
                label=f"Task {task_id}",
            )

    ax.set_yticks(resource_ids)
    ax.set_yticklabels([f"Resource {rid}" for rid in resource_ids])
    ax.set_xlabel("Time")
    ax.set_title("EDF Scheduling - Gantt Chart")

    handles = [
        mpatches.Patch(color=colors[i % len(colors)], label=f"Task {i}")
        for i in range(len(colors))
    ]
    ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc="upper left")

    plt.tight_layout()
    plt.show()
