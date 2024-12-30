import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx

def edf_schedule(dag, resources):
    """
    EDF scheduling with strict precedence constraints.
    
    Parameters:
    - dag: Annotated DAG with 'weight' attributes on nodes (used as deadlines).
    - resources: List of resources with 'speed' attributes.

    Returns:
    - schedule: A dictionary mapping resources to scheduled tasks and their times.
    - makespan: Total time to execute all tasks.
    - utilization: Resource utilization as a dictionary.
    """
    # Step 1: Topologically sort tasks
    topological_order = list(nx.topological_sort(dag))

    # Step 2: Initialize schedules and resource availability
    schedule = {resource: [] for resource in range(len(resources))}
    resource_availability = [0] * len(resources)  # Tracks when each resource becomes free
    task_finish_times = {}  # Track finish times of tasks

    # Step 3: Schedule each task in topological order
    for task in topological_order:
        earliest_start = 0  # Default to 0 if no dependencies
        for parent in dag.predecessors(task):
            # Ensure all predecessors have been scheduled
            if parent not in task_finish_times:
                raise ValueError(f"Predecessor task {parent} has not been scheduled before task {task}.")
            earliest_start = max(earliest_start, task_finish_times[parent])

        best_resource = None
        best_finish_time = float('inf')

        for resource_id, resource in enumerate(resources):
            # Resource is available at max of its own availability or task's earliest start
            resource_ready_time = max(resource_availability[resource_id], earliest_start)
            exec_time = dag.nodes[task]['weight'] / resource['speed']
            finish_time = resource_ready_time + exec_time

            if finish_time < best_finish_time:
                best_finish_time = finish_time
                best_resource = resource_id

        # Assign the task to the best resource
        start_time = max(resource_availability[best_resource], earliest_start)
        end_time = start_time + dag.nodes[task]['weight'] / resources[best_resource]['speed']
        schedule[best_resource].append((task, start_time, end_time))

        # Update task finish time and resource availability
        task_finish_times[task] = end_time
        resource_availability[best_resource] = end_time

        # Debug log for task assignment
        print(f"Task {task} assigned to Resource {best_resource} at time {start_time}-{end_time}")

    # Step 4: Calculate makespan
    makespan = max(task_finish_times.values())

    # Step 5: Calculate resource utilization
    utilization = {}
    for resource_id, tasks in schedule.items():
        active_time = sum(end - start for _, start, end in tasks)
        utilization[resource_id] = active_time / makespan if makespan > 0 else 0.0

    return schedule, makespan, utilization


def visualize_edf(schedule):
    """
    Visualize the task schedule as a Gantt chart.

    Parameters:
    - schedule: The schedule dictionary mapping resources to tasks.
                Format: {resource_id: [(task_id, start_time, end_time), ...]}
    - makespan: The total makespan of the schedule.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    colors = plt.cm.tab20.colors  # Use a colormap for task colors
    resource_ids = list(schedule.keys())

    for resource_id in resource_ids:
        tasks = schedule[resource_id]
        for task_id, start, end in tasks:
            ax.barh(
                resource_id, end - start, left=start,
                color=colors[task_id % len(colors)],
                edgecolor='black', align='center', label=f'Task {task_id}'
            )

    # Label formatting
    ax.set_yticks(resource_ids)
    ax.set_yticklabels([f'Resource {rid}' for rid in resource_ids])
    ax.set_xlabel('Time')
    ax.set_title('EDF Scheduling - Gantt Chart')

    # Add a legend
    handles = [mpatches.Patch(color=colors[i % len(colors)], label=f'Task {i}') for i in range(len(colors))]
    ax.legend(handles=handles, bbox_to_anchor=(1.05, 1), loc='upper left')

    plt.tight_layout()
    plt.show()
