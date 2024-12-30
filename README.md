# DAG it Right!

### The `Real-Time Systems` course project

Sharif University of Technology - Fall 2024

---

+ **Mehrad Milanloo**

    + **Student ID**: 99105775

    + **Email**: milanloomehrad@gmail.com

+ **Hossein Alihosseini**

    + **Student ID**: 99101921

    + **Email**: themmdhossein@gmail.com

---

## Description

This project focuses on benchmarking task scheduling algorithms on Directed Acyclic Graphs (`DAG`s) in the context of complex network systems. The goal is to systematically evaluate the performance of scheduling algorithms, such as the Heterogeneous Earliest Finish Time (`HEFT`) algorithm, across synthetic and real-world DAGs. These benchmarks aim to analyze how various DAG structures and properties affect scheduling efficiency, specifically in terms of Makespan (total execution time) and resource utilization.

Key aspects of the project include:

+ Synthetic DAG Generation: Using graph generators such as **Barabási-Albert** (scale-free), **Watts-Strogatz** (small-world), and **Erdős-Rényi** (random) models to create controlled test cases.

+ Real-World DAGs: Modifying and preprocessing datasets from complex networks to convert them into realistic DAGs for scheduling experiments.

+ Task Scheduling Analysis: Simulating scheduling algorithms on DAGs and comparing performance metrics to identify strengths, weaknesses, and areas for optimization.

This project provides a command-line interface (`CLI`) to work with DAGs for scheduling benchmarks. The CLI supports:

+ Generating synthetic graphs with various network models.

+ Downloading and batch-processing scalable, real-world datasets.

+ Benchmarking and visualizing scheduling algorithms on DAGs.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/MehradMilan/DAG-it-Right
cd DAG-it-Right
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## How to Use the CLI

The CLI supports several commands. Below is a detailed explanation of each command:

### 1. Generate Synthetic Graphs

You can generate synthetic graphs with arbitrary sizes and different models of complex networks.

**Supported Models**:

1. **Barabási-Albert (Scale-Free Model)**:

   + Generates a scale-free network where some nodes have significantly higher connectivity.

   + Use this model to simulate social networks or web graphs.

2. **Watts-Strogatz (Small-World Model)**:

    + Produces graphs with high clustering and short path lengths.

    + Suitable for modeling real-world networks like electrical grids or neural networks.

3. **Erdős-Rényi (Random Model)**:

    + Generates a random graph with a uniform probability of edge creation.

    + Useful for analyzing random processes and network algorithms.

**Command**:

```bash
python cli/cli.py generate --graph-type <model> --nodes <num_nodes> 
--param <model_param> --output <output_file> 
[--visualize] [--benchmark] [--num-proc <num_processors>]
```

**Examples**:

+ Generate a Barabási-Albert graph with 50 nodes:

```bash
python cli/cli.py generate --graph-type barabasi_albert --nodes 50 --param 3 
--output barabasi_albert_dag.gml
```

+ Generate a Watts-Strogatz graph and visualize it:

```bash
python cli/cli.py generate --graph-type watts_strogatz --nodes 100 --param 5 
--output small_world_dag.gml --visualize
```

+ Generate and benchmark an Erdős-Rényi graph:

```bash
python cli/cli.py generate --graph-type erdos_renyi --nodes 75 --param 0.1 
--output random_dag.gml --benchmark --num-proc 4
```

### 2. Download and Process Real-World Datasets

The CLI supports downloading real-world datasets (e.g., internet networks, autonomous systems, etc.) and processing them into DAGs.

**Command**:

1. Download Datasets:

```bash
python cli/cli.py download --type <dataset_type>
```

**Example**:

```bash
python cli/cli.py download --type internet_networks
```

1. Download Datasets:

```bash
python cli/cli.py download --type <dataset_type>
```

**Example**:

```bash
python cli/cli.py download --type internet_networks
```

2. Process a Single Dataset:

```bash
python cli/cli.py process --input <file_path> --format <file_format> --output <output_file>
```

**Example**:

```bash
python cli/cli.py process --input data/input/dataset/Oregon1_010526.txt 
--format edgelist --output p2p_gnutella_dag.gml
```

3. Batch-Process Datasets:

```bash
python cli/cli.py batch-process --type <dataset_type>
```

**Example**:

```bash
python cli/cli.py batch-process --type internet_networks
```

### 3. Benchmark and Visualize Scheduling

You can benchmark scheduling algorithms (like HEFT) on DAGs and visualize the results.

**Command**:

```bash
python cli/cli.py benchmark --input <dag_file> --num-proc <num_processors> [--visualize]

```

**Examples**:

+ Benchmark a previously generated DAG with 3 processors:

```bash
python cli/cli.py benchmark --input barabasi_albert_dag.gml --num-proc 3
```

+ Benchmark and visualize the schedule:

```bash
python cli/cli.py benchmark --input p2p_gnutella_dag.gml --num-proc 4 --visualize

```

## Outputs

+ **Generated Graphs**: Saved in GML format in the specified `--output` file.

+ **Processed DAGs**: Stored in the `data/output/graphs` directory for batch processing.

+ **Visualization**: Graphs are displayed in a matplotlib window if `--visualize` is used.

## Dataset Sources

The real-world datasets are downloaded from:

+ [SNAP](https://snap.stanford.edu/data/)