from collections import deque

def manhattan_distance(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])

def can_all_robot_reach_target(target, robots, stations, capacity, visited_robots=None, visited_stations=None):
    if visited_robots is None:
        visited_robots = set()
    if visited_stations is None:
        visited_stations = set()

    queue = deque([target])

    while queue:
        curr_target = queue.popleft()

        for robot in robots:
            if robot not in visited_robots and manhattan_distance(robot, curr_target) <= capacity:
                visited_robots.add(robot)

        for station in stations:
            if station not in visited_stations and manhattan_distance(station, curr_target) <= capacity:
                visited_stations.add(station)
                queue.append(station)

    return len(robots) == len(visited_robots)

def reachable_robots(target, robots, stations, capacity, visited_robots=None, visited_stations=None):
    if visited_robots is None:
        visited_robots = set()
    if visited_stations is None:
        visited_stations = set()

    queue = deque([target])

    while queue:
        curr_target = queue.popleft()

        for robot in robots:
            if robot not in visited_robots and manhattan_distance(robot, curr_target) <= capacity:
                visited_robots.add(robot)

        for station in stations:
            if station not in visited_stations and manhattan_distance(station, curr_target) <= capacity:
                visited_stations.add(station)
                queue.append(station)

    return visited_robots