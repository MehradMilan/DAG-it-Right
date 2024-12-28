# DAG it Right!

## Description

This project focuses on benchmarking task scheduling algorithms on Directed Acyclic Graphs (`DAG`s) in the context of complex network systems. The goal is to systematically evaluate the performance of scheduling algorithms, such as the Heterogeneous Earliest Finish Time (`HEFT`) algorithm, across synthetic and real-world DAGs. These benchmarks aim to analyze how various DAG structures and properties affect scheduling efficiency, specifically in terms of Makespan (total execution time) and resource utilization.

Key aspects of the project include:

+ Synthetic DAG Generation: Using graph generators such as **Barabási-Albert** (scale-free), **Watts-Strogatz** (small-world), and **Erdős-Rényi** (random) models to create controlled test cases.

+ Real-World DAGs: Modifying and preprocessing datasets from complex networks to convert them into realistic DAGs for scheduling experiments.

+ Task Scheduling Analysis: Simulating scheduling algorithms on DAGs and comparing performance metrics to identify strengths, weaknesses, and areas for optimization.