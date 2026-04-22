import pandas as pd
from src.utils.graph import create_grid_graph
from src.algorithms.heuristic import prune_bfs_tree, charger_placement, optimize_chargers
from src.utils.tree import create_bfs_tree
from src.utils.read_write_csv import extract_robots, extract_target, extract_battery_capacity, build_result_row, create_output_csv

def process_dataset_heuristic(input_file, output_file, grid):

    df = pd.read_csv(f"data/input/{input_file}")
    print(f"Processing {input_file} with {len(df)} rows")
    results = []
    max_robot = 0

    for index, row in df.iterrows():
        robots = extract_robots(row)
        target = extract_target(row)
        battery = extract_battery_capacity(row)

        max_robot = len(robots)
        print(f"Row {index + 1}: {len(robots)} robots, target {target}, capacity {battery}")

        G = create_grid_graph(grid)
        bfs_tree = create_bfs_tree(G, target)
        prune_bfs_tree(bfs_tree, target, robots)

        chargers = []
        charger_placement(bfs_tree, target, battery, chargers)
        chargers = optimize_chargers(robots, target, chargers, battery)


        row_result = build_result_row(row, robots, target, battery, chargers)
        results.append(row_result)
    
    create_output_csv(results, max_robot, output_file)
