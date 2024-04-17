# Longest-simple-path

## Overview
This Python project provides tools for generating and analyzing graphs, focusing on finding the Largest Connected Component (LCC) and the Longest Simple Path (LSP) using various algorithms like DFS, Dijkstra's Algorithm, A*, and GRASP. It includes functionalities for generating random geometric graphs, computing various graph metrics, and visualizing the results.

## Features
- **Graph Generation**: Generate random geometric graphs based on node count and radius.
- **Largest Connected Component (LCC)**: Identify the LCC using Depth-First Search (DFS).
- **Longest Simple Path (LSP)**: Compute the longest simple path using multiple algorithms:
  - **Dijkstra's Algorithm**
  - **DFS**
  - **A* Search**
  - **GRASP (Greedy Randomized Adaptive Search Procedure)**
- **Graph Metrics Calculation**: Compute and compare metrics for each algorithm.
- **File Interaction**: Interact with the file system to select and process graph data files.

## Requirements
- Python 3.x

## Installation
1. Download the ZIP file containing the project.
2. Unzip the file to your preferred location.
3. Navigate to the project directory.

## Usage
Run the script in your command-line interface with:
python Main.py or use pycharm (preferable) and run Main.py

You'll be presented with a file selection menu:

Available files:
1: DSJC500-5.mtx
2: inf-euroad.edges
...
Select a file by number:

Input the number corresponding to the file you wish to analyze and press Enter.

*Please note that the amount of iterations and candidates node sizes for the GRASP
heuristic can be modified directly in the class attributes.