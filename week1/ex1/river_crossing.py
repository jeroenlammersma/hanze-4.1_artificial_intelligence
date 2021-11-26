from copy import deepcopy
from typing import List

STARTING_STATE = ['CFGW', '']

VALID_STATES = [
    '',
    'CFGW',
    'CW',
    'FG',
    'G',
    'CFW',
    'FGW',
    'C',
    'CFG',
    'W'
]

solutions = []

def solution_found(state: List) -> bool:
    return state[1] == 'CFGW'

def valid_state(state: List) -> bool:
    return state[0] in VALID_STATES and state[1] in VALID_STATES

def already_visited(state: List, visited_states: List) -> bool:
    return state in visited_states

def get_successors(state: List, visited_states: List) -> List:
    next_states = get_next_states(state)
    successors = [ state for state in next_states if valid_state(state) and not already_visited(state, visited_states) ]
    return successors
    
def get_next_states(state: List) -> List:
    next_states = []
    
    # determine position of farmer
    f_pos = 0 if state[0].find('F') != -1 else 1

    # move farmer with all possible moveables
    for c in state[f_pos]:
        if c != 'F':
            state_copy = deepcopy(state)

            if f_pos == 0: move_right(state_copy, c)
            else: move_left(state_copy, c)

            next_states.append(state_copy)
    
    # move the farmer only (no moveable)
    state_copy = deepcopy(state)
    if f_pos == 0: move_right(state_copy)
    else: move_left(state_copy)
    next_states.append(state_copy)

    return next_states

def sort_string(s: str) -> str:
    return ''.join(sorted(s))

def move(state: List, source: int, destination: int, moveable: str = None) -> None:
    state[source] = state[source].replace('F', '')
    if moveable: state[source] = state[source].replace(moveable, '')

    state[destination] = sort_string(state[destination] + 'F')
    if moveable: state[destination] = sort_string(state[destination] + moveable)

def move_right(state: List, moveable: str = None) -> None:
    move(state, 0, 1, moveable)

def move_left(state: List, moveable: str = None) -> None:
    move(state, 1, 0, moveable)

def find_solution(state: List, visited_states: List):
    if solution_found(state):
        solutions.append(visited_states)
        return

    successors = get_successors(state, visited_states)

    if len(successors) == 0:
        return
    
    for state in successors:
        visited_states_copy = deepcopy(visited_states)
        visited_states_copy.append(state)
        find_solution(state, visited_states_copy)

if __name__ == '__main__':
    state = STARTING_STATE
    visited_states = [state]

    find_solution(state, visited_states)

    for solution in solutions:
        print(solution)
    