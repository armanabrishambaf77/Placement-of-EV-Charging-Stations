# optimizer.py

import gurobipy as gp
from gurobipy import GRB

def build_and_solve_model(N, D, tau, d, MAX_STATIONS, plot_solution=None):
    """
    Build and solve the SAEV Location-Routing Problem with Gurobi.
    Optionally, plot_solution(N, D, d, A, x, y) after optimization.
    """
    print("Building and optimizing the Multi‐SAEV Location-Routing Problem...")

    K = [1, 2]
    A = [(i, j) for i in N for j in N if i != j and d[i][j] > 0]
    M = 99999  # Big-M

    m = gp.Model("Multi_SAEV_LRP")

    x = m.addVars(A, K, vtype=GRB.BINARY, name="x")                    # arc i→j by vehicle k
    y = m.addVars(N, vtype=GRB.BINARY, name="y")                       # Charging stations
    c = m.addVars(D.keys(), vtype=GRB.BINARY, name="c")                # Covered demand nodes
    r = m.addVars(N, K, vtype=GRB.CONTINUOUS, lb=0, name="r")          # recharge at i by k
    b = m.addVars(N, K, vtype=GRB.CONTINUOUS, lb=0, ub=tau, name="b")  # battery at i by k

    # Objective: Maximize coverage
    m.setObjective(gp.quicksum(D[j] * c[j] for j in D), GRB.MAXIMIZE)

    # Flow Conservation at Origin & Return Depot
    for k in K:
        m.addConstr(gp.quicksum(x[0, j, k] for j in N if (0, j) in A) == 1)
        m.addConstr(gp.quicksum(x[i, N[-1], k] for i in N if (i, N[-1]) in A) == 1)
        m.addConstr(gp.quicksum(x[N[-1], j, k] for j in N if (N[-1], j) in A) == 0)
        for i in N:
            if i not in [0, N[-1]]:
                m.addConstr(gp.quicksum(x[i, j, k] for j in N if (i, j) in A) ==
                            gp.quicksum(x[j, i, k] for j in N if (j, i) in A))
    for j in D:
        m.addConstr(gp.quicksum(x[i, j, k] for i in N for k in K if (i, j) in A) == c[j])
        m.addConstr(gp.quicksum(x[j, i, k] for i in N for k in K if (j, i) in A) == c[j])
    
    for k in K:
        for (i, j) in A:
            m.addConstr(b[j, k] >= b[i, k] - d[i][j] + r[j, k] - M * (1 - x[i, j, k]))
            m.addConstr(b[j, k] <= b[i, k] - d[i][j] + r[j, k] + M * (1 - x[i, j, k]))
            m.addConstr(b[i, k] >= d[i][j] * x[i, j, k])
        for i in N:
            m.addConstr(r[i, k] <= tau * y[i])
            m.addConstr(r[i, k] <= tau * gp.quicksum(x[j, i, k] for j in N if (j, i) in A))
            m.addConstr(b[i, k] >= 0.8 * tau * y[i])
            m.addConstr(b[i, k] <= tau * y[i] + tau * (1 - y[i]))
        m.addConstr(b[0, k] == tau)
        m.addConstr(b[N[-1], k] >= 0)

    for i in D:
        m.addConstr(y[i] == 0)

    m.addConstr(y[0] == 0)
    m.addConstr(y[N[-1]] == 0)
    m.addConstr(gp.quicksum(y[i] for i in N) <= MAX_STATIONS)

    u = m.addVars(range(1, N[-1]), K, vtype=GRB.CONTINUOUS, lb=1, ub=N[-1] - 1, name="u")
    for k in K:
        for i in range(1, N[-1]):
            for j in range(1, N[-1]):
                if i != j and (i, j) in A:
                    m.addConstr(u[i, k] - u[j, k] + (N[-1] - 1) * x[i, j, k] <= N[-1] - 2)




    m.setParam("TimeLimit", 60)
    m.setParam("OutputFlag", 0)
    m.optimize()

    if m.Status in [GRB.OPTIMAL, GRB.TIME_LIMIT]:
        print(f"\nObjective Value (Coverage): {m.ObjVal:.1f}")
        print("Charging stations at nodes:", [i for i in N if y[i].X>0.5])

        routes = {}
        for k in K:
            # reconstruct route
            curr = 0
            route = []
            while curr != N[-1]:
                for (i,j) in A:
                    if x[i,j,k].X > 0.5 and i==curr:
                        route.append((i, j))
                        curr = j
                        break
            routes[k] = route
    else:
        print("No solution found.")
    charging_stations = [i for i in N if y[i].X > 0.5]
    plot_solution(N, D, d, A, x, y, routes, charging_stations)
