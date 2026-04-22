import pandas as pd
from src.utils.reachability_check import reachable_robots
from src.utils.read_write_csv import extract_robots, extract_target, extract_battery_capacity, extract_chargers

def validate_result(input_file):
    df = pd.read_csv(f"data/output/{input_file}")
    total_rows = len(df)
    failed_rows = []
    count = 0

    for index, row in df.iterrows():
        robots = extract_robots(row)
        target = extract_target(row)
        battery = extract_battery_capacity(row)
        chargers = extract_chargers(row)
        
        reachable_robot_s = reachable_robots(target, robots, chargers, battery, visited_robots=None, visited_stations=None)
        if len(reachable_robot_s) == len(robots):
            count += 1
        else:
            unreachable_robots = []
            for i, robot in enumerate(robots, 1):
                if robot not in reachable_robot_s:
                    unreachable_robots.append(f'R{i}')
            failed_rows.append((index + 1, unreachable_robots))

    print("Total Rows : ", total_rows)
    print(f"Passed Rows : {count}/{total_rows}")
    print("----------- Failed Rows ------------")
    for row_index, failed_robots in failed_rows:
        print(f"Row {row_index}, Failed Robots : {failed_robots}")
