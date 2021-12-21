"""(2021) Day 4: Giant Squid"""

# noinspection PyPep8Naming
from collections import defaultdict as DefaultDict

import numpy as np

from utils import read


class BingoBoard:
    board: dict
    marked: np.ndarray
    winning: bool

    def __init__(self, board):
        self.board = DefaultDict(list)

        if not all(len(board) == len(row) for row in board):
            raise ValueError(f"board is not a square matrix")
        for loc, num in np.ndenumerate(board):
            self.board[num].append(loc)

        self.marked = np.full((len(board), len(board)), False)
        self.winning = False

    def _check_winning(self, row, col):
        return all(self.marked[row]) or all(self.marked[:, col])

    def mark(self, target):
        """Mark the bingo square, and return if a bingo was formed from that mark."""
        made_bingo = False
        for loc in self.board[target]:
            self.marked[loc] = True
            if self._check_winning(*loc):
                self.winning, made_bingo = True, True
        return made_bingo


def win_bingo(nums, boards):
    """Find the bingo board that wins first and the number that causes the bingo.

    Break ties using the order of ``boards``.
    """
    for num in nums:
        for board in boards:
            if board.mark(num):
                return board, num
    return None, None


def lose_bingo(nums, boards):
    """Find the bingo board that loses last and the number that causes the bingo.

    Break ties using the order of ``boards``, choosing the last board in ``boards``.
    """
    winning_order = []
    for num in nums:
        for board in boards:
            if board.mark(num) and board not in winning_order:
                winning_order.append(board)
            if len(winning_order) == len(boards):
                return winning_order[-1], num
    return None, None  # not every board won


def squid_score(board, last_mark):
    """Multiply the sum of unmarked numbers on board by the last mark."""
    unmarked_sum = 0
    for num, locs in board.board.items():
        for loc in locs:
            if not board.marked[loc]:
                unmarked_sum += num
    return unmarked_sum * last_mark


def parse_bingo(contents):
    sections = contents.split("\n\n")
    nums = [int(x) for x in sections[0].split(",")]

    boards = []
    for board_str in sections[1:]:
        board = [[int(s) for s in line.split()] for line in board_str.splitlines()]
        boards.append(BingoBoard(np.array(board)))

    return nums, boards


if __name__ == "__main__":
    with read.data_file(day=4) as f:
        bingo_nums, bingo_boards = parse_bingo(f.read())

    print(f"Part One: {squid_score(*win_bingo(bingo_nums, bingo_boards))}")
    print(f"Part Two: {squid_score(*lose_bingo(bingo_nums, bingo_boards))}")
