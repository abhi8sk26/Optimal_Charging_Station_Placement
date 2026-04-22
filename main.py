import numpy as np
from src.main.run_brute_force import process_dataset_brute_force
from src.main.run_heuristic import process_dataset_heuristic
from tests.validation import validate_result
from src.data_generator.synthetic_dataset_generator import generate_dataset
from tests.comparison import compare_results
import subprocess
import sys
import os


def generate():
    row = int(input("Enter the no of rows of the grid: "))
    col = int(input("Enter the no of columns of the grid: "))
    no_of_datasets = int(input("Enter the no of datasets you want to generate: "))
    no_of_robots = int(input("Enter the no of robots you want: "))
    
    min_battery = int(input("Enter the minimum battery capacity: "))
    max_battery = int(input("Enter the maximum battery capacity: "))
    
    user_file = input("Enter the output filename (e.g., robot_dataset.csv): ")
    output_filename = f"data/input/{user_file}"

    
    if min_battery < 0:
        print("Warning: Minimum battery capacity cannot be negative. Setting to 0.")
        min_battery = 0
    if max_battery < min_battery:
        print("Error: Maximum battery capacity cannot be less than minimum battery capacity.")
        return
    
    grid = np.zeros((row, col), dtype=int)
    generate_dataset(output_filename, no_of_robots, no_of_datasets, grid, min_battery, max_battery)
    
def execute_algorithm():
        
    print("Select the algorithm you want to run: ")
    print("Enter 1 for brute force(Take longer time for larger grid size)")
    print("Enter 2 for heuristic")

    selector = int(input())

    row = int(input("Enter the number of rows of the grid: "))
    col = int(input("Enter the number of columns of the grid: "))

    input_file = input("Enter input CSV file name: ").strip()
    output_file = input("Enter output CSV file name: ").strip()

    grid = np.zeros((row, col), dtype=int)

    if selector == 1:
        process_dataset_brute_force(input_file, output_file, grid)
    elif selector == 2:
        process_dataset_heuristic(input_file, output_file, grid)

def validate():
    input_file = input("Enter filename to validate(eg. result.csv): ")
    validate_result(input_file)

def compare_result():
    print("----------Algorithm Results Comparison----------")

    heuristic_result = input("Enter the heuristic filename: ").strip()
    brute_force_result = input("Enter the brute_force filename: ").strip()
    compare_results(heuristic_result, brute_force_result)

def visualize():
    print("🚀 Launching Robot Path Analysis Dashboard...")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    dashboard_path = os.path.join(current_dir, "src", "visualization", "dashboard.py")
    
    if not os.path.exists(dashboard_path):
        print(f"❌ Error: Dashboard file not found at {dashboard_path}")
        print("Please ensure src/visualization/dashboard.py exists.")
        return
    
    # Launch Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", dashboard_path])
    except KeyboardInterrupt:
        print("\n✅ Dashboard closed.")
    except Exception as e:
        print(f"❌ Error launching dashboard: {e}")
        print("\nMake sure Streamlit is installed. Run: pip install streamlit")

def main():
   
    print("Select a choice ")
    print("Enter 1 to generate dataset ")
    print("Enter 2 to run algorithms ")
    print("Enter 3 to validate result ")
    print("Enter 4 to compare results ")
    print("Enter 5 to visualize results (Launch Dashboard) ")

    selector = int(input())
    if selector == 1:
        generate()
    elif selector == 2:
        execute_algorithm()
    elif selector == 3:
        validate()
    elif selector == 4:
        compare_result()
    elif selector == 5:
        visualize()
    else:
        print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    main()