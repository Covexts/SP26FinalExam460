"""
CS 460 – Algorithms: Final Programming Assignment
The Torchbearer

Student Name: Christian Manalo
Student ID:   130370419

INSTRUCTIONS
------------
- Implement every function marked TODO.
- Do not change any function signature.
- Do not remove or rename required functions.
- You may add helper functions.
- Variable names in your code must match what you define in README Part 5a.
- The pruning safety comment inside _explore() is graded. Do not skip it.

Submit this file as: torchbearer.py
"""

import heapq


# =============================================================================
# PART 1
# =============================================================================

def explain_problem():
    """
    Returns
    -------
    str
        Your Part 1 README answers, written as a string.
        Must match what you wrote in README Part 1.
    """
    return """"
    Why a single shortest-path run from S is not enough
    A single shortest path run from S using Dijkstra's gives the cheapest
    path to each room, but not the order to visit the relic chambers.
    
    What decision remains after all inter-location costs are known:
    After all inter-location costs are known, the only decision remaining
    is to determine what order to visit the relic chambers.

    Why this requires a search over orders:
    Since the total fuel cost changes depending on the order you visit the
    relic chambers, you have to search different routes and keep track of the cheapest route."
    """



# =============================================================================
# PART 2
# =============================================================================

def select_sources(spawn, relics, exit_node):
    """
    Parameters
    ----------
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    list[node]
        No duplicates. Order does not matter.
    """
    # only need to run dijkstra from spawn and each relic
    # Skip exit_node because torchbearer will never go to diff node once there
    seen = set()
    sources = []
    for node in [spawn] + list(relics):
        if node not in seen:
            seen.add(node)
            sources.append(node)
    return sources

def run_dijkstra(graph, source):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
        graph[u] = [(v, cost), ...]. All costs are nonnegative integers.
    source : node

    Returns
    -------
    dict[node, float]
        Minimum cost from source to every node in graph.
        Unreachable nodes map to float('inf').

    """
    dist = {node: float('inf') for node in graph} # set every node to infinity to start
    dist[source] = 0 # source set to 0
 
    pq = [(0, source)] # min heap
 
    while pq:
        d, u = heapq.heappop(pq)
 
        if d > dist[u]: # if there is a cheaper way skip
            continue
 
        for v, cost in graph.get(u, []): # check all neigbhbors and change if cheaper path found
            new_dist = dist[u] + cost
            if new_dist < dist[v]:
                dist[v] = new_dist
                heapq.heappush(pq, (new_dist, v))
 
    return dist


def precompute_distances(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    dict[node, dict[node, float]]
        Nested structure supporting dist_table[u][v] lookups
        for every source u your design requires.

    """
    # run dijkstra once from each source and store the results
    sources = select_sources(spawn, relics, exit_node)
    dist_table = {}
    for src in sources:
        dist_table[src] = run_dijkstra(graph, src) # dist_table[u][v] gives the cheapest cost from u to v
    return dist_table


# =============================================================================
# PART 3
# =============================================================================

def dijkstra_invariant_check():
    """
    Returns
    -------
    str
        Your Part 3 README answers, written as a string.
        Must match what you wrote in README Part 3.
    """
    return """
   Part 3a: Invariant Explanation

    For nodes already finalized (in S): When a node is finalized its shortest distance is correct so it will never change.

    For nodes not yet finalized (not in S): For nodes not yet finalized, the distance stored is the best found so far but can change if something cheaper appears.

    Part 3b: Invariant Maintenance

    Initialization : At start, source node is = 0 and every other node to infinity because we havent found any paths.

    Maintenance : Always finalize node with lowest cost because since all edge are nonnegative, no other path can be cheaper.

    Termination : When the algorithm ends, every reachable node is set to its shortest distance. Any node still at infinity cannot be reached.

    Part 3c: Why Correctness Matters

    If any of the distances are wrong the torchbearer might make wrong decisions such as choosing to go a more expensive route even though theres a cheaper option


    """


# =============================================================================
# PART 4
# =============================================================================

