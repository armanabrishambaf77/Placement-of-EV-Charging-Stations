# plot_utils.py

import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations
from matplotlib.lines import Line2D
from matplotlib.patches import FancyArrowPatch  

# 3. SAEVs Network Visualization

# 3.1. Network Visualization
def plot_network(N, D, d):
    """Visualize SAEV network: depot, demand, and other nodes."""
    return_depot = N[-1]
    G = nx.Graph()
    for i, j in combinations(N, 2):
        if d[i][j] > 0 and return_depot not in (i, j):
            G.add_edge(i, j, weight=d[i][j])

    depot = [0]
    demand = list(D.keys())
    others = [n for n in G.nodes() if n not in depot + demand]

    custom_gradient = ['#FF0000', '#FF6666', '#CC66FF', '#9966CC', '#663399']
    unique_prios = sorted(set(D.values()), reverse=True)
    prio_colors = {}

    for i, p in enumerate(unique_prios):
        color_idx = min(i, len(custom_gradient) - 1)
        prio_colors[p] = custom_gradient[color_idx]

    color_map = {0: '#006400'}
    for j in demand:
        color_map[j] = prio_colors[D[j]]
    for o in others:
        color_map[o] = '#dddddd'

    node_colors = [color_map[n] for n in G.nodes()]
    pos = nx.kamada_kawai_layout(G)

    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    ax.set_facecolor('white')
    nx.draw_networkx_edges(G, pos, width=1, edge_color='#cccccc', ax=ax)
    nx.draw_networkx_nodes(G, pos, node_size=600, node_color=node_colors,
                           edgecolors='black', linewidths=1.2, ax=ax)
    nx.draw_networkx_labels(G, pos, font_weight='bold', font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G, pos,
        edge_labels={(i, j): G[i][j]['weight'] for i, j in G.edges()},
        font_size=10, ax=ax)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Depot',
               markerfacecolor=color_map[0], markeredgecolor='black', markersize=12),
        Line2D([0], [0], marker='o', color='w', label='Other Nodes',
               markerfacecolor='#dddddd', markeredgecolor='black', markersize=12)
    ]
    for p in sorted(unique_prios, reverse=True):
        legend_elements.append(
            Line2D([0], [0], marker='o', color='w',
                   label=f"Demand (Priority {p})",
                   markerfacecolor=prio_colors[p],
                   markeredgecolor='black', markersize=12)
        )

    ax.legend(handles=legend_elements, loc='upper right', frameon=False)
    ax.set_title("SAEV Network – Depot, Demand Nodes & Other Nodes", fontsize=16)
    plt.tight_layout()
    plt.show()

    # 3.2. Optimal Route and Charging Station Visualization
def plot_solution(N, D, d, A, x, y, routes, charging_stations):
    """Visualize the optimal SAEV route and charging station solution."""
    return_depot = N[-1]
    raw_path_arcs = [(i, j) for (i, j) in A if (i, j) in x and x[i, j].X > 0.5]
    stations = [i for i in N if y[i].X > 0.5]

    path_arcs = []
    for i, j in raw_path_arcs:
        i2 = 0 if i == return_depot else i
        j2 = 0 if j == return_depot else j
        if i2 != j2:
            path_arcs.append((i2, j2))
    path_arcs = list(set(path_arcs))

    G_plot = nx.Graph()
    for i, j in combinations(N, 2):
        if d[i][j] > 0 and return_depot not in (i, j):
            G_plot.add_edge(i, j, weight=d[i][j])

    depot = [0]
    demand = list(D.keys())
    charged = [i for i in stations if i != 0]
    others = [n for n in G_plot.nodes() if n not in depot + demand + charged]

    custom_gradient = ['#FF4C4C', '#FF9999', '#9B59B6']
    unique_prios = sorted(set(D.values()), reverse=True)
    prio_colors = {}
    for i, p in enumerate(unique_prios):
        color_idx = min(i, len(custom_gradient) - 1)
        prio_colors[p] = custom_gradient[color_idx]

    color_map = {0: '#006400'}
    for j in demand:
        color_map[j] = prio_colors[D[j]]
    for s in charged:
        color_map[s] = '#FFD700'
    for o in others:
        color_map[o] = '#dddddd'

    node_colors = [color_map[n] for n in G_plot.nodes()]
    pos = nx.kamada_kawai_layout(G_plot)

    def add_arrows(G, pos, ax, route, route_color, line_style):
        for (i, j) in route:
            x_start, y_start = pos[i]
            x_end, y_end = pos[j]

            line = FancyArrowPatch(
                posA=(x_start, y_start), posB=(x_end, y_end),
                arrowstyle='-', color=route_color, linewidth=3, linestyle=line_style
            )

            if line_style == '--':
                line.set_linestyle((0, (10, 10)))
            ax.add_patch(line)
            
            arrowhead = FancyArrowPatch(
                posA=(x_start, y_start), posB=((x_start + x_end) / 2, (y_start + y_end) / 2),
                arrowstyle='-|>', color=route_color, linewidth=0, mutation_scale=25
            )

            ax.add_patch(arrowhead)


    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    ax.set_facecolor('white')
    nx.draw_networkx_edges(G_plot, pos, width=1, edge_color='#cccccc', ax=ax)
    nx.draw_networkx_nodes(G_plot, pos, node_size=600, node_color=node_colors,edgecolors='black', linewidths=1.2, ax=ax)
    nx.draw_networkx_labels(G_plot, pos, font_weight='bold', font_size=12, ax=ax)
    route_colors = ['#FF4500', '#00008B']  # Adjusted vibrant red for clarity
    line_styles = ['-', '--']

    for k, route in routes.items():
        adjusted_route = [(0 if i == return_depot else i, 0 if j == return_depot else j) for i, j in route]
        add_arrows(G_plot, pos, ax, adjusted_route, route_colors[k-1], line_styles[k-1])


    legend_elems = [
        Line2D([0], [0], marker='o', color='w', label='Depot', markerfacecolor=color_map[0], markersize=12, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Charging Station', markerfacecolor='#FFD700', markersize=12, markeredgecolor='black'),
    ]

    for p in unique_prios:
        legend_elems.append(Line2D([0], [0], marker='o', color='w', label=f'Demand (Priority {p})', markerfacecolor=prio_colors[p], markersize=12, markeredgecolor='black'))

    legend_elems.extend([
        Line2D([0], [0], color=route_colors[0], lw=3, linestyle='-', label='SAEV 1 Route'),
        Line2D([0], [0], color=route_colors[1], lw=3, linestyle='--', label='SAEV 2 Route'),
    ])

    ax.legend(handles=legend_elems, loc='upper right', frameon=False)
    ax.set_title('SAEV Network – Depot, Demand Nodes & Charging Stations', fontsize=16)
    plt.tight_layout()
    plt.show()
