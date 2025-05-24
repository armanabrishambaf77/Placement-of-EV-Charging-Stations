# SAEV Location-Routing Problem Solver

This project solves the Shared Autonomous Electric Vehicle (SAEV) Location-Routing Problem using Gurobi, with visualization of network structure and optimal solutions.

## Features

- Defines SAEV routing and charging station placement as a mixed-integer program
- Uses Gurobi for optimization
- Visualizes the network and solution with demand node priorities and charging station locations

## Requirements

- Python 3.8+
- [Gurobi Optimizer](https://www.gurobi.com/)
- Packages: `gurobipy`, `networkx`, `matplotlib`


# Table of Contents

- [1. Import Libraries](#1-import-libraries)
- [2. Load Network Data](#2-load-network-data)
- [3. Visualize the Network](#3-visualize-the-network)
- [4. Initialize and Build the Optimization Model](#4-initialize-and-build-the-optimization-model)
- [5. Define Variables and Sets](#5-define-variables-and-sets)
- [6. Objective Function](#6-objective-function)
- [7. Constraints](#7-constraints)
  - [7.1. Route Continuity & Flow Conservation](#71-route-continuity--flow-conservation)
  - [7.2. Battery and Charging Constraints](#72-battery-and-charging-constraints)
  - [7.3. Demand Satisfaction](#73-demand-satisfaction)
  - [7.4. Charging Station Placement](#74-charging-station-placement)
  - [7.5. Subtour Elimination](#75-subtour-elimination)
  - [7.6. Operational Limits](#76-operational-limits)
- [8. Solve the Model](#8-solve-the-model)
  - [8.1. View Results in Console](#81-view-results-in-console)
  - [8.2. Visualize the Optimal Solution](#82-visualize-the-optimal-solution)
