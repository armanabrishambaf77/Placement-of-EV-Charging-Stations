# main.py

from network import get_saev_network_parameters
from plot_utils import plot_network, plot_solution
from optimizer import build_and_solve_model

if __name__ == "__main__":
    N, D, tau, MAX_STATIONS, d = get_saev_network_parameters()
    print("\n✅ SAEV Model Parameters Loaded:")
    print(f"- Number of nodes (including return depot): {len(N)}")
    print(f"- Demand nodes and priorities: {D}")
    print(f"- SAEV battery capacity (tau): {tau}")
    print(f"- Max number of charging stations: {MAX_STATIONS}")
    plot_network(N, D, d)
    build_and_solve_model(N, D, tau, d, MAX_STATIONS, plot_solution=plot_solution)
