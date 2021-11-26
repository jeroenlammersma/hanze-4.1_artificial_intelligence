import random
import string
import sys

from copy import deepcopy
from typing import List, Set
from pprint import pprint

# trie code based on:
# https://stackoverflow.com/questions/11015320/how-to-create-a-trie-in-python

_end = '_end_'

def make_trie(words: List[str]):
    root = dict()

    for word in words:
        current_dict = root

        for letter in word:
            current_dict = current_dict.setdefault(letter, {})

        current_dict[_end] = _end
        
    return root

def in_trie(trie, word: str, as_word: bool) -> bool:
    current_dict = trie

    for letter in word:
        if letter not in current_dict:
            return False
            
        current_dict = current_dict[letter]

    if as_word:
        return _end in current_dict

    return True

def read_file_to_list(path) -> List[str]:
    words = []

    with open(path, 'r', encoding="latin-1") as file:
        while (line := file.readline().rstrip()):
            words.append(line)

    return words

def create_board(size: int) -> List[List[str]]:
    return [ [random.choice(string.ascii_lowercase) for _ in range(size)] for _ in range(size) ]

def print_board(board: List[List[str]]) -> None:
    pprint(board)

def print_result(words: Set) -> None:
    for word in words:
        print(word)

    print(f"\n{len(words)} words found")

def dfs(
    board: List[List[str]],
    trie,
    words: Set[str],
    x: int,
    y: int,
    current_word: str = ''
) -> None:
    current_word = current_word + board[y][x]                       # append letter of current position to current word

    if not in_trie(trie, current_word, as_word=False): return       # stop searching if current word not in trie

    if in_trie(trie, current_word, as_word=True):
        words.add(current_word)                                     # if current word is valid word, add to words

    board[y][x] = ''                                                # mark current position as visited

    board_copy = deepcopy(board)
    current_word_copy = deepcopy(current_word)

    board_size = len(board)

    neighbours = [                                                  # calculate neighbour coordinates 
        ((x + 1) % board_size, y), 
        ((x - 1) % board_size, y),
        (x, (y + 1) % board_size),
        (x, (y - 1) % board_size)
    ]

    for x, y in neighbours:                                         # iterate over neighbours
        if board[y][x] != '':                                       # if neighbour not visited:
            dfs(board_copy, trie, words, x, y, current_word_copy)   # conduct dfs on neighbour

def find_words(board: List[List[str]], trie) -> Set[str]:
    words = set()                                                   # contains found words
    board_size = len(board)

    for x in range(board_size):                                     # iterate over all cells of board
        for y in range(board_size):
            dfs(board, trie, words, x, y)                           # conduct dfs on cell

    return words

def print_call_instruction() -> None:
    print("boggle takes two arguments: language and size")
    print("example: boggle nl 5")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print_call_instruction()
        exit(1)

    language = sys.argv[1].upper()
    if language not in ["NL", "EN"]:
        print_call_instruction()
        exit(1)

    size = sys.argv[2]
    if not size.isdigit():
        print_call_instruction()
        exit(1)

    list_of_words = read_file_to_list(f"words_{language}.txt")
    trie = make_trie(list_of_words)
    board = create_board(int(size))

    print_board(board)
    print()

    # board = [
    #     ['b', 'a', 's', 'i', 's'],
    #     ['a', 'a', 'n', 'b', 'x'],
    #     ['t', 'r', 'e', 'o', 'd'],
    #     ['h', 'e', 't', 'm', 'i'],
    #     ['p', 'l', 'j', 'l', 'w']
    # ]

    words = find_words(board, trie)
    print_result(words)