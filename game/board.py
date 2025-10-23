# game/board.py
import random
from typing import List, Tuple

MINE = -1

class Minesweeper:
    def __init__(self, rows: int = 8, cols: int = 8, mines: int = 10, seed: int | None = None):
        if mines >= rows * cols:
            raise ValueError("mines must be fewer than total cells")
        if seed is not None:
            random.seed(seed)

        self.rows = rows
        self.cols = cols
        self.mines = mines

        self.board: List[List[int]] = [[0 for _ in range(cols)] for _ in range(rows)]
        self.visible: List[List[bool]] = [[False for _ in range(cols)] for _ in range(rows)]
        self.flags: List[List[bool]] = [[False for _ in range(cols)] for _ in range(rows)]

        self._place_mines()
        self._calc_numbers()

    def _place_mines(self) -> None:
        positions = random.sample(range(self.rows * self.cols), self.mines)
        for pos in positions:
            r, c = divmod(pos, self.cols)
            self.board[r][c] = MINE

    def _calc_numbers(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] == MINE:
                    continue
                count = 0
                for nr, nc in self.neighbors(r, c):
                    if self.board[nr][nc] == MINE:
                        count += 1
                self.board[r][c] = count

    def in_bounds(self, r: int, c: int) -> bool:
        return 0 <= r < self.rows and 0 <= c < self.cols

    def neighbors(self, r: int, c: int):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if self.in_bounds(nr, nc):
                    yield nr, nc

    def toggle_flag(self, r: int, c: int) -> None:
        if not self.visible[r][c]:
            self.flags[r][c] = not self.flags[r][c]

    def reveal(self, r: int, c: int) -> bool:
        """
        Returns False if you hit a mine. True otherwise.
        Expands zero tiles like the real game.
        """
        if not self.in_bounds(r, c) or self.flags[r][c]:
            return True  # ignore invalid or flagged click
        if self.visible[r][c]:
            return True  # already open

        if self.board[r][c] == MINE:
            self.visible[r][c] = True
            return False

        # flood fill for zeros
        stack = [(r, c)]
        while stack:
            x, y = stack.pop()
            if self.visible[x][y]:
                continue
            self.visible[x][y] = True
            if self.board[x][y] == 0:
                for nx, ny in self.neighbors(x, y):
                    if not self.visible[nx][ny] and not self.flags[nx][ny]:
                        stack.append((nx, ny))
        return True

    def is_won(self) -> bool:
        """Win when every non-mine cell is visible."""
        for r in range(self.rows):
            for c in range(self.cols):
                if self.board[r][c] != MINE and not self.visible[r][c]:
                    return False
        return True

    def print_board(self, reveal_all: bool = False) -> None:
        """* for mine, number for counts, F for flags, # for hidden."""
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                if reveal_all:
                    row.append("*" if self.board[r][c] == MINE else str(self.board[r][c]))
                else:
                    if self.flags[r][c] and not self.visible[r][c]:
                        row.append("F")
                    elif self.visible[r][c]:
                        row.append("*" if self.board[r][c] == MINE else str(self.board[r][c]))
                    else:
                        row.append("#")
            print(" ".join(row))
