import pandas as pd
import matplotlib.pyplot as plt
import os

# Set up paths
RESULTS_CSV = "/home/rishi/results/compiled_results.csv"
OUTPUT_DIR = "/home/rishi/results/plots"

# Create the output directory if it does not exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Read the compiled results into a DataFrame
df = pd.read_csv(RESULTS_CSV)

# The DataFrame is expected to have these columns:
# Topology, Injection Rate, Received Packets, Average Delay, Throughput

# 1. Plot Average Delay vs. Injection Rate for all topologies
def plot_delay_vs_injection(df, output_path):
    plt.figure(figsize=(10,6))
    # Get unique topologies
    topologies = df['Topology'].unique()
    for topo in topologies:
        subset = df[df['Topology'] == topo].sort_values('Injection Rate')
        plt.plot(subset['Injection Rate'], subset['Average Delay'], marker='o', label=topo)

    plt.title('Global Average Delay vs. Injection Rate')
    plt.xlabel('Injection Rate')
    plt.ylabel('Average Delay (cycles)')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot: {output_path}")

# 2. Plot Throughput vs. Injection Rate for all topologies
def plot_throughput_vs_injection(df, output_path):
    plt.figure(figsize=(10,6))
    topologies = df['Topology'].unique()
    for topo in topologies:
        subset = df[df['Topology'] == topo].sort_values('Injection Rate')
        plt.plot(subset['Injection Rate'], subset['Throughput'], marker='s', label=topo)

    plt.title('Throughput vs. Injection Rate')
    plt.xlabel('Injection Rate')
    plt.ylabel('Throughput (flits/cycle)')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot: {output_path}")

# 3. Compare MESH sizes only (e.g., mesh_2x2, mesh_4x4, mesh_8x8)
def plot_mesh_scalability(df, output_path):
    plt.figure(figsize=(10,6))
    # Filter for only those topologies that start with "mesh_"
    mesh_variants = [t for t in df['Topology'].unique() if t.startswith("mesh_")]
    for topo in mesh_variants:
        subset = df[df['Topology'] == topo].sort_values('Injection Rate')
        plt.plot(subset['Injection Rate'], subset['Average Delay'], marker='o', label=topo)

    plt.title('MESH Scalability: Average Delay vs. Injection Rate')
    plt.xlabel('Injection Rate')
    plt.ylabel('Average Delay (cycles)')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot: {output_path}")

# 4. Compare Delta Networks (BUTTERFLY, BASELINE, OMEGA) vs MESH
def plot_delta_vs_mesh(df, output_path):
    plt.figure(figsize=(10,6))
    # Assuming you compare a single mesh size (e.g., mesh_4x4) against others:
    compare_topologies = ["mesh_4x4", "butterfly", "baseline", "omega"]
    # Filter only these topologies if they exist in the dataset
    compare_topologies = [t for t in compare_topologies if t in df['Topology'].unique()]

    for topo in compare_topologies:
        subset = df[df['Topology'] == topo].sort_values('Injection Rate')
        plt.plot(subset['Injection Rate'], subset['Average Delay'], marker='D', label=topo)

    plt.title('Delta Network Topologies vs. Mesh (4x4): Average Delay')
    plt.xlabel('Injection Rate')
    plt.ylabel('Average Delay (cycles)')
    plt.grid(True)
    plt.legend()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved plot: {output_path}")

# Run the plotting functions
plot_delay_vs_injection(df, os.path.join(OUTPUT_DIR, "average_delay_all_topologies.png"))
plot_throughput_vs_injection(df, os.path.join(OUTPUT_DIR, "throughput_all_topologies.png"))
plot_mesh_scalability(df, os.path.join(OUTPUT_DIR, "mesh_scalability_delay.png"))
plot_delta_vs_mesh(df, os.path.join(OUTPUT_DIR, "delta_vs_mesh_delay.png"))

print("All plots generated successfully.")
