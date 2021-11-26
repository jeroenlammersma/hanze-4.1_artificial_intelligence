import random
import heapq
import math
import config as cf

from typing import Dict, List, Tuple, Union

# global var
grid  = [[0 for x in range(cf.SIZE)] for y in range(cf.SIZE)]

class PriorityQueue:
    # a wrapper around heapq (aka priority queue), a binary min-heap on top of a list
    def __init__(self):
        # create a min heap (as a list)
        self.elements = []
    
    def empty(self) -> bool:
        return len(self.elements) == 0
    
    # heap elements are tuples (priority, item)
    def put(self, item: Tuple[int, int], priority: Union[int, float]):
        heapq.heappush(self.elements, (priority, item))
    
    # pop returns the smallest item from the heap
    # i.e. the root element = element (priority, item) with highest priority
    def pop(self) -> Tuple[int, Tuple[int, int]]:
        return heapq.heappop(self.elements)

def bernoulli_trial(app):
    return 1 if random.random() < int(app.prob.get())/10 else 0

def get_grid_value(node: Tuple[int, int]) -> int:
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    return grid[node[0]][node[1]]

def set_grid_value(node: Tuple[int, int], value): 
    # node is a tuple (x, y), grid is a 2D-list [x][y]
    grid[node[0]][node[1]] = value

def get_neighbors(point):
    neighbors = set()

    if point[1] - 1 >= 0 and grid[point[0]][point[1] - 1] != 'b':
        neighbors.add((point[0], point[1] - 1))

    if point[1] + 1 < cf.SIZE and grid[point[0]][point[1] + 1] != 'b':
        neighbors.add((point[0], point[1] + 1))

    if point[0] - 1 >= 0 and grid[point[0] - 1][point[1]] != 'b':
        neighbors.add((point[0] - 1, point[1]))

    if point[0] + 1 < cf.SIZE and grid[point[0] + 1][point[1]] != 'b':
        neighbors.add((point[0] + 1, point[1]))

    return neighbors

def get_children(node: Tuple[int, int]) -> List[Tuple[int, int]]:
    neighbours = []

    x = node[0]
    y = node[1]

    if x != 0 and get_grid_value((x - 1, y)) != 'b':
        neighbours.append((x - 1, y))
    if x < (len(grid) - 1) and get_grid_value((x + 1, y)) != 'b':
        neighbours.append((x + 1, y))
    if y != 0 and get_grid_value((x, y - 1)) != 'b':
        neighbours.append((x, y - 1))
    if y < (len(grid) - 1) and get_grid_value((x, y + 1)) != 'b':
        neighbours.append((x, y + 1))

    return neighbours

def plot_node(app, source_node: Tuple[int, int], destination_node: Tuple[int, int]):
    app.plot_line_segment(
        source_node[0],
        source_node[1],
        destination_node[0],
        destination_node[1],
        color=cf.PATH_C
    )

    app.plot_node(destination_node, color=cf.BG_C)

def get_costs(source_node: Tuple[int, int], destination_node: Tuple[int, int]):
    return (abs(source_node[0] - destination_node[0])) + (abs(source_node[1] - destination_node[1]))

def heuristic(node: Tuple[int, int], goal: Tuple[int, int]) -> float:
    x = goal[0] - node[0]
    y = goal[1] - node[1]
    return 2 * math.hypot(x, y)

def search(app, start: tuple[int, int], goal: tuple[int, int]):
    frontier = PriorityQueue()
    visited = set()
    path = dict()

    visited.add(start)
    set_grid_value(start, 0)
    frontier.put(start, 0)

    while not frontier.empty():
        (cost, parent) = frontier.pop()

        if parent == goal:
            plot_solution(app, path, start, goal)
            return path

        for child in get_neighbors(parent):
            if app.alg.get() == "A*":
                new_cost = get_costs(parent, child)
            else:
                new_cost = cost + get_costs(parent, child)

            if child not in visited or new_cost < get_grid_value(child):
                visited.add(child)
                set_grid_value(child, new_cost)

                if (app.alg.get() == "A*"):
                    new_cost += heuristic(child, goal)

                frontier.put(child, new_cost)

                path[child] = parent
                plot_node(app, parent, child)

        app.pause()
    
def plot_solution(app, path: Dict, start: Tuple[int, int], goal: Tuple[int, int]):
    node = goal
    next_node = path[node]

    while next_node != start:
        app.plot_line_segment(
            node[0],
            node[1],
            next_node[0],
            next_node[1],
            color=cf.FINAL_C
        )

        node = path[node]
        next_node = path[node]
    
    app.plot_line_segment(
        node[0],
        node[1],
        next_node[0],
        next_node[1],
        color=cf.FINAL_C
    )
