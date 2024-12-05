import os
import re
import csv

# Directories for the three delta network topologies
topologies = ["butterfly", "baseline", "omega"]
base_results_dir = "/home/rishi/results"

OUTPUT_CSV = "/home/rishi/results/delta_topologies_compiled_results.csv"

results = []

for topo in topologies:
    topo_dir = os.path.join(base_results_dir, topo)
    if not os.path.isdir(topo_dir):
        continue
    
    for filename in os.listdir(topo_dir):
        if filename.endswith(".txt"):
            fullpath = os.path.join(topo_dir, filename)
            # Expected pattern:
            # <topology>_DELTA_TRAFFIC_..._rate_<value>.txt
            # e.g., butterfly_DELTA_TRAFFIC_RANDOM_rate_0.01.txt
            # or butterfly_DELTA_TRAFFIC_BIT_REVERSAL_rate_0.05.txt

            parts = filename.replace(".txt","").split("_")
            # Minimal expected parts:
            # [topology, "DELTA", "TRAFFIC", ... , "rate", <rate_value>]

            if len(parts) < 6:
                # Not enough parts to parse
                continue

            if "rate" not in parts:
                continue

            try:
                rate_index = parts.index("rate")
            except ValueError:
                continue

            if rate_index + 1 >= len(parts):
                # No rate value after 'rate'
                continue

            rate_str = parts[rate_index + 1]
            try:
                rate_val = float(rate_str)
            except ValueError:
                continue

            # Extract traffic pattern:
            # Everything between "TRAFFIC" and "rate" belongs to the traffic pattern
            try:
                traffic_index = parts.index("TRAFFIC")
            except ValueError:
                # If no TRAFFIC token, skip
                continue

            # Traffic tokens from traffic_index to rate_index (excluding rate_index)
            # Example: ["TRAFFIC","BIT","REVERSAL"]
            traffic_tokens = parts[traffic_index:rate_index]
            traffic_pattern = "_".join(traffic_tokens)

            # Routing is always DELTA here
            routing = "DELTA"

            # Verify topology (the first token should match the directory's topology)
            # parts[0] = topology name
            file_topo = parts[0]
            if file_topo not in topologies:
                # Filename doesn't match expected topology
                continue

            # Parse simulation output
            with open(fullpath, 'r') as f:
                content = f.read()

                received = re.search(r"% Total received packets:\s+(\d+)", content)
                avg_delay = re.search(r"% Global average delay \(cycles\):\s+([\d\.]+)", content)
                throughput = re.search(r"% Network throughput \(flits/cycle\):\s+([\d\.]+)", content)

                if received and avg_delay and throughput:
                    results.append({
                        "Topology": file_topo,
                        "Routing": routing,
                        "Traffic": traffic_pattern,
                        "Injection Rate": rate_val,
                        "Received Packets": int(received.group(1)),
                        "Average Delay": float(avg_delay.group(1)),
                        "Throughput": float(throughput.group(1))
                    })

# Write results to CSV
with open(OUTPUT_CSV, 'w', newline='') as csvfile:
    fieldnames = ["Topology", "Routing", "Traffic", "Injection Rate", "Received Packets", "Average Delay", "Throughput"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Compiled results written to {OUTPUT_CSV}")
