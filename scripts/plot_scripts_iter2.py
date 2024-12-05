import pandas as pd
import matplotlib.pyplot as plt
import os

# Input CSV file generated from the data extraction script
RESULTS_CSV = "/home/rishi/results/butterfly_compiled_results.csv"

# Output directory for plots
OUTPUT_DIR = "/home/rishi/results/plots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the compiled results into a pandas DataFrame
df = pd.read_csv(RESULTS_CSV)

# Ensure the expected columns exist
expected_cols = {"Topology", "Routing", "Traffic", "Injection Rate", "Received Packets", "Average Delay", "Throughput"}
if not expected_cols.issubset(df.columns):
    raise ValueError(f"The CSV file must contain the following columns: {expected_cols}")

##############################
# Example 1: For each Traffic Pattern, plot Average Delay vs. Injection Rate,
# grouping lines by Routing Algorithm.
##############################

def plot_delay_by_routing_for_each_traffic(df):
    traffic_patterns = df['Traffic'].unique()
    for pattern in traffic_patterns:
        subset = df[df['Traffic'] == pattern]
        if subset.empty:
            continue
        
        plt.figure(figsize=(10, 6))
        # Group by routing algorithm
        for routing_alg in subset['Routing'].unique():
            data = subset[subset['Routing'] == routing_alg].sort_values('Injection Rate')
            plt.plot(data['Injection Rate'], data['Average Delay'], marker='o', label=routing_alg)

        plt.title(f"Average Delay vs. Injection Rate\nTraffic: {pattern}")
        plt.xlabel("Injection Rate")
        plt.ylabel("Average Delay (cycles)")
        plt.grid(True)
        plt.legend()
        output_file = os.path.join(OUTPUT_DIR, f"delay_vs_rate_{pattern}.png")
        plt.savefig(output_file)
        plt.close()
        print(f"Saved {output_file}")

##############################
# Example 2: For each Routing Algorithm, plot Average Delay vs. Injection Rate,
# grouping lines by Traffic Pattern.
##############################

def plot_delay_by_traffic_for_each_routing(df):
    routing_algs = df['Routing'].unique()
    for routing_alg in routing_algs:
        subset = df[df['Routing'] == routing_alg]
        if subset.empty:
            continue

        plt.figure(figsize=(10, 6))
        for pattern in subset['Traffic'].unique():
            data = subset[subset['Traffic'] == pattern].sort_values('Injection Rate')
            plt.plot(data['Injection Rate'], data['Average Delay'], marker='s', label=pattern)

        plt.title(f"Average Delay vs. Injection Rate\nRouting: {routing_alg}")
        plt.xlabel("Injection Rate")
        plt.ylabel("Average Delay (cycles)")
        plt.grid(True)
        plt.legend()
        output_file = os.path.join(OUTPUT_DIR, f"delay_vs_rate_routing_{routing_alg}.png")
        plt.savefig(output_file)
        plt.close()
        print(f"Saved {output_file}")

##############################
# Example 3: Throughput vs. Injection Rate for a chosen Traffic Pattern,
# comparing all Routing Algorithms. 
# (You can pick any traffic pattern you want.)
##############################

def plot_throughput_for_specific_traffic(df, chosen_pattern="TRAFFIC_RANDOM"):
    subset = df[df['Traffic'] == chosen_pattern]
    if subset.empty:
        print(f"No data found for traffic pattern: {chosen_pattern}")
        return

    plt.figure(figsize=(10, 6))
    for routing_alg in subset['Routing'].unique():
        data = subset[subset['Routing'] == routing_alg].sort_values('Injection Rate')
        plt.plot(data['Injection Rate'], data['Throughput'], marker='^', label=routing_alg)

    plt.title(f"Throughput vs. Injection Rate\nTraffic: {chosen_pattern}")
    plt.xlabel("Injection Rate")
    plt.ylabel("Throughput (flits/cycle)")
    plt.grid(True)
    plt.legend()
    output_file = os.path.join(OUTPUT_DIR, f"throughput_vs_rate_{chosen_pattern}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved {output_file}")

##############################
# Run the plotting functions
##############################

plot_delay_by_routing_for_each_traffic(df)
plot_delay_by_traffic_for_each_routing(df)
# Adjust the traffic pattern here if needed. If you have TRAFFIC_SHUFFLE, TRAFFIC_RANDOM, etc. choose accordingly.
plot_throughput_for_specific_traffic(df, chosen_pattern="TRAFFIC_RANDOM")

print("All plots have been generated and saved.")
