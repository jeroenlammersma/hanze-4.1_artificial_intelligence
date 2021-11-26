import numpy as np
from typing import List, Tuple

NR_OF_COLS = 7
NR_OF_ROWS = 6

grid = np.array([
    [1, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 1, 1, 0, 1],
    [0, 0, 1, 0, 1, 1, 0],
    [0, 1, 1, 0, 0, 1, 1],
    [0, 1, 0, 0, 0, 0, 1]
])

def prepare(mx: List[List[np.int64]]) -> Tuple[bool, List[int], List[int], List[List[int]], List[List[int]]]:
    # note that when applying alg-x we're only interested in 1's
    # so we add 2 lists that define where the 1's are
    rows = mx    
    # note that zip(*b) is the transpose of b
    cols = [list(i) for i in zip(*rows)]

    print(np.array(rows), '\n')

    def find_ones(rows: List[List[np.int64]]):
        # returns indexes in rows where the ondes are
        # example: [[0, 3], [1, 3], [1, 2], [2]]
        lv_row_has_1_at = []
        for row in rows:
            x = []
            for i in range(len(row)):
                if row[i] == 1:
                    x.append(i)
            lv_row_has_1_at.append(x.copy())
        return lv_row_has_1_at

    row_has_1_at = find_ones(rows) # read-only list; example: [[0, 3], [1, 3], [1, 2], [2]]
    col_has_1_at = find_ones(cols) # read-only list; example: [[0], [1, 2], [2, 3], [0, 1]]

    # if there's a col without ones, then there is no exact cover possible
    halt_fl = False
    for l in col_has_1_at:
        if l == []:
            print("No solution possible!")
            halt_fl = True

    row_valid = NR_OF_ROWS * [1]
    col_valid = NR_OF_COLS * [1]

    return halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at

def cover(r: int, row_valid: List[int], col_valid: List[int], row_has_1_at: List[List[int]], col_has_1_at: List[List[int]]):
    # given a row r:
    #   cover all cols that have a 1 in row r
    #   cover all rows r' that intersect/overlap with row r
    # returns row_valid, col_valid

    # iterate over cols where col on row has 1
    # cover col in col_valid
    for col_idx in row_has_1_at[r]:
        col_valid[col_idx] = 0

        # iterate over rows while getting list of indices of ones on row
        # if col index present, cover row
        for row_idx, row in enumerate(row_has_1_at):
            if col_idx in row:
                row_valid[row_idx] = 0

    return row_valid, col_valid

def solve(row_valid: List[int], col_valid: List[int], row_has_1_at: List[List[int]], col_has_1_at: List[List[int]], solution: List[int]):
    # using Algoritm X, find all solutions (= set of rows) given valid/uncovered rows and cols

    def get_lowest_ones_col() -> int:
        lowest_ones_count = float('INF')
        lowest_ones_col = -1

        # iterate over cols
        for col_idx in range(len(col_valid)):

            # if col is valid (uncovered) and number of ones in col is lower than lowest_ones_count
            if col_valid[col_idx] and (ones_count := len(col_has_1_at[col_idx])) < lowest_ones_count:

                # update lowest ones col
                lowest_ones_count = ones_count
                lowest_ones_col = col_idx

        return lowest_ones_col

    # solution found if no more ones in col_valid
    if not any(col_valid):
        print(solution)
        return
    
    # get col with lowest number of ones
    lowest_ones_col = get_lowest_ones_col()
    
    # iterate over rows which have a one in lowest_ones_col
    for row in col_has_1_at[lowest_ones_col]:
        # proceed if row is valid (uncovered)
        if row_valid[row]:
            # add row to (partial) solution
            solution.append(row)

            # cover rows and cols, creating a reduced matrix
            reduced_row_valid, reduced_col_valid = cover(row, row_valid.copy(), col_valid.copy(), row_has_1_at, col_has_1_at)

            # repeat algorithm recursively on matrix
            solve(reduced_row_valid, reduced_col_valid, row_has_1_at, col_has_1_at, solution)

            # remove row from solution
            solution.remove(row)
    

halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at = prepare(grid)

if not halt_fl:
    solve(row_valid, col_valid, row_has_1_at, col_has_1_at, [])