def explain_search():
    """
    Returns
    -------
    str
        Your Part 4 README answers, written as a string.
        Must match what you wrote in README Part 4.
    """

    return """
    Part 4: Search Design

    Why Greedy Fails


    The failure mode: Greedy will always go to nearest unvisited relic however choosing the next cheapest node will not mean it will be the cheapest distance overall
    Counter-example setup: Starting from S the next available nodes are A B and T. A has a cost of 1, S to B has a cost of 3, A to B has a cost of 10,B to A costs 1, A to T costs 1, and B to T costs 10
    What greedy picks: Greedy would pick A as it is the lowest cost of 1,, then B cost 10, then T cost 10 with a total cost of 21
    What optimal picks: Optimal would pick B with a cost of 3, A cost 1, and T cost 1 with total cost of 5
    Why greedy loses: Greedy loses because since it always chooses A first with a low cost, it always locks into the path with a high cost and doesn't look for cheaper costs

    ### What the Algorithm Must Explore

    The algorithm must explore every possible route to visit the relics and return the order that has the lowest total cost.
    """


# =============================================================================
# PARTS 5 + 6
# =============================================================================

def _lower_bound(dist_table, current_loc, relics_remaining, exit_node):
    """
    Added helper function to estimates the minimum remaining fuel needed from the current state.
    It always underesitames to make sure it is safe for pruning.
    """
    if not relics_remaining:
        return dist_table[current_loc].get(exit_node, float('inf'))
 
    # all relics still needed to visit with exit
    required = relics_remaining | {exit_node}
    bound = 0.0
 
    # find cheapest way out for every possible place to leave
    for src in [current_loc] + list(relics_remaining):
        min_out = float('inf')
        for dest in required:
            if dest != src:
                d = dist_table.get(src, {}).get(dest, float('inf'))
                if d < min_out:
                    min_out = d
        bound += min_out
 
    return bound

