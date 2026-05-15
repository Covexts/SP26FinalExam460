# The Torchbearer

**Student Name:** Christian Manalo
**Student ID:** 130370419
**Course:** CS 460 – Algorithms | Spring 2026
---

## Part 1: Problem Analysis

- **Why a single shortest-path run from S is not enough:**
  Single shortest path run from s using dijkstras gives cheapest path to each room, but not the order to visit the relic chambers.

- **What decision remains after all inter-location costs are known:**
 After all inter-location costs are known, the only decision remains is to determine what order to visit the relic chambers.

- **Why this requires a search over orders (one sentence):**
Since the total fuel cost changes depending on the order you visit the relic chambers, you have to search different routes and keep track of the cheapest route.

---

## Part 2: Precomputation Design

### Part 2a: Source Selection

| Source Node Type | Why it is a source |
|---|---|
| Entrance | It starts at the entrance node and we find cheapest route from entrance to every relic |
| Relic | We travel to any unvisited relic or to an exit so we need to find distances from each relic |

### Part 2b: Distance Storage

| Property | Your answer |
|---|---|
| Data structure name | Nested dictionary |
| What the keys represent | Outer key is the source node, inner key is destination node |
| What the values represent | Cheapest path cost from sourch to destination|
| Lookup time complexity | O(1) |
| Why O(1) lookup is possible | Dictionary uses a hashtable which is O(1) |

### Part 2c: Precomputation Complexity

- **Number of Dijkstra runs:** _K + 1 total, one from each of the relics k, and one from spawn_
- **Cost per run:** _O(m log n)_
- **Total complexity:** _O((k + 1) * m log n) = O(k * m log n)_
- **Justification (one line):** _Runs Dijkstra once per source and every run has a cost of O(m log n)_
---

## Part 3: Algorithm Correctness

### Part 3a: Invariant Explanation

- **For nodes already finalized (in S):**
  _When a node is finalized its shortest distance is correct so it will never change._

- **For nodes not yet finalized (not in S):**
  _For nodes not yet finalized, the distance stored is the best found so far but can change if something cheaper appears._

### Part 3b: Invariant Maintenance

- **Initialization : why the invariant holds before iteration 1:**
  _At start, source node is = 0 and every other node to infinity because we havent found any paths._

- **Maintenance : why finalizing the min-dist node is always correct:**
  _Always finalize node with lowest cost because since all edge are nonnegative, no other path can be cheaper._

- **Termination : what the invariant guarantees when the algorithm ends:**
  _When the algorithm ends, every reachable node is set to its shortest distance._
  _Any node still at infinity cannot be reached._

### Part 3c: Why Correctness Matters

_If any of the distances are wrong the torchbearer might make wrong decisions such as choosing to go a more expensive route even though theres a cheaper option._

---

## Part 4: Search Design

### Why Greedy Fails

- **The failure mode:** _Greedy will always go to nearest unvisited relic however choosing the next cheapest node will not mean it will be the cheapest distance overall._
- **Counter-example setup:** _Starting from S the next available nodes are A B and T. A has a cost of 1, S to B has a cost of 3, A to B has a cost of 10,B to A costs 1, A to T costs 1, and B to T costs 10._
- **What greedy picks:** _Greedy would pick A as it is the lowest cost of 1,, then B cost 10, then T cost 10 with a total cost of 21._
- **What optimal picks:** _Optimal would pick B with a cost of 3, A cost 1, and T cost 1 with total cost of 5._
- **Why greedy loses:** _Greedy loses because since it always chooses A first with a low cost, it always locks into the path with a high cost and doesn't look for cheaper costs._

### What the Algorithm Must Explore

- _The algorithm must explore every possible route to visit the relics and return the order that has the lowest total cost._

---

## Part 5: State and Search Space

### Part 5a: State Representation

| Component | Variable name in code | Data type | Description |
|---|---|---|---|
| Current location | current_loc | node| The room where the torchbearer currently is|
| Relics not yet collected | relics_remaining | set[node] | Tracks what relics have not been collected |
| Fuel cost so far | cost_so_far | float | The total fuel used so far |

### Part 5b: Data Structure for Visited Relics

| Property | Your answer |
|---|---|
| Data structure chosen | set |
| Operation: check if relic already collected | Time complexity: O(1) |
| Operation: mark a relic as collected | Time complexity: O(1) |
| Operation: unmark a relic (backtrack) | Time complexity: O(1) |
| Why this structure fits | All thre operations have a O(1) time complexity on a hash set and if you undo a move when backtracking you can just add the relic back|

### Part 5c: Worst-Case Search Space

- **Worst-case number of orders considered:** _k!._
- **Why:** _You have k relics to choose from and every time you do it becomes k-1, k-2..., until there is none left. Multiplying those give k!._

---

## Part 6: Pruning

### Part 6a: Best-So-Far Tracking

- **What is tracked:** _Cheapest completed route fond so far and the relic order._
- **When it is used:** _It is used before exploring a new branch, it checks if that branch can lead to a better route._
- **What it allows the algorithm to skip:** _It allows to skip any branch that cannot lead to a better route._

### Part 6b: Lower Bound Estimation

- **What information is available at the current state:** _We know how much fuel has been used, current location, and unvisited relics._
- **What the lower bound accounts for:** _It accounts for the cheapest possible trip from current location to any relic and cheapest possible route to any remaining relic to the exit._
- **Why it never overestimates:** _It uses precomputed shortest path distances and always picks the minumum so it can only be <= remaining cost._

### Part 6c: Pruning Correctness

- _Pruning is safe becasuse we only cut a branch hen the cheapest possible route of that branch is worse than the best route found so far._

---

## References

- _Lecture notes_
- _Python Documentation, Data Structures (Sets), https://docs.python.org/3/tutorial/datastructures.html Used for Part 5b to understand how to implement a set in Python using set(), add() and remove(). Verified by testing the same syntax in my code and confirmed all tests passed_
- _GeeksforGeeks, Internal Working of Set in Python, https://www.geeksforgeeks.org/internal-working-of-set-in-python/ Used for Part 5b to confirm that set operations like add, remove, and lookup run O(1) due to hashing. Verified by checking with the Python documentation which states the same time complexities_
