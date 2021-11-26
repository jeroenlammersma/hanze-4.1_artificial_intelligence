import random
random.seed(1)
import itertools
import math

from collections import namedtuple
from tkinter.constants import S
from typing import List, Tuple, Union

from copy import deepcopy

Cell = namedtuple("Cell", "x y")
Move = namedtuple("Move", "move score")

MAX_DEPTH = 3

def merge_left(b: Union[List[List[int]], "zip[Tuple[int]]"]) -> List[List[int]]:
    # merge the board left
    # this function is reused in the other merges
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]    
    def merge(row: List[int], acc: List[int]):
        # recursive helper for merge_left
        # if len row == 0, return accumulator
        if not row:
            return acc

        # x = first element
        x = row[0]
        # if len(row) == 1, add element to accu
        if len(row) == 1:
            return acc + [x]
        # if len(row) >= 2
        if x == row[1]:
            # add row[0] + row[1] to accu, continue with row[2:]
            return merge(row[2:], acc + [2 * x])
        else:
            # add row[0] to accu, continue with row[1:]
            return merge(row[1:], acc + [x])

    new_b = []
    for row in b:
        # merge row, skip the [0]'s
        merged = merge([x for x in row if x != 0], [])
        # add [0]'s to the right if necessary
        merged = merged + [0] * (len(row) - len(merged))
        new_b.append(merged)
    # return [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    return new_b

def merge_right(b: Union[List[List[int]], "zip[Tuple[int]]"]) -> List[List[int]]:
    # merge the board right
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    def reverse(x: Union[List[int], Tuple[int]]) -> List[int]:
        return list(reversed(x))

    # rev = [[4, 4, 2, 0], [8, 4, 2, 0], [4, 0, 0, 0], [2, 2, 2, 2]]
    rev = [reverse(x) for x in b]
    # ml = [[8, 2, 0, 0], [8, 4, 2, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    ml = merge_left(rev)
    # return [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    return [reverse(x) for x in ml]

def merge_up(b: List[List[int]]) -> List[List[int]]:
    # merge the board upward
    # note that zip(*b) is the transpose of b
    # b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    # trans = [[2, 0, 0, 0], [4, 2, 0, 0], [8, 2, 0, 0], [4, 8, 4, 2]]
    trans = merge_left(zip(*b))
    # return [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    return [list(x) for x in zip(*trans)]

def merge_down(b: List[List[int]]) -> List[List[int]]:
    # merge the board downward
    trans = merge_right(zip(*b))
    # return [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    return [list(x) for x in zip(*trans)]

# location: after functions
MERGE_FUNCTIONS = {
    'left': merge_left,
    'right': merge_right,
    'up': merge_up,
    'down': merge_down
}

def move_exists(b: List[List[int]]) -> bool:
    # check whether or not a move exists on the board
    # b = [[1, 2, 3, 4], [5, 6, 7, 8]]
    # move_exists(b) return False
    def inner(b: Union[List[List[int]], "zip[Tuple[int]]"]) -> bool:
        for row in b:
            for x, y in zip(row[:-1], row[1:]):
                # tuples (1, 2),(2, 3),(3, 4),(5, 6),(6, 7),(7, 8)
                # if same value or an empty cell
                if x == y or x == 0 or y == 0:
                    return True
        return False

    # check horizontally and vertically
    if inner(b) or inner(zip(*b)):
        return True
    else:
        return False

def start() -> List[List[int]]:
    # make initial board
    b = [[0] * 4 for _ in range(4)]
    add_two_four(b)
    add_two_four(b)
    return b

def play_move(b: List[List[int]], direction: str) -> List[List[int]]:
    # get merge functin an apply it to board
    b = MERGE_FUNCTIONS[direction](b)
    add_two_four(b)
    return b

def add_two_four(b: List[List[int]]) -> Union[List[List[int]], None]:
    # add a random tile to the board at open position.
    # chance of placing a 2 is 90%; chance of 4 is 10%
    rows, cols = list(range(4)), list(range(4))
    random.shuffle(rows)
    random.shuffle(cols)
    distribution = [2] * 9 + [4]
    for i, j in itertools.product(rows, cols):
        if b[i][j] == 0:
            b[i][j] = random.sample(distribution, 1)[0]
            return (b)
        else:
            continue
            
def game_state(b: List[List[int]]) -> str:
    for i in range(4):
        for j in range(4):
            if b[i][j] >= 2048:
                return 'win'
    return 'lose'

