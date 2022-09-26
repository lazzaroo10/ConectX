from kaggle_environments import make
from IPython.display import clear_output
import random
import numpy as np

#Funciones auxiliares

def checkcolum(grid,player): 
    valid_moves =[]
    for i in range(len(grid[0])):
            if grid[0][i]  == 0:
                valid_moves.append(i)
    priority_moves = []
    priority_moves2 = []
    me = 0 
    enemy = 0
    for x in valid_moves: 

        #print(me)
        #print(grid[:,x])
        for i in reversed(range(grid.shape[0])):
            #print(grid[i,x])
            if grid[i,x] == 1:
                me += 1
                enemy = 0
            elif grid[i,x] == 2:
                enemy += 1
                me = 0

            #pint('me:', me)
            #print('enemy: ', enemy)
        #pnt(me)
        if me == 3:
            priority_moves.append(x)
            #print('Pririty: ',priority_moves)
        elif enemy == 3:
            priority_moves2.append(x) 
            print(priority_moves2)
        me = 0 
        enemy = 0
        
    if player == 2:
        priority_moves,priority_moves2 = priority_moves2,priority_moves

    return priority_moves,priority_moves2
    
def checkraw(grid,player):

    priority_moves = []
    priority_moves2 = []

    for i in range(grid.shape[0]):
        #print(grid[i,:])
        raw = np.array(grid[i,:])
        for x in range(4):
            raw_slice = list(raw[0 + x:4 + x])
            #print(raw_slice)
            if raw_slice.count(1) == 3 and raw_slice.count(0) == 1:
                m=9
                print(raw_slice.count(1))
                if i == list(grid[:,raw_slice.index(0)+x]).count(0) - 1:
                    priority_moves.append(raw_slice.index(0)+x)
            elif raw_slice.count(2) == 3 and raw_slice.count(0) == 1:
                #print(raw_slice.count(1))
                if i == list(grid[:,raw_slice.index(0)+x]).count(0) - 1:
                    priority_moves2.append(raw_slice.index(0)+x)
    if player == 2:
        priority_moves,priority_moves2 = priority_moves2,priority_moves

    return priority_moves,priority_moves2

# Create game environment
env = make("connectx", debug=True, configuration={ "actTimeout": 9999999999 })


#agente

def agentV2(observation, configuration):
    # Get the number of columns in the board
    number_of_columns = configuration.columns
    
    grid = np.asarray(observation.board).reshape(configuration.rows, configuration.columns)
    
    # Movimientos prioritariooos
    priority1 , priority2= checkcolum(grid,observation.mark)
    priority1_raw,priority2_raw= checkraw(grid,observation.mark)
    print(priority1)
    valid_moves = []
     
    #: Choose a random move (column) from the list
    if bool(priority1):
        chosen_move = random.choice(priority1)
    elif bool(priority1_raw):
        chosen_move = random.choice(priority1_raw) 
    elif bool(priority2):
        chosen_move = random.choice(priority2)
    elif bool(priority2_raw):
        chosen_move = random.choice(priority2_raw)
    
    else:
        primera_fila = grid[0]
        for i in range(len(primera_fila)):
            if primera_fila[i]  == 0:
                valid_moves.append(i)
        chosen_move = random.choice(valid_moves)

    # ...and return it
    return int(chosen_move) 