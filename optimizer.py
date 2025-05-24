# optimizer.py

import gurobipy as gp
from gurobipy import GRB

def build_and_solve_model(N, D, tau, d, MIN_RECHARGE, MAX_STATIONS, plot_solution=None):
    """
    Build and solve the SAEV Location-Routing Problem with Gurobi.
    Optionally, plot_solution(N, D, d, A, x, y) after optimization.
    """
    print("\n🔧 Building and optimizing the SAEV Location-Routing Problem...")

    A = [(i, j) for i in N for j in N if i != j and d[i][j] > 0]
    M = 99999  # Big-M

    m = gp.Model("SAEV_LRP")

    x = m.addVars(A, vtype=GRB.BINARY, name="x")   # Path arcs
    y = m.addVars(N, vtype=GRB.BINARY, name="y")   # Charging stations
    c = m.addVars(D.keys(), vtype=GRB.BINARY, name="c")  # Covered demand nodes
    r = m.addVars(N, vtype=GRB.CONTINUOUS, lb=0, name="r")  # Recharge amount at node
    b = m.addVars(N, vtype=GRB.CONTINUOUS, lb=0, ub=tau, name="b")  # Battery at node

    # Objective: Maximize coverage
    m.setObjective(gp.quicksum(D[j] * c[j] for j in D), GRB.MAXIMIZE)

    # Flow Conservation at Origin & Return Depot
    m.addConstr(gp.quicksum(x[0, j] for j in N if (0, j) in A) == 1)
    m.addConstr(gp.quicksum(x[i, N[-1]] for i in N if (i, N[-1]) in A) == 1)
    m.addConstr(gp.quicksum(x[i, 0] for i in N if (i, 0) in A) == 0)
    m.addConstr(gp.quicksum(x[N[-1], j] for j in N if (N[-1], j) in A) == 0)

    # Flow Conservation at Intermediate Nodes
    for i in N:
        if i not in [0, N[-1]]:
            m.addConstr(gp.quicksum(x[i, j] for j in N if (i, j) in A) ==
                        gp.quicksum(x[j, i] for j in N if (j, i) in A))
    
    # Flow Conservation at Demand Nodes
    for j in D:
        m.addConstr(gp.quicksum(x[i, j] for i in N if (i, j) in A) == c[j])
        m.addConstr(gp.quicksum(x[j, k] for k in N if (j, k) in A) == c[j])

    # Battery Update Equation and Battery Sufficiency
    for (i, j) in A:
        m.addConstr(b[j] >= b[i] - d[i][j] + r[j] - M * (1 - x[i, j]))
        m.addConstr(b[j] <= b[i] - d[i][j] + r[j] + M * (1 - x[i, j]))
        m.addConstr(b[i] >= d[i][j] * x[i, j])

    # Charging Station Constraints
    for i in N:
        m.addConstr(r[i] <= tau * y[i])
        m.addConstr(r[i] >= MIN_RECHARGE * y[i])
        m.addConstr(r[i] <= tau * gp.quicksum(x[j, i] for j in N if (j, i) in A))
        m.addConstr(y[i] <= gp.quicksum(x[j, i] for j in N if (j, i) in A))
        m.addConstr(b[i] >= 0.8 * tau * y[i])
        m.addConstr(b[i] <= tau * y[i] + tau * (1 - y[i]))

    # Initial and Final Battery Condition
    m.addConstr(b[0] == tau)
    m.addConstr(b[N[-1]] >= 0)
    m.addConstr(y[0] == 0)
    m.addConstr(y[N[-1]] == 0)

    # Budget constraint: max charging stations
    m.addConstr(gp.quicksum(y[i] for i in N) <= MAX_STATIONS)

    # No Charging Station at Demand Nodes
    for i in D:
        m.addConstr(y[i] == 0)

    # Subtour elimination (MTZ)
    u = m.addVars(range(1, N[-1]), vtype=GRB.CONTINUOUS, lb=1, ub=N[-1] - 1, name="u")
    for i in range(1, N[-1]):
        for j in range(1, N[-1]):
            if i != j and (i, j) in A:
                m.addConstr(u[i] - u[j] + (N[-1] - 1) * x[i, j] <= N[-1] - 2)

    m.setParam("TimeLimit", 60)
    m.setParam("OutputFlag", 0)
    m.optimize()

    if m.Status in [GRB.OPTIMAL, GRB.TIME_LIMIT]:
        print(f"\nObjective Value (Coverage): {m.ObjVal:.1f}")
        for i in N:
            if y[i].X > 0.5:
                print(f"  - Charging Station at node {i}")

        print("\nRecharge Events:")
        for i in N:
            if r[i].X > 1e-3:
                print(f"  - Recharge at node {i} (Energy added: {r[i].X:.1f}, Battery after: {b[i].X:.1f})")

        print("\nRoute:")
        visited_nodes = set()
        for (i, j) in A:
            if x[i, j].X > 0.5:
                print(f"  - {i} → {j} (distance: {d[i][j]})")
                visited_nodes.add(i)
        visited_nodes.add(N[-1])

        print("\nBattery Levels Along Route:")
        for i in sorted(visited_nodes):
            print(f"  - Node {i}: Battery = {b[i].X:.1f}")

        print("\nComplete Route:")
        route = [0]
        current = 0
        while current != N[-1]:
            for j in N:
                if (current, j) in A and x[current, j].X > 0.5:
                    route.append(j)
                    current = j
                    break
        print("  - " + " → ".join(map(str, route)))

        if plot_solution:
            plot_solution(N, D, d, A, x, y)
    else:
        print("No solution found.")
