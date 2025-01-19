
from filler import Filler
import random


ROWS, COLS = 7, 8
COLORS_ORIGINAL = {1: 'red', 2: 'yellow', 3: 'green', 4: 'blue', 5: 'purple', 6: 'black'}
COLORS = {1: 'red', 2: 'yellow', 3: '#a4de02', 4: '#6badce', 5: 'purple', 6: 'black'}


class Filler_Computer_Greedy(Filler):

    def __init__(self):
        super().__init__()
    

    def update_grid(self, color: int) -> None:

        if color == self.p1_color:
            print(f'Error: You are already {COLORS_ORIGINAL[color]}')
            return
        if color == self.p2_color:
            print(f'Error: Computer is already {COLORS_ORIGINAL[color]}')
            return
        
        print(f'You chose {COLORS_ORIGINAL[color]}')
        
        def is_valid(row: int, col: int):
            return 0 <= row < ROWS and 0 <= col < COLS and self.grid[row][col] == color

        # add squares to player's turn
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        curr_squares = self.squares[1].copy()
        for curr_row, curr_col in curr_squares:
            self.grid[curr_row][curr_col] = color
            for r, c in dirs:
                new_r, new_c = curr_row + r, curr_col + c
                if is_valid(new_r, new_c):
                    self.squares[1].add((new_r, new_c))

        self.p1_color = self.grid[-1][0]
        self.plot_grid()
    

    def computer_turn_greedy(self) -> None:
        # simulate greedy turn by the computer

        def is_valid(row: int, col: int):
            return 0 <= row < ROWS and 0 <= col < COLS and (row, col) not in self.squares[1]

        neighbors = {i: 0 for i in range(1, 7)}
        dirs = [(1,0), (-1,0), (0,1), (0,-1)]
        for curr_row, curr_col in self.squares[2]:
            for r, c in dirs:
                new_r, new_c = curr_row + r, curr_col + c
                if is_valid(new_r, new_c):
                    neighbors[self.grid[new_r][new_c]] += 1

        valid_numbers = {key: value for key, value in neighbors.items() if key not in (self.p1_color, self.p2_color)}
        max_frequency = max(valid_numbers.values())
        candidates = [key for key, value in valid_numbers.items() if value == max_frequency]
        random_color = random.choice(candidates)  # randomly choose 1 of the candidates
        print(f'Computer chose {COLORS_ORIGINAL[random_color]}')

        curr_squares = self.squares[2].copy()
        for curr_row, curr_col in curr_squares:
            self.grid[curr_row][curr_col] = random_color
            for r, c in dirs:
                new_r, new_c = curr_row + r, curr_col + c
                if is_valid(new_r, new_c) and self.grid[new_r][new_c] == random_color:
                    self.squares[2].add((new_r, new_c))
        
        self.p2_color = self.grid[0][-1]
        self.plot_grid()


    def play_game(self):

        self.plot_grid()

        def possible_turns():
            return list(set(range(1,7)) - {self.p1_color, self.p2_color})

        def get_user_input():
            while True:
                try:
                    print(f'VALID TURNS for Player 1: {possible_turns()}')
                    user_input = input(f"Player 1's turn (-1 to exit):: ")
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
                print(f'You win! You reached {len(self.squares[1])} > 28 already! Ending game...')
                return True
            elif len(self.squares[2]) > 28:
                print(f'Greedy computer wins! Computer reached {len(self.squares[2])} > 28 already! Ending game...')
                return True
            elif len(self.squares[1]) + len(self.squares[2]) == ROWS * COLS:
                if len(self.squares[1]) > 28:
                    print('You win!')
                elif len(self.squares[2]) > 28:
                    print('Greedy computer wins!')
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
            self.update_grid(color=int(user_input))
            self.print_score()
            if termination_condition():
                break

            # play the computer's turn
            self.computer_turn_greedy()
            self.print_score()
            if termination_condition():
                break


if __name__ == '__main__':

    filler_obj = Filler_Computer_Greedy()
    filler_obj.plot_grid()
