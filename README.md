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

-[1. SAEV Network Parameters](./network.py#L2)
  - [1.1. Demand Nodes with Priorities](./network.py#L12)
  - [1.2. Set Battery Capacity and Maximum Stations](./network.py#L14)
  - [1.3. Distance Matrix](./network.py#L17)
- [2. Build and Solve SAEV Model](./optimizer.py#L6)
  - [2.1. Initialize Variables](./optimizer.py#L13)
  - [2.2. Decision Variables](./optimizer.py#L20)
  - [2.3. Objective Function and Constraints](./optimizer.py#L28)
  - [2.4. Flow Conservation and Routing](./optimizer.py#L32)
  - [2.5. Recharge and Battery Constraints](./optimizer.py#L45)
  - [2.6. Solve the Model and Extract Results](./optimizer.py#L73)
- [3. SAEVs Network Visualization](./plot_utils.py#L9)
  - [3.1. Network Visualization](./plot_utils.py#L11)
  - [3.2. Optimal Route and Charging Station Visualization](./plot_utils.py#L70)


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
This project is licensed under the MIT License - see the [LICENSE](./LICENSE.txt) file for details.