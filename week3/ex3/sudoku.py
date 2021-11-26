import time

from typing import Dict, List

#   1 2 3 4 .. 9
# A
# B
# C
# D
# ..
# I

def cross(A: str, B: str) -> List[str]:
    # concat of chars in string A and chars in string B
    return [a+b for a in A for b in B]

digits = '123456789'
rows   = 'ABCDEFGHI'
cols   = digits
cells  = cross(rows, cols) # 81 cells A1..9, B1..9, C1..9, ... 

# unit = a row, a column, a box; list of all units
unit_list = ([cross(r, cols) for r in rows] +                             # 9 rows 
             [cross(rows, c) for c in cols] +                             # 9 cols
             [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]) # 9 units


units = dict((s, [u for u in unit_list if s in u]) for s in cells)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in cells)

def test() -> None:
    # a set of tests that must pass
    assert len(cells) == 81
    assert len(unit_list) == 27
    assert all(len(units[s]) == 3 for s in cells)
    assert all(len(peers[s]) == 20 for s in cells)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2'],
                           ['C1', 'C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9'],
                           ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']]
    assert peers['C2'] == set(['A2', 'B2', 'D2', 'E2', 'F2', 'G2', 'H2', 'I2',
                               'C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9',
                               'A1', 'A3', 'B1', 'B3'])
    print ('All tests pass.')

def display(grid: Dict[str, str]):
    # grid is a dict of {cell: string}, e.g. grid['A1'] = '1234'
    print()
    for r in rows:
        for c in cols:
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
    char_list1 = [c for c in grid_string if c in digits or c == '.']
    # char_list1 = ['8', '5', '.', '.', '.', '2', '4', ...  ]
    
    assert len(char_list1) == 81

    # replace '.' with '1234567'
    char_list2 = [s.replace('.', '123456789') for s in char_list1]

    # grid {'A1': '8', 'A2': '5', 'A3': '123456789',  }
    return dict(zip(cells, char_list2))

def no_conflict(grid: Dict[str, str], c: str, val: str) -> bool:
    # check if assignment is possible: value v not a value of a peer
    for p in peers[c]:
        if grid[p] == val:
           return False # conflict
    return True

def solution_found(grid: Dict[str, str]) -> bool:
    """
    Check if solution is found

    :param grid: sudoku board
    :return: True if solution found, else False
    """
    for val in grid.values():
        if len(val) != 1:
            return False
    return True

def remove_peer_values_using_clues(grid: Dict[str, str]) -> Dict[str, str]:
    """
    Remove the value of the clues from the corresponding peers

    :param grid: sudoku board
    :return: sudoku board
    """
    for cell, val in grid.items():
        if len(val) == 1 and val in digits:
            for p in peers[cell]:
                grid[p] = grid[p].replace(val, '')
    return grid

def grids_equal(grid1: Dict[str, str], grid2: Dict[str, str]) -> bool:
    """
    Check whether two grids are equal

    :param grid1: first sudoku board
    :param grid2: second sudoku board
    :return: True if
    """
    for cell, val in grid1.items():
        if grid2[cell] is not val:
            return False
    return True

def solve(grid: Dict[str, str], algorithm: str):
    # remove all impossible values from peers using clues
    remove_peer_values_using_clues(grid)

    # backtracking search for a solution (DFS)
    if algorithm == 'dfs':
        def dfs():
            # iterate over grid
            for cell, val in grid.items():
                # if no value set yet (if set: it has just one value)
                if len(val) > 1:
                    # iterate over candidate digits from value
                    for digit in val:
                        # if value is potential candidate
                        if no_conflict(grid, cell, digit):
                            # remove digit from value
                            val.replace(digit, '')
                            # set digit on cell
                            grid[cell] = digit
                            # recursively call dfs 
                            dfs()
                            # set value (excluding digit) on cell
                            grid[cell] = val

                    # if conflict, return
                    return

            # if solution found, show it
            display(grid)

        # initial call to dfs
        dfs()
    
    if algorithm == 'arc':
        def make_arc_concistent(grid: Dict[str, str], cell: str, digit: str) -> bool:
            # create copy of grid (used to see if grid changed)
            grid_copy = grid.copy()

            # iterate over peers of cell
            for p in peers[cell]:
                # if digit present in peer
                if digit in grid[p]:
                    # if peer has only 1 digit
                    if len(grid[p]) == 1:
                        # there is a conflict, no solution on this path
                        return False
                    else:
                        # else, remove digit from peer
                        grid[p] = grid[p].replace(digit, '')
            
            # if grid is changed
            if not grids_equal(grid, grid_copy):
                # iterate over grid
                for cell, val in grid.items():
                    # if cell has only one value
                    if len(val) == 1:
                        # recursively call make_arc_concistent
                        if not make_arc_concistent(grid, cell, val):
                            # if conflict, then return False
                            return False
            
            # if grid not changed or no conflicts, return True
            return True

        def arc(grid: Dict[str, str]):
            if solution_found(grid):
                # display grid if solution found
                display(grid)
                return True
            
            # iterate over grid
            for cell, val in grid.items():
                # if no value set yet (if set: it has just one value)
                if len(val) > 1:
                    # iterate over candidate digits from value
                    for digit in val:
                        # if value is potential candidate
                        if no_conflict(grid, cell, digit):
                            # create copy of grid
                            grid_copy = grid.copy()
                            
                            # set digit on cell
                            grid_copy[cell] = digit

                            # if no conflicts during make_arc_concistent
                            if make_arc_concistent(grid_copy, cell, digit):
                                # recursively call arc
                                # if true, solution is found
                                if arc(grid_copy):
                                    return True
                    
                    # no solution, go back up
                    return False

        # inital call to arc
        arc(grid)


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

for i, sudo in enumerate(slist):
    print('*** sudoku {0} ***'.format(i))
    print(sudo)
    d = parse_string_to_dict(sudo)
    start_time = time.time()
    solve(d, 'arc')
    end_time = time.time()
    hours, rem = divmod(end_time-start_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print("duration [hh:mm:ss.ddd]: {:0>2}:{:0>2}:{:06.3f}".format(int(hours),int(minutes),seconds))
    print()
