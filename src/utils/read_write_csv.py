import pandas as pd
import numpy as np

#--------------------------------------------------------------------Reading------------------------------------------------------------
def extract_robots(row):
    robot_positions = []
    i = 1
    while f'R{i}_x' in row and not pd.isna(row[f'R{i}_x']):
        robot_x = int(row[f'R{i}_x'])
        robot_y = int(row[f'R{i}_y'])
        robot_positions.append((robot_x, robot_y))
        i += 1
    return robot_positions

def extract_target(row):
    target_x = int(row['Target_x'])
    target_y = int(row['Target_y'])
    target = (target_x, target_y)
    return target 

def extract_chargers(row):
    chargers_positions = []
    i = 1
    while f'Station_{i}_x' in row and not pd.isna(row[f'Station_{i}_x']):
        charger_x = int(row[f'Station_{i}_x'])
        charger_y = int(row[f'Station_{i}_y'])
        chargers_positions.append((charger_x, charger_y))
        i += 1
    return chargers_positions

def extract_battery_capacity(row):
    battery_capacity = int(row['Capacity'])
    return battery_capacity

#-------------------------------------------------------------writing--------------------------------------------------------------
def build_result_row(row, robot_pos, target, battery_Capacity, chargers):

    result_row = {}
    result_row["S.No"] = row["S.No"]

    for i, robot in enumerate(robot_pos, 1):
        result_row[f"R{i}_x"] = robot[0]
        result_row[f"R{i}_y"] = robot[1]

    result_row["Capacity"] = battery_Capacity
    result_row["Target_x"] = target[0]
    result_row["Target_y"] = target[1]
    result_row["StationCount"] = len(chargers)

    for i, charger in enumerate(chargers, 1):
        result_row[f"Station_{i}_x"] = charger[0]
        result_row[f"Station_{i}_y"] = charger[1]

    for i in range(len(chargers) + 1, 51):
        result_row[f"Station_{i}_x"] = np.nan
        result_row[f"Station_{i}_y"] = np.nan

    return result_row

def create_output_csv(data, max_robots, output_file):
    output_df = pd.DataFrame(data)
    
    base_columns = ['S.No']
    
    for i in range(1, max_robots + 1):
        base_columns.extend([f'R{i}_x', f'R{i}_y'])
    
    base_columns.extend(['Capacity', 'Target_x', 'Target_y', 'StationCount'])
    
    for i in range(1, 50):
        base_columns.extend([f'Station_{i}_x', f'Station_{i}_y'])
    
    output_df = output_df[base_columns]
    
    output_df.to_csv(f"data/output/{output_file}", index=False)
    print(f"Results saved to {output_file}")