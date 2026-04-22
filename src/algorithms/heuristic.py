from src.utils.reachability_check import can_all_robot_reach_target

def prune_bfs_tree(bfs_tree, curr_node, robots):
    if bfs_tree.out_degree(curr_node) == 0:
        return curr_node in robots
    
    keep_this_node = False
    if curr_node in robots:
        keep_this_node = True

    children = list(bfs_tree.successors(curr_node))
    for child in children:
        is_child_usefull = prune_bfs_tree(bfs_tree, child, robots)

        if not is_child_usefull:
            bfs_tree.remove_edge(curr_node, child)
        else:
            keep_this_node = True

    return keep_this_node
        
def charger_placement(bfs_tree, curr_node, battery_capacity, chargers):

    if bfs_tree.out_degree(curr_node) == 0:
        return 0
    
    curr_height = 0
    for child in bfs_tree.successors(curr_node):
        child_height = charger_placement(bfs_tree, child, battery_capacity, chargers)
        if child_height == battery_capacity and child not in chargers:
            chargers.append(child)
            child_height = 0
        curr_height = max(curr_height, child_height)

    if curr_height == battery_capacity or curr_node in chargers:
        curr_height = 0

    return curr_height + 1

def optimize_chargers(robots, target, chargers, battery_capacity):

    for charger in chargers:
        temp_chargers = []
        for c in chargers:
            if c != charger:
                temp_chargers.append(c)

        if can_all_robot_reach_target(target, robots, temp_chargers, battery_capacity, visited_robots = None, visited_stations = None):
            print(f"✅ Removed redundant charger at {charger}")
            chargers = temp_chargers
        else:
            print(f"❌ Kept charger at {charger} (needed)")
    print(f"Graph-based optimization complete: {len(chargers)} chargers remain.")
    return chargers
