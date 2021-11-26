from copy import deepcopy
from pprint import pprint
from typing import List, Tuple

s = """
0  0  0  0  0  0  0  0 81
0  0 46 45  0 55 74  0  0
0 38  0  0 43  0  0 78  0
0 35  0  0  0  0  0 71  0
0  0 33  0  0  0 59  0  0
0 17  0  0  0  0  0 67  0
0 18  0  0 11  0  0 64  0
0  0 24 21  0  1  2  0  0
0  0  0  0  0  0  0  0  0 """

CLUES = [
    (81, 8, 0),
    (46, 2, 1),
    (45, 3, 1),
    (55, 5, 1),
    (74, 6, 1),
    (38, 1, 2),
    (43, 4, 2),
    (78, 7, 2),
    (35, 1, 3),
    (71, 7, 3),
    (33, 2, 4),
    (59, 6, 4),
    (17, 1, 5),
    (67, 7, 5),
    (18, 1, 6),
    (11, 4, 6),
    (64, 7, 6),
    (24, 2, 7),
    (21, 3, 7),
    (1 , 5, 7),
    (2 , 6, 7)
]

def print_board(board):
    pprint(board)

def create_board(size: int, clues: List[Tuple[int, int, int]]) -> List[List[int]]:
    board = [ [0 for _ in range(size) ] for _ in range(size) ]

    for cell in clues:
        number = cell[0]
        x = cell[1]
        y = cell[2]

        board[y][x] = number

    return board

def create_clues_list(clues_tuple: List[Tuple[int, int, int]]) -> List[int]:
    clues = [ cell[0] for cell in clues_tuple ]
    clues.sort()
    return clues

def position_of_number(board: List[List[int]], number: int) -> Tuple[int, int]:
    for y, row in enumerate(board):
        for x, col in enumerate(row):
            if col == number:
                return (x, y)

    return (-1, -1)

def get_neighbours(board: List[List[int]], x: int, y: int) -> List[Tuple[int, int, int]]:
    neighbours = []
    board_size = len(board)

    if x != (board_size - 1): neighbours.append((board[y][x + 1], x + 1, y))
    if x != 0:                neighbours.append((board[y][x - 1], x - 1, y))
    if y != (board_size - 1): neighbours.append((board[y + 1][x], x, y + 1))
    if y != 0:                neighbours.append((board[y - 1][x], x, y - 1))

    return neighbours

def dfs(board, current_number, current_x, current_y, clues):
    if len(clues) == 0:
        print("solution found\n")
        print_board(board)
        return

    current_number += 1
    next_clue = clues[0]
    neighbours = get_neighbours(board, current_x, current_y)

    for neighbour in neighbours:
        n = neighbour[0]
        x = neighbour[1]
        y = neighbour[2]

        board_copy = deepcopy(board)
        clues_copy = deepcopy(clues)

        if n == next_clue and current_number == next_clue:
            dfs(board_copy, current_number, x, y, clues_copy[1:])
        elif n == 0:
            board_copy[y][x] = current_number
            dfs(board_copy, current_number, x, y, clues_copy)


def find_solution(board, clues):
    current_number = 1
    clues = clues[1:]
    start_x, start_y = position_of_number(board, current_number)
    
    dfs(board, current_number, start_x, start_y, clues)

clues = CLUES
board = create_board(9, clues)

board = [
    [1, 0],
    [4, 0]
]
clues = [1, 4]

board = [
    [10, 0, 0, 0],
    [0, 0, 0, 16],
    [0, 1, 0, 3],
    [0, 6, 0, 0]
]
clues = [1, 3, 6, 10, 16]


board = [
    [0,  0,  0,  0,  0,  0,  0,  0, 81],
    [0,  0, 46, 45,  0, 55, 74,  0,  0],
    [0, 38,  0,  0, 43,  0,  0, 78,  0],
    [0, 35,  0,  0,  0,  0,  0, 71,  0],
    [0,  0, 33,  0,  0,  0, 59,  0,  0],
    [0, 17,  0,  0,  0,  0,  0, 67,  0],
    [0, 18,  0,  0, 11,  0,  0, 64,  0],
    [0,  0, 24, 21,  0,  1,  2,  0,  0],
    [0,  0,  0,  0,  0,  0,  0,  0,  0]
]
clues = []
for y in board:
    for x in y:
        if x != 0:
            clues.append(x)
clues.sort()

find_solution(board, clues)