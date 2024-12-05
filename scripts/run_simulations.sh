#!/bin/bash

topologies=("mesh_4x4" "mesh_8x8" "mesh_10x10" "butterfly" "baseline" "omega")
injection_rates=(0.01 0.05 0.1 0.15 0.2)

for topo in "${topologies[@]}"; do
    # Create a results directory for this topology/size if not existing
    mkdir -p /home/rishi/results/${topo}
    
    for rate in "${injection_rates[@]}"; do
        # Modify the injection rate in the configuration file
        sed -i "s/^packet_injection_rate:.*/packet_injection_rate: ${rate}/" /home/rishi/configs/${topo}.yaml
        
        # Run the simulation
        /home/rishi/noxim/bin/noxim \
            -config /home/rishi/configs/${topo}.yaml \
            -power /home/rishi/noxim/bin/power.yaml \
            > /home/rishi/results/${topo}/${topo}_rate_${rate}.txt
        
        echo "Simulation for ${topo} at injection rate ${rate} completed."
    done
done
