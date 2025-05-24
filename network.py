# network.py

def get_saev_network_parameters():
    """
    Returns SAEV LRP instance parameters:
        N: List of node indices
        D: Dictionary of demand nodes with priority
        tau: SAEV battery capacity
        MIN_RECHARGE: Minimum recharge amount
        MAX_STATIONS: Maximum number of charging stations
        d: Distance matrix
    """
    D = {7: 3, 11: 2, 5: 1}
    tau = 2000
    MIN_RECHARGE = 1000
    MAX_STATIONS = 3
    d = [
        [0, 320, 0, 0, 0, 0, 0, 0, 0, 310, 0, 0],
        [320, 0, 350, 0, 0, 0, 0, 0, 0, 0, 260, 0],
        [0, 350, 0, 200, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 200, 0, 450, 0, 0, 290, 0, 0, 0, 0],
        [0, 0, 0, 450, 0, 250, 0, 320, 0, 0, 0, 0],
        [0, 0, 0, 0, 250, 0, 320, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 320, 0, 280, 0, 0, 0, 0],
        [0, 0, 0, 290, 320, 0, 280, 0, 350, 310, 310, 0],
        [0, 0, 0, 0, 0, 0, 0, 350, 0, 350, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 310, 350, 0, 260, 310],
        [310, 260, 0, 0, 0, 0, 0, 310, 0, 260, 0, 300],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 310, 300, 0]
    ]

    n = len(d)
    # Post-processing, as in original input code
    for i in range(n):
        d[i].append(d[i][0])
    d.append([0] * (n + 1))
    d[n][1] = d[0][1]
    if n > 10:
        d[n][10] = d[0][10]

    return list(range(n + 1)), D, tau, MIN_RECHARGE, MAX_STATIONS, d
