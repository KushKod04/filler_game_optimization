
from filler import Filler


ROWS, COLS = 7, 8
COLORS_ORIGINAL = {1: 'red', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'purple', 6: 'black'}
COLORS = {1: 'red', 2: 'yellow', 3: '#a4de02', 4: '#6badce', 5: 'purple', 6: 'black'}


class Filler_2_Player(Filler):

    def __init__(self):
        super().__init__()
    

    def update_grid(self, color: int, turn: int) -> None:

        if color == self.p1_color:
            print(f'Error: Player 1 is already {COLORS_ORIGINAL[color]}')
            return
        if color == self.p2_color:
            print(f'Error: Player 2 is already {COLORS_ORIGINAL[color]}')
            return
        
        print(f'Player {turn} chose {COLORS_ORIGINAL[color]}')
        
        def is_valid(row: int, col: int):
            return 0 <= row < ROWS and 0 <= col < COLS and self.grid[row][col] == color

        # add squares to player's turn
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        curr_squares = self.squares[turn].copy()
        for curr_row, curr_col in curr_squares:
            self.grid[curr_row][curr_col] = color
            for r, c in dirs:
                new_r, new_c = curr_row + r, curr_col + c
                if is_valid(new_r, new_c):
                    self.squares[turn].add((new_r, new_c))

        self.plot_grid()
    
        if turn == 1:
            self.p1_color = self.grid[-1][0]
        elif turn == 2:
            self.p2_color = self.grid[0][-1]


    def play_game(self):

        self.plot_grid()

        def possible_turns():
            return list(set(range(1,7)) - {self.p1_color, self.p2_color})

        def get_user_input():
            while True:
                try:
                    print(f'VALID TURNS for Player {self.turn}: {possible_turns()}')
                    user_input = input(f"Player {self.turn}'s turn (-1 to exit):: ")
                    if user_input == '':
                        break
                    
                    user_input = int(user_input)
                    if user_input == self.p1_color:
                        print(f'Player 1 is already {user_input}!')
                    elif user_input == self.p2_color:
                        print(f'Player 2 is already {user_input}!')
                    else:
                        break
                except ValueError:
                    print("Invalid input. Please enter an integer or a valid color.")
            
            return user_input

        def termination_condition() -> bool:
            if len(self.squares[1]) > 28:
                print(f'Player 1 wins! P1 reached {len(self.squares[1])} > 28 already! Ending game...')
                return True
            elif len(self.squares[2]) > 28:
                print(f'Player 2 wins! P2 reached {len(self.squares[2])} > 28 already! Ending game...')
                return True
            elif len(self.squares[1]) + len(self.squares[2]) == ROWS * COLS:
                if len(self.squares[1]) > 28:
                    print('Player 1 wins!')
                elif len(self.squares[2]) > 28:
                    print('Player 2 wins!')
                else:
                    print('DRAW!')
                return True
            return False


        while True:
            print('Use the following color mappings :: ', COLORS_ORIGINAL)

            user_input = get_user_input()
            
            # check if user wants to exit the game
            if user_input == -1 or user_input == '':
                print('Ending the game!')
                break

            # clear_output(wait=True)
            if self.turn == 1:
                self.update_grid(color=int(user_input), turn=1)
                self.turn = 2
            else:
                self.update_grid(color=int(user_input), turn=2)
                self.turn = 1
            
            self.print_score()
            if termination_condition():
                break


if __name__ == '__main__':
    obj = Filler_2_Player()
    obj.play_game()
