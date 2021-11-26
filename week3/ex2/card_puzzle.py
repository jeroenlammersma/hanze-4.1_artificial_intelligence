import itertools

from copy import deepcopy
from typing import Dict, List

'''Constraints:
    1 every Ace borders a King
    2 every King borders a Queen
    3 every Queen borders a Jack
    4 no Ace borders a Queen
    5 no two of the same cards border each other

'''
# the board has 8 cells, let’s represent the board with a dict key=cell, value=card
start_board = {cell: '.' for cell in range(8)}
cards = ['K', 'K', 'Q', 'Q', 'J', 'J', 'A', 'A']
neighbors = {0: [3], 1: [2], 2: [1, 4, 3], 3: [0, 2, 5],
             4: [2, 5], 5: [3, 4, 6, 7], 6: [5], 7: [5]}


def is_valid(board: Dict[int, str]) -> bool:

    # to check if card is in neighbours of cell
    def card_in_neighbours(card: str, cell: int) -> bool:
        for n in neighbors[cell]:
            if card == board[n]:
                return True

        return False

    # check if more than 2 of the same card exist on board
    if (
        sum(map(('K').__eq__, board.values())) > 2 or
        sum(map(('Q').__eq__, board.values())) > 2 or
        sum(map(('J').__eq__, board.values())) > 2 or
        sum(map(('A').__eq__, board.values())) > 2
    ):
        return False

    # order in which cells will be validated
    order = [5, 3, 2, 4, 0, 1, 6, 7]

    for cell in order:
        card = board[cell]

        # empty cell, continue
        if card == '.':
            continue

        # (5) check if two of same cards border each other
        if card_in_neighbours(card, cell):
            return False

        # (4) first check if Ace does not border Queen
        # (1) then check if Ace borders a King if no more empty neighbouring cells
        if (
            card == 'A' and (card_in_neighbours('Q', cell) or
            (not card_in_neighbours('.', cell) and not card_in_neighbours('K', cell)))
        ):
            return False

        # (3) check if Queen borders a Jack if no more empty neighbouring cells
        if (
            card == 'Q'
            and not card_in_neighbours('.', cell)
            and not card_in_neighbours('J', cell)
        ):
            return False

        # (2) check if King borders a Queen if no more empty neighbouring cells
        if (
            card == 'K'
            and not card_in_neighbours('.', cell)
            and not card_in_neighbours('Q', cell)
        ):
            return False

    return True


def test() -> None:
    # is_valid(board) checks all cards, returns False if any card is invalid
    print('f ', is_valid({0: 'J', 1: 'K', 2: 'Q', 3: 'Q', 4: 'J', 5: 'K', 6: 'A', 7: 'A'}))
    print('f ', is_valid({0: 'J', 1: 'J', 2: 'Q', 3: 'Q', 4: 'K', 5: 'K', 6: 'A', 7: 'A'}))
    print('t ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('t ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: 'J', 4: 'J', 5: 'A', 6: 'J', 7: 'J'}))  # [1]
    print('f ', is_valid({0: 'J', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'K', 6: 'J', 7: 'Q'}))  # [3]
    print('t ', is_valid({0: '.', 1: 'Q', 2: '.', 3: '.', 4: 'Q', 5: 'J', 6: '.', 7: '.'}))  # [3]
    print('f ', is_valid({0: 'Q', 1: '.', 2: '.', 3: 'K', 4: '.', 5: '.', 6: '.', 7: '.'}))  # [3]
    print('f ', is_valid({0: '.', 1: 'A', 2: 'Q', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: '.'}))  # [4]
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: 'J', 5: 'J', 6: '.', 7: '.'}))  # [5]
    print('f ', is_valid({0: '.', 1: '.', 2: '.', 3: '.', 4: '.', 5: 'Q', 6: '.', 7: 'Q'}))  # [5]
    print('t ', is_valid({0: 'Q', 1: 'Q', 2: '.', 3: '.', 4: '.', 5: '.', 6: '.', 7: '.'}))


def brute_force():
    permuations = {p for p in list(itertools.permutations(cards))}
    
    for p in permuations:
        board = {cell: p[cell] for cell in range(8)}
        if is_valid(board):
            print(board)
    
# brute_force()


def dfs():
    solutions = []

    def search():
        for cell in range(8):
            if start_board[cell] == '.':
                for card in cards:
                    board_copy = deepcopy(start_board)
                    board_copy[cell] = card
                    if is_valid(board_copy):
                        start_board[cell] = card
                        search()
                        start_board[cell] = '.'
                return
        if start_board not in solutions:
            solutions.append(deepcopy(start_board))
    
    search()
    [print(solution) for solution in solutions]

dfs()
