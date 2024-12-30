import matplotlib.pyplot as plt

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


def heft_schedule(dag, resources):
    print(resources)
    bottom_level = calculate_bottom_level(dag)
    tasks = sorted(dag.nodes, key=lambda node: bottom_level[node], reverse=True)

    schedule = {resource: [] for resource in range(len(resources))}
    task_allocation = {}
    resource_availability = [0] * len(resources)
    task_start_times = {}

    for task in tasks:
        best_time = float('inf')
        best_resource = None

        for resource_id, resource in enumerate(resources):
            est = resource_availability[resource_id]
            for pred in dag.predecessors(task):
                if pred in task_allocation:
                    pred_end_time = task_start_times[pred][1]
                    if task_allocation[pred] != resource_id:
                        pred_end_time += dag.edges[pred, task]['weight']
                    est = max(est, pred_end_time)

            exec_time = dag.nodes[task]['weight'] / resource['speed']
            eft = est + exec_time

            if eft < best_time:
                best_time = eft
                best_resource = resource_id

        task_allocation[task] = best_resource
        task_start_times[task] = (best_time - dag.nodes[task]['weight'] / resources[best_resource]['speed'], best_time)
        schedule[best_resource].append((task, task_start_times[task][0], task_start_times[task][1]))

        resource_availability[best_resource] = best_time

        print(f"Task {task} assigned to Resource {best_resource} at time {task_start_times[task][0]}-{task_start_times[task][1]}")

    makespan = max(resource_availability)
    print(f"Makespan: {makespan}")

    utilization = {}
    for resource_id, tasks in schedule.items():
        active_time = sum(end - start for _, start, end in tasks)
        utilization[resource_id] = active_time / makespan if makespan > 0 else 0.0

    for resource_id, util in utilization.items():
        print(f"Resource {resource_id} utilization: {util:.2%}")

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

