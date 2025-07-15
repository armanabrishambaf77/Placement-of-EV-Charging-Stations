# network.py
# 1. SAEV Network Parameters
def get_saev_network_parameters():
    """
    Returns SAEV LRP instance parameters:
        N: List of node indices
        D: Dictionary of demand nodes with priority
        tau: SAEV battery capacity
        MAX_STATIONS: Maximum number of charging stations
        d: Distance matrix
    """
    # 1.1. Demand Nodes with Priorities
    D = {13: 3, 12: 3 ,5: 2 ,11: 2, 8: 1, 4:1}
    # 1.2. Set Battery Capacity and Maximum Stations
    tau = 1500
    MAX_STATIONS = 2
    # 1.3. Distance Matrix
    d = [
        [0,   320, 0,   0,   0,   0,   0,   0,   0,   0,   310, 0,   0,   0],
        [320, 0,   350, 0,   0,   0,   0,   0,   0,   0,   260, 0,   0,   0],
        [0,   350, 0,   200, 0,   0,   0,   0,   0,   0,   0,   0,   0,   0],
        [0,   0,   200, 0,   450, 0,   0,   290, 0,   0,   0,   0,   235, 0],
        [0,   0,   0,   450, 0,   250, 0,   320, 0,   0,   0,   0,   295, 310],
        [0,   0,   0,   0,   250, 0,   320, 0,   0,   0,   0,   0,   0,   200],
        [0,   0,   0,   0,   0,   320, 0,   280, 0,   0,   0,   0,   0,   230],
        [0,   0,   0,   290, 320, 0,   280, 0,   350, 310, 310, 0,   0,   0],
        [0,   0,   0,   0,   0,   0,   0,   350, 0,   350, 0,   0,   0,   0],
        [0,   0,   0,   0,   0,   0,   0,   310, 350, 0,   260, 310, 0,   0],
        [310, 260, 0,   0,   0,   0,   0,   310, 0,   260, 0,   300, 0,   0],
        [0,   0,   0,   0,   0,   0,   0,   0,   0,   310, 300, 0,   0,   0],
        [0,   0,   0,   235, 310, 0,   0,   0,   0,   0,   0,   0,   0,   300],
        [0,   0,   0,   0,   310, 200, 230, 0,   0,   0,   0,   0,   300, 0],
    ]

    n = len(d)
    # Post-processing, as in original input code
    for i in range(n):
        d[i].append(d[i][0])
    d.append(d[0][:])
    
    return list(range(n + 1)), D, tau, MAX_STATIONS, d
