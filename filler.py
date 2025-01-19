
from copy import deepcopy
import matplotlib.pyplot as plt
import random


ROWS, COLS = 7, 8
COLORS_ORIGINAL = {1: 'red', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'purple', 6: 'black'}
COLORS = {1: 'red', 2: 'yellow', 3: '#a4de02', 4: '#6badce', 5: 'purple', 6: 'black'}


class Filler:

    def __init__(self):
        self.original_grid = self.generate_grid()
        self.grid = deepcopy(self.original_grid)
        self.p1_color = self.grid[-1][0]
        self.p2_color = self.grid[0][-1]
        self.squares = {1: {(6,0)}, 2: {(0,7)}}
        self.turn = 1  # integer: 1 for P1, 2 for P2

        self.plot_grid()

    
    def generate_grid(self) -> list:

        # determine if we can change grid[row][col] to color
        def is_valid(row, col, color):

            if row > 0 and grid[row-1][col] == color:  # on top of current cell
                return False
            if col > 0 and grid[row][col-1] == color:  # to the left of current cell
                return False

            if (row, col) == (1, 7) and grid[0][6] == color:  # check 2 neighbors of top-right
                return False
            if (row, col) == (6, 1) and grid[5][0] == color:  # check 2 neighbors of bottom-left
                return False
            if (row, col) == (6, 1) and grid[5][0] == grid[0][6] and grid[1][7] == color:  # check 2 options at start are different
                return False
            if (row, col) == (6, 0) and grid[0][7] == color:  # ensure difference in P1/P2 start colors
                return False
            return True
        
        grid = [[0]*COLS for _ in range(ROWS)]
        for row in range(ROWS):
            for col in range(COLS):
                color_keys = list(COLORS.keys())
                random.shuffle(color_keys)  # shuffle colors for randomness
                for color in color_keys:
                    if is_valid(row, col, color):
                        grid[row][col] = color
                        break
        return grid


    def plot_grid(self):
        color_grid = [[COLORS[key] for key in row] for row in self.grid]

        fig, ax = plt.subplots()

        for i in range(ROWS):
            for j in range(COLS):
                rect = plt.Rectangle((j, ROWS - i - 1), 1, 1, color=color_grid[i][j])
                ax.add_patch(rect)

        ax.set_xlim(0, COLS)
        ax.set_ylim(0, ROWS)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])

        plt.show()

    
    def reset_board(self):
        self.grid = deepcopy(self.original_grid)
        self.p1_color = self.grid[-1][0]
        self.p2_color = self.grid[0][-1]
        self.squares[1] = {(6,0)}
        self.squares[2] = {(0,7)}
        self.turn = 1
        self.plot_grid()

    
    def print_score(self):
        print(f'Player 1: {len(self.squares[1])}')
        print(f'Player 2: {len(self.squares[2])}')

