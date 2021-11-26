import random
random.seed(3)

from collections import namedtuple
from typing import List, Tuple, Union

"""

Othello is a turn-based two-player strategy board game.

-----------------------------------------------------------------------------
Board representation

We represent the board as a flat-list of 100 elements, which includes each square on
the board as well as the outside edge. Each consecutive sublist of ten
elements represents a single row, and each list element stores a piece. 
An initial board contains four pieces in the center:

    ? ? ? ? ? ? ? ? ? ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . o @ . . . ?
    ? . . . @ o . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? . . . . . . . . ?
    ? ? ? ? ? ? ? ? ? ?

The outside edge is marked ?, empty squares are ., black is @, and white is o.

This representation has two useful properties:

1. Square (m,n) can be accessed as `board[mn]`, and m,n means m*10 + n. This avoids conversion
   between square locations and list indexes.
2. Operations involving bounds checking are slightly simpler.
"""

# The black and white pieces represent the two players.

EMPTY, BLACK, WHITE, OUTER = '.', '@', 'o', '?'
PIECES = (EMPTY, BLACK, WHITE, OUTER)
PLAYERS = {BLACK: 'Black', WHITE: 'White'}

# To refer to neighbor squares we can add a direction to a square.
UP, DOWN, LEFT, RIGHT = -10, 10, -1, 1
UP_RIGHT, DOWN_RIGHT, DOWN_LEFT, UP_LEFT = -9, 11, 9, -11
# in total 8 directions.
DIRECTIONS = (UP, UP_RIGHT, RIGHT, DOWN_RIGHT, DOWN, DOWN_LEFT, LEFT, UP_LEFT)

Move = namedtuple('Move', 'move score')

def squares() -> List[int]:
    # list all the valid squares on the board.
    # returns a list of valid integers [11, 12, ...]; e.g. 19,20,21 are invalid
    # 11 means first row, first col, because the board size is 10x10
    return [i for i in range(11, 89) if 1 <= (i % 10) <= 8]

def initial_board() -> List[str]:
    # create a new board with the initial black and white positions filled
    # returns a list ['?', '?', '?', ..., '?', '?', '?', '.', '.', '.', ...]
    board = [OUTER] * 100
    for i in squares():
        board[i] = EMPTY
    # the middle four squares should hold the initial piece positions.
    board[44], board[45] = WHITE, BLACK
    board[54], board[55] = BLACK, WHITE
    return board

def print_board(board: List[str]) -> str:
    # get a string representation of the board
    # heading '  1 2 3 4 5 6 7 8\n'
    rep = ''
    rep += '  %s\n' % ' '.join(map(str, range(1, 9)))
    # begin,end = 11,19 21,29 31,39 ..
    for row in range(1, 9):
        begin, end = 10*row + 1, 10*row + 9
        rep += '%d %s\n' % (row, ' '.join(board[begin:end]))
    return rep

# -----------------------------------------------------------------------------
# Playing the game

# We need functions to get moves from players, check to make sure that the moves
# are legal, apply the moves to the board, and detect when the game is over.

# Checking moves. A move must be both valid and legal: it must refer to a real square,
# and it must form a bracket with another piece of the same color with pieces of the
# opposite color in between.

def is_valid(move: int) -> bool:
    # is move a square on the board?
    # move must be an int, and must refer to a real square
    return move in squares()

def opponent(player: str) -> str:
    # get player's opponent piece
    return BLACK if player is WHITE else WHITE

def find_bracket(square: int, player: str, board: List[str], direction: int) -> Union[int, None]:
    # find and return the square that forms a bracket with square for player in the given
    # direction; returns None if no such square exists
    bracket = square + direction
    if board[bracket] == player:
        return None
    opp = opponent(player)
    while board[bracket] == opp:
        bracket += direction
    # if last square board[bracket] not in (EMPTY, OUTER, opp) then it is player
    return None if board[bracket] in (OUTER, EMPTY) else bracket

def is_legal(move: int, player: str, board: List[str]) -> bool:
    # is this a legal move for the player?
    # move must be an empty square and there has to be a bracket in some direction
    # note: any(iterable) will return True if any element of the iterable is true
    hasbracket = lambda direction: find_bracket(move, player, board, direction)
    return board[move] == EMPTY and any(hasbracket(x) for x in DIRECTIONS)

def make_move(move: int, player: str, board: List[str]) -> List[str]:
    # when the player makes a valid move, we need to update the board and flip all the
    # bracketed pieces.
    board[move] = player
    # look for a bracket in any direction
    for d in DIRECTIONS:
        make_flips(move, player, board, d)
    return board

def make_flips(move: int, player: str, board: List[str], direction: int) -> None:
    # flip pieces in the given direction as a result of the move by player
    bracket = find_bracket(move, player, board, direction)
    if not bracket:
        return
    # found a bracket in this direction
    square = move + direction
    while square != bracket:
        board[square] = player
        square += direction

# Monitoring players

# define an exception
class IllegalMoveError(Exception):
    def __init__(self, player: str, move: int, board: List[str]):
        self.player = player
        self.move = move
        self.board = board
    
    def __str__(self):
        return '%s cannot move to square %d' % (PLAYERS[self.player], self.move)

def legal_moves(player: str, board: List[str]) -> List[int]:
    # get a list of all legal moves for player
    # legal means: move must be an empty square and there has to be is an occupied line in some direction
    return [sq for sq in squares() if is_legal(sq, player, board)]

