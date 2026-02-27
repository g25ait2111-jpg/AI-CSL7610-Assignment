import heapq
import time
from collections import deque

# ===============================
# Utility Functions
# ===============================

def get_neighbors(state):
    neighbors = []
    idx = state.index('B')
    row, col = divmod(idx, 3)

    moves = []
    if row > 0: moves.append(-3)
    if row < 2: moves.append(3)
    if col > 0: moves.append(-1)
    if col < 2: moves.append(1)

    for move in moves:
        new = list(state)
        swap = idx + move
        new[idx], new[swap] = new[swap], new[idx]
        neighbors.append(tuple(new))

    return neighbors


def misplaced(state, goal):
    return sum(1 for i in range(9) if state[i] != goal[i] and state[i] != 'B')


def manhattan(state, goal):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 'B':
            continue
        goal_idx = goal.index(tile)
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_idx, 3)
        distance += abs(x1 - x2) + abs(y1 - y2)
    return distance


# ===============================
# BFS
# ===============================

def bfs(start, goal):
    start_time = time.time()
    queue = deque([(start, [])])
    visited = set([start])
    states = 0

    while queue:
        state, path = queue.popleft()
        states += 1

        if state == goal:
            return path, states, time.time() - start_time

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return None, states, time.time() - start_time


# ===============================
# DFS
# ===============================

def dfs(start, goal):
    start_time = time.time()
    stack = [(start, [])]
    visited = set()
    states = 0

    while stack:
        state, path = stack.pop()
        states += 1

        if state == goal:
            return path, states, time.time() - start_time

        if state not in visited:
            visited.add(state)
            for neighbor in get_neighbors(state):
                stack.append((neighbor, path + [neighbor]))

    return None, states, time.time() - start_time


# ===============================
# A* Search
# ===============================

def astar(start, goal, heuristic_name):
    start_time = time.time()
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set()
    states = 0

    while pq:
        f, state, path = heapq.heappop(pq)
        states += 1

        if state == goal:
            return path, states, time.time() - start_time

        if state in visited:
            continue

        visited.add(state)

        for neighbor in get_neighbors(state):
            g = len(path) + 1

            if heuristic_name == "Manhattan":
                h = manhattan(neighbor, goal)
            else:
                h = misplaced(neighbor, goal)

            heapq.heappush(pq, (g + h, neighbor, path + [neighbor]))

    return None, states, time.time() - start_time


# ===============================
# MAIN
# ===============================

if __name__ == "__main__":

    # Read input file
    with open("input.txt", "r") as file:
        lines = file.readlines()

    start_str = lines[0].split(":")[1].strip()
    goal_str = lines[1].split(":")[1].strip()
    algorithm = lines[2].split(":")[1].strip()

    heuristic_name = None
    if algorithm == "A*":
        heuristic_name = lines[3].split(":")[1].strip()

    start = tuple(int(x) if x != 'B' else 'B' for x in start_str)
    goal = tuple(int(x) if x != 'B' else 'B' for x in goal_str)

    print("========================================")
    print("Algorithm Used:", algorithm)
    if heuristic_name:
        print("Heuristic Used:", heuristic_name)
    print("Start State:", start)
    print("Goal State:", goal)
    print("========================================")

    if algorithm == "BFS":
        path, states, t = bfs(start, goal)

    elif algorithm == "DFS":
        path, states, t = dfs(start, goal)

    elif algorithm == "A*":
        path, states, t = astar(start, goal, heuristic_name)

    else:
        print("Invalid Algorithm Selected")
        exit()

    if path is not None:
        print("Status: Success")
        print("Total Moves:", len(path))
        print("Total States Explored:", states)
        print("Total Time Taken:", round(t, 5), "seconds")
    else:
        print("Status: Failure")