def find_optimal_route(dist_table, spawn, relics, exit_node):
    """
    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
        Output of precompute_distances.
    spawn : node
    relics : list[node]
        Every node in this list must be visited at least once.
    exit_node : node
        The route must end here.

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    # edge case
    # if there are no relics to collect then go to exit
    if not relics:
        cost = dist_table.get(spawn, {}).get(exit_node, float('inf'))
        return (cost, [])
 
    # best[0] best cost found 
    # best[1] relic order that got that cost
    best = [float('inf'), []]
 
    # uses a set for O(1) add remove and check if relic is in set
    relics_remaining = set(relics)
    relics_visited_order = []
 
    _explore(
        dist_table,
        current_loc=spawn,
        relics_remaining=relics_remaining,
        relics_visited_order=relics_visited_order,
        cost_so_far=0.0,
        exit_node=exit_node,
        best=best,
    )
 
    return (best[0], best[1])


def _explore(dist_table, current_loc, relics_remaining, relics_visited_order,
             cost_so_far, exit_node, best):
    """
    Recursive helper for find_optimal_route.

    Parameters
    ----------
    dist_table : dict[node, dict[node, float]]
    current_loc : node
    relics_remaining : collection
        Your chosen data structure from README Part 5b.
    relics_visited_order : list[node]
    cost_so_far : float
    exit_node : node
    best : list
        Mutable container for the best solution found so far.

    Returns
    -------
    None
        Updates best in place.
    Implement: base case, pruning, recursive case, backtracking.

    REQUIRED: Add a 1-2 sentence comment near your pruning condition
    explaining why it is safe (cannot skip the optimal solution).
    This comment is graded.
    """
# ------------------------------------------------------------------
# Pruning
# ------------------------------------------------------------------
    lb = _lower_bound(dist_table, current_loc, relics_remaining, exit_node)
 
    # this prune is safe because the lower bound never overestimates remaining fuel cost
    # no route through this branch can ever be cheaper than what we already found
    if cost_so_far + lb >= best[0]:
        return
 
# ------------------------------------------------------------------
# Base case
# ------------------------------------------------------------------
    if not relics_remaining:
        final_cost = cost_so_far + dist_table[current_loc].get(exit_node, float('inf'))
        if final_cost < best[0]:
            best[0] = final_cost
            best[1] = list(relics_visited_order)
        return
 
# ------------------------------------------------------------------
# Rrcursive case
# ------------------------------------------------------------------
    for relic in list(relics_remaining):
        travel_cost = dist_table.get(current_loc, {}).get(relic, float('inf'))
 
        # skip if we can't reach this relic
        if travel_cost == float('inf'):
            continue
 
        # choose this relic next
        relics_remaining.remove(relic)
        relics_visited_order.append(relic)
 
        _explore(
            dist_table,
            current_loc=relic,
            relics_remaining=relics_remaining,
            relics_visited_order=relics_visited_order,
            cost_so_far=cost_so_far + travel_cost,
            exit_node=exit_node,
            best=best,
        )
 
        # backtrack to try other ordering
        relics_remaining.add(relic)
        relics_visited_order.pop()


# =============================================================================
# PIPELINE
# =============================================================================

def solve(graph, spawn, relics, exit_node):
    """
    Parameters
    ----------
    graph : dict[node, list[tuple[node, int]]]
    spawn : node
    relics : list[node]
    exit_node : node

    Returns
    -------
    tuple[float, list[node]]
        (minimum_fuel_cost, ordered_relic_list)
        Returns (float('inf'), []) if no valid route exists.

    """
    dist_table = precompute_distances(graph, spawn, relics, exit_node) # precompute shortest distances between points
    return find_optimal_route(dist_table, spawn, relics, exit_node) # find optomial or cheapest route to visit all relics


# =============================================================================
# PROVIDED TESTS (do not modify)
# Graders will run additional tests beyond these.
# =============================================================================

def _run_tests():
    print("Running provided tests...")

    # Test 1: Spec illustration. Optimal cost = 4.
    graph_1 = {
        'S': [('B', 1), ('C', 2), ('D', 2)],
        'B': [('D', 1), ('T', 1)],
        'C': [('B', 1), ('T', 1)],
        'D': [('B', 1), ('C', 1)],
        'T': []
    }
    cost, order = solve(graph_1, 'S', ['B', 'C', 'D'], 'T')
    assert cost == 4, f"Test 1 FAILED: expected 4, got {cost}"
    print(f"  Test 1 passed  cost={cost}  order={order}")

    # Test 2: Single relic. Optimal cost = 5.
    graph_2 = {
        'S': [('R', 3)],
        'R': [('T', 2)],
        'T': []
    }
    cost, order = solve(graph_2, 'S', ['R'], 'T')
    assert cost == 5, f"Test 2 FAILED: expected 5, got {cost}"
    print(f"  Test 2 passed  cost={cost}  order={order}")

    # Test 3: No valid path to exit. Must return (inf, []).
    graph_3 = {
        'S': [('R', 1)],
        'R': [],
        'T': []
    }
    cost, order = solve(graph_3, 'S', ['R'], 'T')
    assert cost == float('inf'), f"Test 3 FAILED: expected inf, got {cost}"
    print(f"  Test 3 passed  cost={cost}")

    # Test 4: Relics reachable only through intermediate rooms.
    # Optimal cost = 6.
    graph_4 = {
        'S': [('X', 1)],
        'X': [('R1', 2), ('R2', 5)],
        'R1': [('Y', 1)],
        'Y': [('R2', 1)],
        'R2': [('T', 1)],
        'T': []
    }
    cost, order = solve(graph_4, 'S', ['R1', 'R2'], 'T')
    assert cost == 6, f"Test 4 FAILED: expected 6, got {cost}"
    print(f"  Test 4 passed  cost={cost}  order={order}")

    # Test 5: Explanation functions must return non-placeholder strings.
    for fn in [explain_problem, dijkstra_invariant_check, explain_search]:
        result = fn()
        assert isinstance(result, str) and result != "TODO" and len(result) > 20, \
            f"Test 5 FAILED: {fn.__name__} returned placeholder or empty string"
    print("  Test 5 passed  explanation functions are non-empty")

    print("\nAll provided tests passed.")


if __name__ == "__main__":
    _run_tests()
