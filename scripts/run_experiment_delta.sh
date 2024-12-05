#!/bin/bash

# Configure your test parameters here
TOPOLOGY="omega"
CONFIG_FILE="/home/rishi/configs/${TOPOLOGY}.yaml"
POWER_FILE="/home/rishi/noxim/bin/power.yaml"
NOXIM_BIN="/home/rishi/noxim/bin/noxim"

# Directories
RESULTS_DIR="/home/rishi/results/${TOPOLOGY}"
mkdir -p $RESULTS_DIR

# Set the lists of parameters you want to vary
ROUTING_ALGORITHMS=("DELTA")
TRAFFIC_PATTERNS=("TRAFFIC_RANDOM" "TRAFFIC_BIT_REVERSAL")
INJECTION_RATES=(0.01 0.05 0.1 0.15 0.2)

# If using HOTSPOT traffic, Noxim may require hotspot configuration lines in the config.
# Ensure your config or Noxim supports these patterns as needed.
# For TRANSPOSE or other patterns, also ensure Noxim supports them.

for ROUTING in "${ROUTING_ALGORITHMS[@]}"; do
    for PATTERN in "${TRAFFIC_PATTERNS[@]}"; do
        for RATE in "${INJECTION_RATES[@]}"; do
            # Modify the config file on-the-fly
            sed -i "s/^routing_algorithm:.*/routing_algorithm: ${ROUTING}/" $CONFIG_FILE
            sed -i "s/^packet_injection_rate:.*/packet_injection_rate: ${RATE}/" $CONFIG_FILE
            sed -i "s/^traffic_distribution:.*/traffic_distribution: ${PATTERN}/" $CONFIG_FILE

            # Construct output filename
            # Example format: mesh_4x4_ROUTING=XY_PATTERN=TRAFFIC_RANDOM_RATE=0.01.txt
            OUTPUT_FILE="${RESULTS_DIR}/${TOPOLOGY}_${ROUTING}_${PATTERN}_rate_${RATE}.txt"

            # Run the simulation
            $NOXIM_BIN -config $CONFIG_FILE -power $POWER_FILE > $OUTPUT_FILE

            echo "Completed: Topology=$TOPOLOGY, Routing=$ROUTING, Traffic=$PATTERN, Rate=$RATE"
        done
    done
done

echo "All simulations completed."
