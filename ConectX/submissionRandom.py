from kaggle_environments import make
from IPython.display import clear_output
import random
import numpy as np

# Create game environment
env = make("connectx", debug=True, configuration={ "actTimeout": 9999999999 })


def agent_random2(observation, configuration):
    # Get the number of columns in the board
    number_of_columns = configuration.columns
    
    grid = np.asarray(observation.board).reshape(configuration.rows, configuration.columns)
    
    # TODO: Create a list of all the valid moves (columns) using `range()`
    
    primera_fila = grid[0]
    
    valid_moves = []
    
    for i in range(len(primera_fila)):
        if primera_fila[i]  == 0:
            valid_moves.append(i) 
            
    # TODO: Choose a random move (column) from the list
    chosen_move = random.choice(valid_moves)
    
    # ...and return it
    return chosen_move 
