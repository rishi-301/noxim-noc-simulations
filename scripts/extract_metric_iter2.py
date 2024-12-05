import os
import re
import csv

RESULTS_DIR = "/home/rishi/results/omega"
OUTPUT_CSV = "/home/rishi/results/omega_compiled_results.csv"

results = []

for filename in os.listdir(RESULTS_DIR):
    if filename.endswith(".txt"):
        fullpath = os.path.join(RESULTS_DIR, filename)
        parts = filename.replace(".txt","").split("_")

        # Expected general pattern: mesh_4x4_<ROUTING>_<TRAFFIC_...>_rate_<RATE>
        # e.g. mesh_4x4_WEST_FIRST_TRAFFIC_SHUFFLE_rate_0.01.txt
        # After splitting:
        # ["mesh", "4x4", "WEST", "FIRST", "TRAFFIC", "SHUFFLE", "rate", "0.01"]

        # Basic checks
        if len(parts) < 6:
            continue
        if "rate" not in parts:
            continue

        # Topology is fixed in first two tokens
        topo = parts[0] + "_" + parts[1]

        try:
            rate_index = parts.index("rate")
        except ValueError:
            continue

        # Injection rate is the token after 'rate'
        if rate_index + 1 >= len(parts):
            continue
        rate_str = parts[rate_index + 1]
        try:
            rate_val = float(rate_str)
        except ValueError:
            continue

        # The tokens between parts[2] and parts[rate_index] contain ROUTING and TRAFFIC
        # Find 'TRAFFIC' token in that range
        try:
            traffic_index = parts.index("TRAFFIC", 2, rate_index)
        except ValueError:
            # If 'TRAFFIC' is not found, we cannot parse correctly
            continue

        # Routing tokens are between parts[2] and parts[traffic_index]
        routing_tokens = parts[2:traffic_index]
        # Traffic tokens are from traffic_index to rate_index
        # The first token in this is "TRAFFIC", followed by pattern specifiers
        traffic_tokens = parts[traffic_index:rate_index]

        # Rejoin the routing tokens with underscores to get full routing algorithm name
        routing = "_".join(routing_tokens)

        # Rejoin the traffic tokens with underscores for full traffic pattern name
        # e.g. ["TRAFFIC","SHUFFLE"] -> "TRAFFIC_SHUFFLE"
        traffic_pattern = "_".join(traffic_tokens)

        # Read file content and extract metrics
        with open(fullpath, 'r') as f:
            content = f.read()

            received = re.search(r"% Total received packets:\s+(\d+)", content)
            avg_delay = re.search(r"% Global average delay \(cycles\):\s+([\d\.]+)", content)
            throughput = re.search(r"% Network throughput \(flits/cycle\):\s+([\d\.]+)", content)

            if received and avg_delay and throughput:
                results.append({
                    "Topology": topo,
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