def test():
    b = [[0, 2, 4, 4], [0, 2, 4, 8], [0, 0, 0, 4], [2, 2, 2, 2]]
    assert merge_left(b) == [[2, 8, 0, 0], [2, 4, 8, 0], [4, 0, 0, 0], [4, 4, 0, 0]]
    assert merge_right(b) == [[0, 0, 2, 8], [0, 2, 4, 8], [0, 0, 0, 4], [0, 0, 4, 4]]
    assert merge_up(b) == [[2, 4, 8, 4], [0, 2, 2, 8], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert merge_down(b) == [[0, 0, 0, 4], [0, 0, 0, 8], [0, 2, 8, 4], [2, 4, 2, 2]]
    assert move_exists(b) == True
    b = [[2, 8, 4, 0], [16, 0, 0, 0], [2, 0, 2, 0], [2, 0, 0, 0]]
    assert (merge_left(b)) == [[2, 8, 4, 0], [16, 0, 0, 0], [4, 0, 0, 0], [2, 0, 0, 0]]
    assert (merge_right(b)) == [[0, 2, 8, 4], [0, 0, 0, 16], [0, 0, 0, 4], [0, 0, 0, 2]]
    assert (merge_up(b)) == [[2, 8, 4, 0], [16, 0, 2, 0], [4, 0, 0, 0], [0, 0, 0, 0]]
    assert (merge_down(b)) == [[0, 0, 0, 0], [2, 0, 0, 0], [16, 0, 4, 0], [4, 8, 2, 0]]
    assert (move_exists(b)) == True
    b = [[32, 64, 2, 16], [8, 32, 16, 2], [4, 16, 8, 4], [2, 8, 4, 2]]
    assert (move_exists(b)) == False
    b = [[0, 7, 0, 0], [0, 0, 7, 7], [0, 0, 0, 7], [0, 7, 0, 0]]
    for i in range(11):
        add_two_four(b)
        print(b)

def get_random_move() -> str:
    return random.choice(list(MERGE_FUNCTIONS.keys()))

def get_expectimax_move(b: List[List[int]]) -> str:
    depth = 4
    heuristic = heuristic_2048

    # get result of every move
    results = [ (move, expectimax(func(b), depth, False, heuristic)) for move, func in MERGE_FUNCTIONS.items() ]

    # return move with best score
    return max(results, key = lambda x: x[1])[0]

def get_empty_tiles(b: List[List[int]]) -> List[Cell]:
    return [ Cell(x, y) for x in range(len(b)) for y in range(len(b)) if b[y][x] == 0 ]

def max_value(b: List[List[int]]) -> int:
    m = -1

    for y in b:
        for x in y:
            m = max(m, x)

    return m

def heuristic_2048(b: List[List[int]]) -> float:
    # if game is loss, return worst possible outcome
    if not move_exists(b):
        return -float("INF")
    
    # snake pattern strategy
    board_weights = [
        [15, 14, 13, 12],
        [ 8,  9, 10, 11],
        [ 7,  6,  5,  4],
        [ 0,  1,  2,  3]
    ]

    # get score for board using weights
    # heavier weights weigh relatively more
    score = 0
    for y, row in enumerate(b):
        for x, col in enumerate(row):
            score += col * 10 ** board_weights[y][x]

    # penalize if max value not in upper left hand corner
    maxval = max_value(b)
    corner = b[0][0]
    if corner != maxval:
        score -= abs(corner - maxval) ** 2

    return score

def expectimax(b: List[List[int]], depth: int, player: bool, heuristic):
    # when maximum depth reached or no more moves, calculate score
    if depth == 0 or (player and not move_exists(b)):
        return heuristic(b)

    # init score
    score = 0

    if player:
        # for all merge functions, get best score
        for func in MERGE_FUNCTIONS.values():
            score = max(score, expectimax(func(b), depth - 1, False, heuristic))

    else:
        empty_tiles = get_empty_tiles(b)

        # for each empty tile
        for tile in empty_tiles:
            # create 2 copies of board
            b1 = deepcopy(b)
            b2 = deepcopy(b)

            x = tile.x
            y = tile.y

            # place 2 on first board, 4 on second
            b1[y][x] = 2
            b2[y][x] = 4

            # calculate average score, 90% change new tile is 2, 10% change new tile is 4
            score += .9 * expectimax(b1, depth - 1, True, heuristic) / len(empty_tiles) + \
                     .1 * expectimax(b2, depth - 1, True, heuristic) / len(empty_tiles)

    return score