def any_legal_move(player: str, board: List[str]) -> bool:
    # can player make any moves?
    return any(is_legal(sq, player, board) for sq in squares())

# Putting it all together. Each round consists of:
# - Get a move from the current player.
# - Apply it to the board.
# - Switch players. If the game is over, get the final score.

def play(black_strategy, white_strategy) -> Tuple[List[str], int]:
    # play a game of Othello and return the final board and score
    board = initial_board()
    print(print_board(board))

    # starting player
    player = BLACK

    while player != None:
        strategy = black_strategy if player == BLACK else white_strategy
        move = get_move(strategy, player, board)
        make_move(move, player, board)
        player = next_player(board, player)
        print(print_board(board))

    return board, score(BLACK, board)


def next_player(board: List[str], prev_player: str) -> Union[str, None]:
    # which player should move next?  Returns None if no legal moves exist
    other_player = opponent(prev_player)
    if any_legal_move(other_player, board):
        return other_player    
    elif any_legal_move(prev_player, board):
        return prev_player
    return None
    
    
def get_move(strategy, player: str, board: List[str]) -> int:
    # call strategy(player, board) to get a move
    board_copy = board[:]
    move = strategy(player, board_copy)

    if not is_valid(move) or not is_legal(move, player, board_copy):
        raise IllegalMoveError(player, move, board_copy)
    
    return move

def score(player: str, board: List[str]) -> int:
    # compute player's score (number of player's pieces minus opponent's)
    score = other_score = 0
    other_player = opponent(player)

    for square in squares():
        piece = board[square]
        if piece == player:
            score += 1
        elif piece == other_player:
            other_score += 1
    
    return score - other_score

# Play strategies

def random_strategy(player: str, board: List[str]) -> int:
    return random.choice(legal_moves(player, board))

def heuristic_othello(player: str, board: List[str]) -> int:
    board_weights = [
        0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
        0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
        0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
        0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
        0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
        0,   5,  -5,   3,   3,   3,   3,  -5,   5,   0,
        0,  20,  -5,  15,   3,   3,  15,  -5,  20,   0,
        0, -20, -40,  -5,  -5,  -5,  -5, -40, -20,   0,
        0, 120, -20,  20,   5,   5,  20, -20, 120,   0,
        0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
    ]

    score = 0
    other_player = opponent(player)

    for square in squares():
        if board[square] == player:
            score += board_weights[square]
        elif board[square] == other_player:
            score -= board_weights[square]
        
    return score

def maximizing(player: str, turn: str):
    return player == turn

def minimax(player: str, turn: str, board: List[str], depth: int, heuristic) -> Move:
    # max depth reached, return heuristic value
    if depth == 0:
        return Move(None, heuristic(player, board))
    
    # if player cannot make moves, switch turn
    if not any_legal_move(turn, board):
        turn = opponent(turn)

        # if still no turns, game is over and return heuristic value
        if not any_legal_move(turn, board):
            return Move(None, heuristic(player, board))
    
    # initialize inital best move, according to maximizing or not
    init_score = -float('INF') if maximizing(player, turn) else float('INF')
    best = Move(-1, init_score)

    # get all availabe moves
    moves = legal_moves(turn, board)

    for move in moves:
        # get score 
        result = minimax(player, opponent(turn), board, depth - 1, heuristic)

        # get new best move and ...
        # when maximizing, result me be greater than best
        if maximizing(player, turn) and result.score > best.score:
            best = Move(move, result.score)
        # when not maximizing, result must be less than best
        elif result.score < best.score:
            best = Move(move, result.score)

    return best

def minimax_ab(
     player: str,
     turn: str,
     board: List[str],
     depth: int,
     alpha: float, 
     beta: float, 
     heuristic
) -> Move:
    # max depth reached, return heuristic value
    if depth == 0:
        return Move(None, heuristic(player, board))
    
    # if player cannot make moves, switch turn
    if not any_legal_move(turn, board):
        turn = opponent(turn)

        # if still no turns, game is over and return heuristic value
        if not any_legal_move(turn, board):
            return Move(None, heuristic(player, board))
    
    # initialize inital best move, according to maximizing or not
    init_score = -float('INF') if maximizing(player, turn) else float("INF")
    best = Move(-1, init_score)

    # get all availabe moves
    moves = legal_moves(turn, board)

    for move in moves:
        # get move
        result = minimax_ab(player, opponent(turn), board, depth - 1, alpha, beta, heuristic)

        # get new best move and ...
        # when maximizing, result me be greater than best
        if maximizing(player, turn) and result.score > best.score:
            best = Move(move, result.score)
        # when not maximizing, result must be less than best
        elif result.score < best.score:
            best = Move(move, result.score)

        # apply alpha beta pruning
        if maximizing(player, turn) and result.score > alpha:
            alpha = result.score
        elif result.score < beta:
            beta = result.score
        if beta <= alpha:
            break

    return best
        
def minimax_strategy(player: str, board: List[str]) -> int:
    depth = 5
    heuristic = heuristic_othello

    return minimax(player, player, board, depth, heuristic).move

def minimax_ab_strategy(player: str, board: List[str]) -> int:
    depth = 11
    heuristic = heuristic_othello

    return minimax_ab(player, player, board, depth, -float('INF'), float('INF'), heuristic).move

black_strategy = minimax_ab_strategy
white_strategy = random_strategy

board, final_score = play(black_strategy, white_strategy)
print("score black:", final_score)
print("score white:", -final_score)