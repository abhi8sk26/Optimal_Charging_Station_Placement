import random
import csv

def coordinates_generator(grid):
    row, col = grid.shape
    x = random.randint(0, row - 1)
    y = random.randint(0, col - 1)
    return (x, y)

def battery_capacity_generator(min_battery, max_battery):
    battery = random.randint(min_battery, max_battery)
    return battery

def generate_dataset(filename, no_of_robots, no_of_dataset, grid, min_battery, max_battery):

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        
        header = ["S.No"]
        for i in range(1, no_of_robots + 1):
            header.append(f"R{i}_x")
            header.append(f"R{i}_y")
        header.append("Capacity")
        header.extend(["Target_x", "Target_y"])
        writer.writerow(header)

        for run in range(1, no_of_dataset + 1):

            robots = []
            i = 1
            while i <= no_of_robots:
                robot_cord = coordinates_generator(grid)
                if robot_cord not in robots: 
                    robots.append(robot_cord)
                    i += 1
            
            battery = battery_capacity_generator(min_battery, max_battery)

            while True:
                target = coordinates_generator(grid)
                if target not in robots:
                    break
            
            row_data = [run]
            for (x, y) in robots:
                row_data.extend([x, y])
            row_data.append(battery)
            row_data.extend([target[0], target[1]])
            
            writer.writerow(row_data)

    print(f"Dataset saved to {filename}")
