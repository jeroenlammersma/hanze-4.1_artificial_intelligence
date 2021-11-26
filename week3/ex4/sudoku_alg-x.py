import numpy as np
import time

from collections import namedtuple
from typing import Dict, List, Tuple


Cell = namedtuple('Cell', 'row col digit')
Y_idx = namedtuple('Y_idx', 'cell row column box')


def cross(A: str, B: str) -> List[str]:
    # concat of chars in string A and chars in string B
    return [a+b for a in A for b in B]

DIGITS = '123456789'
ROWS   = 'ABCDEFGHI'
COLS   = DIGITS
CELLS  = cross(ROWS, COLS) # 81 cells A1..9, B1

SUDOKU_SIZE = 9

SUDOKU_BOX_WIDTH = int(SUDOKU_SIZE ** .5)
SUDOKU_VALUE_COUNT = SUDOKU_SIZE

SUDOKU_CELL_COUNT = SUDOKU_SIZE ** 2

GROUP_OFFSET_CELLS   = 0 * SUDOKU_CELL_COUNT
GROUP_OFFSET_ROWS    = 1 * SUDOKU_CELL_COUNT
GROUP_OFFSET_COLUMNS = 2 * SUDOKU_CELL_COUNT
GROUP_OFFSET_BOXES   = 3 * SUDOKU_CELL_COUNT

NR_OF_ROWS = SUDOKU_SIZE ** 3
NR_OF_COLS = SUDOKU_SIZE ** 2 * 4


def parse_list_to_string(solution: List[int]) -> str:
    # make sure list is sorted in asc order
    solution.sort()

    sudoku_str = ''
    # iterator over row indices in solution
    for row_idx in solution:
        # calculate digit from row index and append to sudoku string
        sudoku_str += str(calc_digit(row_idx))
    return sudoku_str


def display(grid: Dict[str, str]):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in ROWS:
        for c in COLS:
            v = grid[r+c]
            # avoid the '123456789'
            if v == '123456789': 
                v = '.'
            print (''.join(v), end=' ')
            if c == '3' or c == '6': print('|', end='')
        print()
        if r == 'C' or r == 'F': 
            print('-------------------')
    print()


def parse_string_to_dict(grid_string: str) -> Dict[str, str]:
    # grid_string is a string like '4.....8.5.3..........7......2.....6....   '
    # convert grid_string into a dict of {cell: chars}
    char_list1 = [c for c in grid_string if c in DIGITS or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(CELLS, char_list2))


def print_solution(solution: List[int]) -> None:
    solution_str = parse_list_to_string(solution)
    solution_dict = parse_string_to_dict(solution_str)
    display(solution_dict)


def prepare(mx: List[List[np.int64]]) -> Tuple[bool, List[int], List[int], List[List[int]], List[List[int]]]:
    # note that when applying alg-x we're only interested in 1's
    # so we add 2 lists that define where the 1's are
    rows = mx
    # note that zip(*b) is the transpose of b
    cols = [list(i) for i in zip(*rows)]

    # print(np.array(rows), '\n')

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

    # read-only list; example: [[0, 3], [1, 3], [1, 2], [2]]
    row_has_1_at = find_ones(rows)
    # read-only list; example: [[0], [1, 2], [2, 3], [0, 1]]
    col_has_1_at = find_ones(cols)

    # if there's a col without ones, then there is no exact cover possible
    halt_fl = False
    for l in col_has_1_at:
        if l == []:
            print("No solution possible!")
            halt_fl = True

    row_valid = NR_OF_ROWS * [1]
    col_valid = NR_OF_COLS * [1]

    return halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at


def cover(r: int, row_valid: List[int], col_valid: List[int], row_has_1_at: List[List[int]], col_has_1_at: List[List[int]]) -> Tuple[List[int], List[int]]:
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
        print_solution(solution)
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
            reduced_row_valid, reduced_col_valid = cover(
                row, row_valid.copy(), col_valid.copy(), row_has_1_at, col_has_1_at)

            # repeat algorithm recursively on matrix
            solve(reduced_row_valid, reduced_col_valid,
                  row_has_1_at, col_has_1_at, solution)

            # remove row from solution
            solution.remove(row)


def calc_row(row_idx: int) -> int:
    return row_idx // SUDOKU_CELL_COUNT


def calc_column(row_idx: int) -> int:
    row_idx %= SUDOKU_CELL_COUNT
    return row_idx // SUDOKU_SIZE


def calc_digit(row_idx: int) -> int:
    return row_idx % SUDOKU_SIZE + 1


def get_row_col_digit(row_idx: int) -> Cell:
    row = calc_row(row_idx)
    col = calc_column(row_idx)
    digit = calc_digit(row_idx)
    return Cell(row, col, digit)


def calc_matrix_cells_y_index(row_idx: int) -> int:
    return GROUP_OFFSET_CELLS + row_idx // SUDOKU_VALUE_COUNT


