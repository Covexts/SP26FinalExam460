# Development Log – The Torchbearer

**Student Name:** Christian Manalo
**Student ID:** 130370419
---

## Entry 1 – [5/11/2026]: Initial Plan


In order to make sure no torchbearer dies on my watch, my first step is to add dijkstras as the job requires me to find the shortest path to certain rooms which is what disjkstras does. I will also add a search algorithms that goes through different paths to find the cheapest route. I expect trying to find dead routes to cut off early to be the most difficult. I plan to test it by using the example tests.

---

## Entry 2 – [5/13/2026]: Source selection bug

I ran into a bug with select_sources. What I did was include the exit node as a source and ran the algorithim... I realized that this wasted an extra step as didn't need to include it since torchbearer never moves once at the exit node. I resolved it by simply removing it as a source node and ran tests to make sure the values were correct.
---

## Entry 3 – [5/14/2026]: Implemented search

Implemented find_optimal_route and _explore. I ran into an issue with backtracking as I didn't remove the relic from the visited list after recursing. This meant the same relic was being skipped on other branches. I also added the lower bound pruning which helped cut off bad routes early. Most of the tests passed nicely after fixing!

---

## Entry 4 – [5/14/2026]: Post-Implementation Reflection

The implemnation is now complete! If i had more time I would have liked to find a way to avoid rechecking paths that have already been visited at a lower cost. I would also test more different scenarioes like if the start and exit are the same room or when there are no relics to collect at all. The solution works for small inputs but if there were a lot of relics it would get very slow since there are so many possible orders to check.

---

## Final Entry – [5/14/2026]: Time Estimate

| Part | Estimated Hours |
|---|---|
| Part 1: Problem Analysis | 1 |
| Part 2: Precomputation Design | 1 |
| Part 3: Algorithm Correctness | 2 |
| Part 4: Search Design | 2 |
| Part 5: State and Search Space | 2 |
| Part 6: Pruning | 3 |
| Part 7: Implementation | 4 |
| README and DEVLOG writing | 2 |
| **Total** | 17 |
