# Search and Rescue simulations
This project uses PX4 SITL together with the MAVLink 2 communication protocol to simulate and evaluate search-and-rescue flight patterns for multicopter UAVs. The system generates autonomous waypoints and executes sector searches, expanding patterns, and other SAR-relevant geometries within a fully simulated PX4 environment.
## Pre-requisties
- QGroundControl installed and running
- PX4 SITL configured with a single multicopter airframe
- Python 3 environment with required dependencies installed
- pymavlink

## Runtime
Execute the main script
    ```
    main.py
    ```
Ensure PX4 SITL is running before launching script to allow MAVLink connections
### References
Search pattern definitions and descriptions are based on the methods described in: https://owaysonline.com/iamsar-search-patterns/
