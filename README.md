# Multiple SAEV Routing and Charging Station Location Optimization

This project solves the **Shared Autonomous Electric Vehicle (SAEV)** Location-Routing Problem using the **Gurobi** optimization solver. It integrates optimal routing decisions with strategic charging station placements to achieve **maximum demand coverage**. The results include clear visualization of the network structure, optimal routes, and charging station locations.

## Features

- Formulates the SAEV routing and charging station location problem as a **Mixed-Integer Linear Programming (MILP)** model
- Solves optimization problems using the **Gurobi** solver
- Visualizes the network structure and solution with demand node priorities and charging station locations, and the number of served demand nodes

## Requirements

- Python 3.8+
- [Gurobi Optimizer](https://www.gurobi.com/)
- Packages: `gurobipy`, `networkx`, `matplotlib`


# Table of Contents

- [1. SAEV Network Parameters](#1-saev-network-parameters)
  - [1.1. Demand Nodes with Priorities](#11-demand-nodes-with-priorities)
  - [1.2. Set Battery Capacity and Maximum Stations](#12-set-battery-capacity-and-maximum-stations)
  - [1.3. Distance Matrix](#13-distance-matrix)
- [2. Build and Solve SAEV Model](#2-build-and-solve-saev-model)
  - [2.1. Initialize Variables](#21-initialize-variables)
  - [2.2. Decision Variables](#22-decision-variables)
  - [2.3. Objective Function and Constraints](#23-objective-function-and-constraints)
  - [2.4. Flow Conservation and Routing](#24-flow-conservation-and-routing)
  - [2.5. Recharge and Battery Constraints](#25-recharge-and-battery-constraints)
  - [2.6. Solve the Model and Extract Results](#26-solve-the-model-and-extract-results)
- [3. SAEVs Network Visualization](#3-saev-network-visualization)
  - [3.1. Network Visualization](#31-network-visualization)
  - [3.2. Optimal Route and Charging Station Visualization](#32-optimal-route-and-charging-station-visualization)


## Results

### SAEVs Network Visualization

Here we show the network structure, demand nodes, and the placement of charging stations. These visualizations help in understanding the network optimization.

#### Network Visualization

This figure shows the overall network layout with demand nodes and charging stations.

![Network Visualization](Network%20Visualization.png)

#### Optimal Route and Charging Station Visualization

The following image illustrates the optimal route taken by SAEVs, as well as the charging station placement based on the optimization results.

![Optimal Route and Charging Stations](Optimal%20Route%20and%20Charging%20Stations.png)



## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.