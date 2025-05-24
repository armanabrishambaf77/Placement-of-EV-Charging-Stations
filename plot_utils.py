# plot_utils.py

import matplotlib.pyplot as plt
import networkx as nx
from itertools import combinations
from matplotlib.lines import Line2D

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

def plot_solution(N, D, d, A, x, y):
    """Visualize the optimal SAEV route and charging station solution."""
    return_depot = N[-1]
    raw_path_arcs = [(i, j) for (i, j) in A if x[i, j].X > 0.5]
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

    prio_colors = {3: '#d73027', 2: '#fc8d59', 1: '#fee08b'}
    color_map = {0: '#006400'}
    for j in demand:
        color_map[j] = prio_colors[D[j]]
    for s in charged:
        color_map[s] = '#4575b4'
    for o in others:
        color_map[o] = '#dddddd'

    node_colors = [color_map[n] for n in G_plot.nodes()]
    pos = nx.kamada_kawai_layout(G_plot)

    fig, ax = plt.subplots(figsize=(12, 8), facecolor='white')
    ax.set_facecolor('white')
    nx.draw_networkx_edges(G_plot, pos, edgelist=G_plot.edges(),
                           width=1, edge_color='#cccccc', ax=ax)
    nx.draw_networkx_edges(G_plot, pos, edgelist=path_arcs,
                           width=3, edge_color='#2166ac', ax=ax)
    nx.draw_networkx_nodes(G_plot, pos, node_size=600,
                           node_color=node_colors, edgecolors='black', linewidths=1.2, ax=ax)
    nx.draw_networkx_labels(G_plot, pos, font_weight='bold', font_size=12, ax=ax)
    nx.draw_networkx_edge_labels(G_plot, pos,
        edge_labels={(i, j): G_plot[i][j]['weight'] for i, j in G_plot.edges()},
        font_size=10, ax=ax)

    legend_elems = [
        Line2D([0], [0], marker='o', color='w', label='Depot',
               markerfacecolor=color_map[0], markersize=12, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Demand Node (High Priority)',
               markerfacecolor=prio_colors[3], markersize=12, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Demand Node (Medium Priority)',
               markerfacecolor=prio_colors[2], markersize=12, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Demand Node (Low Priority)',
               markerfacecolor=prio_colors[1], markersize=12, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='Charging Station',
               markerfacecolor='#4575b4', markersize=12, markeredgecolor='black'),
        Line2D([0], [0], color='#2166ac', lw=3, label='Optimal Route')
    ]
    ax.legend(handles=legend_elems, loc='upper right', frameon=False)
    ax.set_title('SAEV Network – Depot, Demand Nodes & Charging Stations', fontsize=16)
    plt.tight_layout()
    plt.show()
