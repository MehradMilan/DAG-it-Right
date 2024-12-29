import matplotlib.pyplot as plt


# HEFT Scheduling Implementation
def calculate_bottom_level(dag):
    """Calculate the bottom-level value for each task in the DAG."""
    bottom_level = {}

    def compute_bottom_level(node):
        if node in bottom_level:
            return bottom_level[node]
        successors = list(dag.successors(node))  # Convert to list to avoid re-iteration
        if not successors:  # No successors
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
    """
    Implement the HEFT algorithm for DAG scheduling.

    Parameters:
    - dag: Annotated DAG with 'weight' attributes for nodes (computation costs)
           and 'weight' attributes for edges (communication costs).
    - resources: List of resources with 'speed' attributes.

    Returns:
    - schedule: A dictionary mapping each resource to a list of scheduled tasks
                with their start and end times.
    """
    print(resources)
    # Step 1: Calculate bottom-level priority for each task
    bottom_level = calculate_bottom_level(dag)
    tasks = sorted(dag.nodes, key=lambda node: bottom_level[node], reverse=True)

    # Step 2: Initialize schedule and resource availability
    schedule = {resource: [] for resource in range(len(resources))}
    task_allocation = {}
    resource_availability = [0] * len(resources)  # Tracks when each resource becomes free
    task_start_times = {}

    # Step 3: Schedule tasks
    for task in tasks:
        best_time = float('inf')
        best_resource = None

        for resource_id, resource in enumerate(resources):
            # Calculate earliest start time for the current resource
            est = resource_availability[resource_id]  # Resource is free at this time
            for pred in dag.predecessors(task):
                if pred in task_allocation:
                    pred_end_time = task_start_times[pred][1]
                    if task_allocation[pred] != resource_id:
                        pred_end_time += dag.edges[pred, task]['weight']  # Communication cost
                    est = max(est, pred_end_time)

            # Calculate execution time
            exec_time = dag.nodes[task]['weight'] / resource['speed']
            eft = est + exec_time

            # Check if this resource gives the best EFT
            if eft < best_time:
                best_time = eft
                best_resource = resource_id

        # Assign task to the best resource
        task_allocation[task] = best_resource
        task_start_times[task] = (best_time - dag.nodes[task]['weight'] / resources[best_resource]['speed'], best_time)
        schedule[best_resource].append((task, task_start_times[task][0], task_start_times[task][1]))

        # Update resource availability
        resource_availability[best_resource] = best_time

        # Debug output for allocation
        print(f"Task {task} assigned to Resource {best_resource} at time {task_start_times[task][0]}-{task_start_times[task][1]}")

    return schedule


def visualize_schedule(schedule):
    """Visualize the HEFT schedule as a Gantt chart."""
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
    ax.set_title("HEFT Scheduling")
    ax.grid(True, linestyle='--', alpha=0.5)
    plt.show()

