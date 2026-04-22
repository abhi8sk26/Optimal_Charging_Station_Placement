# Optimal Charging Station Placement for Multi-Robot Systems

This project implements algorithms to determine the optimal placement of charging stations in a grid environment, ensuring that all robots can reach a target location under battery constraints.

## Problem Description

Given:
- A grid of size M x N
- Multiple robots at different starting positions
- A target location that all robots must reach
- A battery capacity (maximum Manhattan distance each robot can travel)

Objective:
Find the minimum number of charging stations and their optimal positions such that every robot can reach the target. Robots can recharge at stations, and stations can be placed in any empty cell (not occupied by the target).

## Features

- **Synthetic Dataset Generation** - Create custom test datasets
- **Brute Force Algorithm** - Guaranteed optimal solution (for small grids)
- **Heuristic Algorithm** - Fast approximation for larger grids
- **Validation** - Verify all robots can reach target
- **Comparison** - Compare algorithm performance
- **Interactive Dashboard** - Visualize robot paths and station coverage

## Dataset
    The dataset used in this project is included in the repository under the `data/` directory.

## Algorithms Implemented

### 1. Brute Force
- Exhaustively checks all combinations of charger positions
- Guarantees optimal solution
- Computationally expensive (suitable for small grids up to ~5x5)

### 2. Heuristic
- Constructs a BFS tree rooted at the target
- Prunes branches that don't lead to robots
- Places chargers based on battery constraints
- Adds post-processing to remove redundant chargers
- Faster than brute force for larger grids

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

## Way to run
    ```bash
    python main.py

## you will be prompted with the following options:

📋 Menu Options
## Dataset Generation
    - Generate synthetic dataset

## Run Algorithm
Executes either:
    - Brute Force (optimal)
    - Heuristic (faster, near-optimal)

## Validate Result
    - Validate result CSV

## Compare Results
    - Compares outputs of brute-force and heuristic approaches
    - Helps evaluate performance

## visualize results (Launch Dashboard)
   - Visually verify that all robots can reach the target using the placed charging stations
   - Shows robot paths from start → stations → target
   - Displays battery range coverage
   - Identifies and show which robots CAN and CANNOT reach target
    
