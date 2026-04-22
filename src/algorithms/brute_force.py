from itertools import combinations
from src.utils.reachability_check import can_all_robot_reach_target

def find_min_chargers(grid, robots, target, battery):
    row, col = grid.shape

    all_positions = [(i, j) for i in range(row) for j in range(col)
                     if grid[i][j] == 0 and (i, j) != target]

    for num_chargers in range(0, row * col + 1):
        for chargers in combinations(all_positions, num_chargers):
            if can_all_robot_reach_target(target, robots, chargers, battery, visited_robots=None, visited_stations=None):
                return chargers
    return []