import os
import re
import csv

topologies = ["mesh_4x4", "mesh_8x8", "mesh_10x10" ,"butterfly", "baseline", "omega"]
injection_rates = [0.01, 0.05, 0.1, 0.15, 0.2]

results = []

for topo in topologies:
    for rate in injection_rates:
        filename = f"/home/rishi/results/{topo}/{topo}_rate_{rate}.txt"
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                content = f.read()

                # Regex patterns as established previously
                received = re.search(r"% Total received packets:\s+(\d+)", content)
                avg_delay = re.search(r"% Global average delay \(cycles\):\s+([\d\.]+)", content)
                throughput = re.search(r"% Network throughput \(flits/cycle\):\s+([\d\.]+)", content)

                if received and avg_delay and throughput:
                    results.append({
                        "Topology": topo,
                        "Injection Rate": rate,
                        "Received Packets": int(received.group(1)),
                        "Average Delay": float(avg_delay.group(1)),
                        "Throughput": float(throughput.group(1))
                    })

# Write to CSV
output_csv = "/home/rishi/results/compiled_results.csv"
with open(output_csv, 'w', newline='') as csvfile:
    fieldnames = ["Topology", "Injection Rate", "Received Packets", "Average Delay", "Throughput"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"Results compiled into {output_csv}")
