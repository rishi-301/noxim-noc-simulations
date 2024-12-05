import pandas as pd
import matplotlib.pyplot as plt
import os

RESULTS_CSV = "/home/rishi/results/delta_topologies_compiled_results.csv"
OUTPUT_DIR = "/home/rishi/results/plots_delta"
os.makedirs(OUTPUT_DIR, exist_ok=True)

df = pd.read_csv(RESULTS_CSV)

expected_cols = {"Topology", "Routing", "Traffic", "Injection Rate", "Received Packets", "Average Delay", "Throughput"}
if not expected_cols.issubset(df.columns):
    raise ValueError(f"The CSV must contain {expected_cols} columns.")

# Since Routing is always DELTA, we don't need to group by routing. Just filter if needed.
# Confirm that routing is DELTA for all entries (optional check)
if (df['Routing'].unique() != ['DELTA']).all():
    print("Warning: Found routing algorithms other than DELTA. Proceeding anyway.")


def plot_delay_by_topologies_for_traffic(df, traffic_pattern):
    # For a given traffic pattern, plot Average Delay vs Injection Rate for each topology
    subset = df[(df['Traffic'] == traffic_pattern)]
    if subset.empty:
        print(f"No data for traffic pattern: {traffic_pattern}")
        return

    plt.figure(figsize=(10,6))
    for topo in subset['Topology'].unique():
        data = subset[subset['Topology'] == topo].sort_values('Injection Rate')
        plt.plot(data['Injection Rate'], data['Average Delay'], marker='o', label=topo)
    
    plt.title(f"Average Delay vs. Injection Rate\nTraffic: {traffic_pattern} (Routing=DELTA)")
    plt.xlabel("Injection Rate")
    plt.ylabel("Average Delay (cycles)")
    plt.grid(True)
    plt.legend()
    output_file = os.path.join(OUTPUT_DIR, f"delay_vs_rate_{traffic_pattern}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved {output_file}")

def plot_delay_by_traffic_for_topology(df, topology):
    # For a given topology, plot Average Delay vs Injection Rate for each traffic pattern
    subset = df[df['Topology'] == topology]
    if subset.empty:
        print(f"No data for topology: {topology}")
        return

    plt.figure(figsize=(10,6))
    for pattern in subset['Traffic'].unique():
        data = subset[subset['Traffic'] == pattern].sort_values('Injection Rate')
        plt.plot(data['Injection Rate'], data['Average Delay'], marker='s', label=pattern)
    
    plt.title(f"Average Delay vs. Injection Rate\nTopology: {topology} (Routing=DELTA)")
    plt.xlabel("Injection Rate")
    plt.ylabel("Average Delay (cycles)")
    plt.grid(True)
    plt.legend()
    output_file = os.path.join(OUTPUT_DIR, f"delay_vs_rate_topology_{topology}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved {output_file}")

def plot_throughput_by_topologies_for_traffic(df, traffic_pattern):
    # For a given traffic pattern, plot Throughput vs Injection Rate for each topology
    subset = df[df['Traffic'] == traffic_pattern]
    if subset.empty:
        print(f"No data for traffic pattern: {traffic_pattern}")
        return

    plt.figure(figsize=(10,6))
    for topo in subset['Topology'].unique():
        data = subset[subset['Topology'] == topo].sort_values('Injection Rate')
        plt.plot(data['Injection Rate'], data['Throughput'], marker='^', label=topo)
    
    plt.title(f"Throughput vs. Injection Rate\nTraffic: {traffic_pattern} (Routing=DELTA)")
    plt.xlabel("Injection Rate")
    plt.ylabel("Throughput (flits/cycle)")
    plt.grid(True)
    plt.legend()
    output_file = os.path.join(OUTPUT_DIR, f"throughput_vs_rate_{traffic_pattern}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved {output_file}")

def plot_throughput_by_traffic_for_topology(df, topology):
    # For a given topology, plot Throughput vs Injection Rate for each traffic pattern
    subset = df[df['Topology'] == topology]
    if subset.empty:
        print(f"No data for topology: {topology}")
        return

    plt.figure(figsize=(10,6))
    for pattern in subset['Traffic'].unique():
        data = subset[subset['Traffic'] == pattern].sort_values('Injection Rate')
        plt.plot(data['Injection Rate'], data['Throughput'], marker='d', label=pattern)
    
    plt.title(f"Throughput vs. Injection Rate\nTopology: {topology} (Routing=DELTA)")
    plt.xlabel("Injection Rate")
    plt.ylabel("Throughput (flits/cycle)")
    plt.grid(True)
    plt.legend()
    output_file = os.path.join(OUTPUT_DIR, f"throughput_vs_rate_topology_{topology}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved {output_file}")

# Traffic patterns available: TRAFFIC_RANDOM and TRAFFIC_BIT_REVERSAL
traffic_patterns = df['Traffic'].unique()
topologies = df['Topology'].unique()

# Generate plots
for pattern in traffic_patterns:
    # Delay vs Injection Rate for all topologies under this traffic pattern
    plot_delay_by_topologies_for_traffic(df, pattern)
    # Throughput vs Injection Rate for all topologies under this traffic pattern
    plot_throughput_by_topologies_for_traffic(df, pattern)

for topo in topologies:
    # Delay vs Injection Rate for all traffic patterns under this topology
    plot_delay_by_traffic_for_topology(df, topo)
    # Throughput vs Injection Rate for all traffic patterns under this topology
    plot_throughput_by_traffic_for_topology(df, topo)

print("All plots generated for butterfly, baseline, and omega topologies with DELTA routing.")
