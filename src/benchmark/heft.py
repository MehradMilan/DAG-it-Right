from collections import defaultdict
import networkx as nx

def compute_upward_ranks(dag):
    ranks = {}

    def rank(node):
        if node in ranks:
            return ranks[node]
        if dag.out_degree(node) == 0:  # Leaf node
            ranks[node] = dag.nodes[node]['weight']
        else:
            ranks[node] = dag.nodes[node]['weight'] + max(
                dag.edges[node, succ]['weight'] + rank(succ)
                for succ in dag.successors(node)
            )
        return ranks[node]

    for node in nx.topological_sort(dag):
        rank(node)

    return ranks

def heft_schedule(dag, num_processors):
    upward_ranks = compute_upward_ranks(dag)
    tasks_sorted = sorted(upward_ranks, key=upward_ranks.get, reverse=True)

    schedule = defaultdict(list)  # Processor -> List of (task, start_time, end_time)
    task_start_end = {}  # Task -> (start_time, end_time)
    processor_avail = [0] * num_processors  # Track availability of each processor

    for task in tasks_sorted:
        best_processor = None
        earliest_finish_time = float("inf")
        best_start_time = None

        for proc in range(num_processors):
            ready_time = processor_avail[proc]
            start_time = ready_time

            # Check dependency constraints
            for pred in dag.predecessors(task):
                if pred not in task_start_end:
                    raise ValueError(f"Predecessor {pred} of task {task} has no scheduled end time.")
                pred_end = task_start_end[pred][1]
                comm_time = dag.edges[pred, task]['weight'] if (pred, task) in dag.edges else 0
                start_time = max(start_time, pred_end + comm_time)

            finish_time = start_time + dag.nodes[task]['weight']

            if finish_time < earliest_finish_time:
                earliest_finish_time = finish_time
                best_processor = proc
                best_start_time = start_time

        if best_processor is None:
            raise ValueError(f"Task {task} could not be assigned to any processor.")

        # Assign task to best processor
        schedule[best_processor].append((task, best_start_time, earliest_finish_time))
        task_start_end[task] = (best_start_time, earliest_finish_time)
        processor_avail[best_processor] = earliest_finish_time

    return dict(schedule)


def print_schedule(schedule):
    for proc, tasks in schedule.items():
        print(f"Processor {proc}:")
        for task, start, end in tasks:
            print(f"  Task {task}: Start at {start}, End at {end}")