def calc_matrix_rows_y_index(row_idx: int) -> int:
    # group offset + cell value + row offset
    return GROUP_OFFSET_ROWS + (row_idx % SUDOKU_SIZE) + ((row_idx // SUDOKU_CELL_COUNT) * SUDOKU_SIZE)


def calc_matrix_columns_y_index(row_idx: int) -> int:
    return GROUP_OFFSET_COLUMNS + (row_idx % SUDOKU_CELL_COUNT)


def calc_matrix_boxes_y_index(row_idx: int) -> int:
    row_offset_value = SUDOKU_VALUE_COUNT * SUDOKU_BOX_WIDTH ** 2 * SUDOKU_BOX_WIDTH
    row_offset = SUDOKU_CELL_COUNT // SUDOKU_BOX_WIDTH

    return GROUP_OFFSET_BOXES + ((row_idx % SUDOKU_SIZE) + (row_idx // (SUDOKU_SIZE * SUDOKU_BOX_WIDTH) * SUDOKU_SIZE)) % \
         (SUDOKU_BOX_WIDTH * SUDOKU_VALUE_COUNT) + ((row_idx // (row_offset_value)) * row_offset)


def get_matrix_y_indices(row_idx: int) -> Y_idx:
    cell = calc_matrix_cells_y_index(row_idx)
    row = calc_matrix_rows_y_index(row_idx)
    column = calc_matrix_columns_y_index(row_idx)
    box = calc_matrix_boxes_y_index(row_idx)
    return Y_idx(cell, row, column, box)


def calc_sudoku_str_idx_digit_to_row(idx: int, digit: int) -> int:
    # offset + digit minus 1 (first index == 0)
    return idx * SUDOKU_VALUE_COUNT + (digit - 1)


def create_matrix():
    mx = np.zeros((NR_OF_ROWS, NR_OF_COLS), dtype=np.int64)

    for i in range(NR_OF_ROWS):
        y = get_matrix_y_indices(i)

        mx[i, y.cell]   = 1
        mx[i, y.row]    = 1
        mx[i, y.column] = 1
        mx[i, y.box]    = 1

    return mx


def matrix_to_csv(mx: np.ndarray) -> None:
    np.savetxt("matrix.csv", fmt="%d", X=mx, delimiter=",")


def update_valid_rows_cols_using_clues(
    sudoku_str: str,
    row_valid: List[int],
    col_valid: List[int],
    row_has_1_at: List[List[int]],
    col_has_1_at: List[List[int]]
) -> Tuple[List[int], List[int]]:
    for idx, char in enumerate(sudoku_str):
        if char != '.':
            digit = int(char)
            row_idx = calc_sudoku_str_idx_digit_to_row(idx, digit)
            row_valid, col_valid = cover(row_idx, row_valid, col_valid, row_has_1_at, col_has_1_at)
    return row_valid, col_valid


def add_clues_to_solution(sudoku: str) -> List[int]:
    return [ calc_sudoku_str_idx_digit_to_row(idx, int(char)) for idx, char in enumerate(sudoku) if char != '.' ]


def reset_row_col_valid() -> Tuple[List[int], List[int]]:
    row_valid = NR_OF_ROWS * [1]
    col_valid = NR_OF_COLS * [1]
    return (row_valid, col_valid)


# minimum nr of clues for a unique solution is 17
slist = ['' for _ in range(20)]
slist[0] = '.56.1.3....16....589...7..4.8.1.45..2.......1..42.5.9.1..4...899....16....3.6.41.'
slist[1] = '.6.2.58...1....7..9...7..4..73.4..5....5..2.8.5.6.3....9.73....1.......93......2.'
slist[2] = '.....9.73.2.....569..16.2.........3.....1.56..9....7...6.34....7.3.2....5..6...1.'
slist[3] = '..1.3....5.917....8....57....3.1.....8..6.59..2.9..8.........2......6...315.9...8'
slist[4] = '....6.8748.....6.3.....5.....3.4.2..5.2........72...35.....3..........69....96487'
slist[5] = '.94....5..5...7.6.........71.2.6.........2.19.6...84..98.......51..9..78......5..'
slist[6] = '.5...98..7...6..21..2...6..............4.598.461....5.54.....9.1....87...2..5....'
slist[7] = '...17.69..4....5.........14.....1.....3.5716..9.....353.54.9....6.3....8..4......'
slist[8] = '..6.4.5.......2.3.23.5..8765.3.........8.1.6.......7.1........5.6..3......76...8.'
slist[9] = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[10]= '85...24..72......9..4.........1.7..23.5...9...4...........8..7..17..........36.4.'
slist[11]= '...5....2...3..85997...83..53...9...19.73...4...84...1.471..6...5...41...1...6247'
slist[12]= '.....6....59.....82....8....45........3........6..3.54...325..6..................'
slist[13]= '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
slist[14]= '8..........36......7..9.2...5...7.......457.....1...3...1....68..85...1..9....4..'
slist[15]= '6..3.2....5.....1..........7.26............543.........8.15........4.2........7..'
slist[16]= '.6.5.1.9.1...9..539....7....4.8...7.......5.8.817.5.3.....5.2............76..8...'
slist[17]= '..5...987.4..5...1..7......2...48....9.1.....6..2.....3..6..2.......9.7.......5..'
slist[18]= '3.6.7...........518.........1.4.5...7.....6.....2......2.....4.....8.3.....5.....'
slist[19]= '1.....3.8.7.4..............2.3.1...........958.........5.6...7.....8.2...4.......'


mx = create_matrix()
halt_fl, row_valid, col_valid, row_has_1_at, col_has_1_at = prepare(mx)


for i, sudo in enumerate(slist):
    print('*** sudoku {0} ***'.format(i))
    print(sudo)
    start_time = time.time()

    row_valid, col_valid = reset_row_col_valid()
    row_valid, col_valid = update_valid_rows_cols_using_clues(sudo, row_valid, col_valid, row_has_1_at, col_has_1_at)
    solution = add_clues_to_solution(sudo)
    solve(row_valid, col_valid, row_has_1_at, col_has_1_at, solution)

    end_time = time.time()
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(int(hours),int(minutes),seconds))
    print()