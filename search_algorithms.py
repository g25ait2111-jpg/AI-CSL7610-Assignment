import heapq
import time
from collections import deque
import math
import random

GOAL = (1,2,3,4,5,6,7,'B',8)

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

def misplaced(state):
    return sum(1 for i in range(9) if state[i] != GOAL[i] and state[i] != 'B')

def manhattan(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 'B': continue
        goal_idx = GOAL.index(tile)
        x1, y1 = divmod(i, 3)
        x2, y2 = divmod(goal_idx, 3)
        distance += abs(x1-x2) + abs(y1-y2)
    return distance

def bfs(start):
    start_time = time.time()
    queue = deque([(start, [])])
    visited = set([start])
    states = 0

    while queue:
        state, path = queue.popleft()
        states += 1
        if state == GOAL:
            return path, states, time.time()-start_time

        for neighbor in get_neighbors(state):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path+[neighbor]))

    return None, states, time.time()-start_time

def astar(start, heuristic):
    start_time = time.time()
    pq = []
    heapq.heappush(pq, (0, start, []))
    visited = set()
    states = 0

    while pq:
        f, state, path = heapq.heappop(pq)
        states += 1

        if state == GOAL:
            return path, states, time.time()-start_time

        if state in visited:
            continue

        visited.add(state)

        for neighbor in get_neighbors(state):
            g = len(path) + 1
            h = heuristic(neighbor)
            heapq.heappush(pq, (g+h, neighbor, path+[neighbor]))

    return None, states, time.time()-start_time

if __name__ == "__main__":
    start = (1,2,3,'B',4,6,7,5,8)

    print("Running BFS...")
    path, states, t = bfs(start)
    print("Moves:", len(path))
    print("States explored:", states)
    print("Time:", t)

    print("\nRunning A* (Manhattan)...")
    path, states, t = astar(start, manhattan)
    print("Moves:", len(path))
    print("States explored:", states)
    print("Time:", t)