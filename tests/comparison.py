import pandas as pd

def compare_results(result1,result2):
    df1 = pd.read_csv(f"data/output/{result1}")
    df2 = pd.read_csv(f"data/output/{result2}")
      
    stations1 = df1['StationCount']
    stations2 = df2['StationCount']

    # Basic stats
    print("\n--- Statistics ---")
    print(f"{'Metric':<20} {'Algorithm 1':<10} {'Algorithm 2':<10}")
    print(f"{'Max':<20} {stations1.max():<10} {stations2.max():<10}")
    print(f"{'Average':<20} {stations1.mean():<10.3f} {stations2.mean():<10.3f}")

    # Ratios
    ratios = []
    for a, b in zip(stations1, stations2):
        if b != 0:
            ratio = a / b
        else:
            ratio = 1
        ratios.append(ratio)


    print("\n--- Ratio Summary (Algorithm1 / Algorithm2) ---")
    print(f"Average Ratio: {sum(ratios)/len(ratios):.3f}")
    print(f"Max Ratio: {max(ratios):.3f}")