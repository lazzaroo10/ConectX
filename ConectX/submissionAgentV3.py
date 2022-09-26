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

def checkdiagonal(grid,player):
    priority_moves = []
    priority_moves2 = []
    for i in range(grid.shape[1]):
        #print(grid[:,i])
        #print(grid[grid.shape[1]-4:grid.shape[1],i])
        for x in range(grid.shape[0]-3,grid.shape[0]):
            if x == 5:
                altura = 0
            elif x == 4:
                altura = 1
            else:
                altura  = 2
            diagonal_d = []
            diagonal_i = []

            if i < 3:
                diagonal_d.append(grid[x,i])
                diagonal_d.append(grid[x-1,i+1])
                diagonal_d.append(grid[x-2,i+2])
                diagonal_d.append(grid[x-3,i+3])
            elif i>3:
                diagonal_i.append(grid[x,i])
                diagonal_i.append(grid[x-1,i-1])
                diagonal_i.append(grid[x-2,i-2])
                diagonal_i.append(grid[x-3,i-3])
            elif i == 3:
                diagonal_d.append(grid[x,i])
                diagonal_d.append(grid[x-1,i+1])
                diagonal_d.append(grid[x-2,i+2])
                diagonal_d.append(grid[x-3,i+3])

                diagonal_i.append(grid[x,i])
                diagonal_i.append(grid[x-1,i-1])
                diagonal_i.append(grid[x-2,i-2])
                diagonal_i.append(grid[x-3,i-3]) 

            #print(diagonal_d)
            #print(diagonal_i)
            #altura_accion = grid.shape[1]-list(grid[:,i]).count(0) - 1

            if diagonal_d.count(1) == 3 and diagonal_d.count(0) == 1:
                #altura del 0 a completar
                altura = diagonal_d.index(0)+altura  
                x_duda = diagonal_d.index(0)+i
                altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                print('diagonal derecha 1',diagonal_d.index(0)+i)
                print('altura',altura)
                print('altura_accion',altura_accion)
                if altura  == altura_accion:
                    #Movimiento prioritario(columna)
                    priority_moves.append(diagonal_d.index(0)+i)

            if diagonal_d.count(2) == 3 and diagonal_d.count(0) == 1:
                #altura del 0 a completar
                altura = diagonal_d.index(0)+altura
                x_duda = diagonal_d.index(0)+i
                altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                print('diagonal derecha 2',diagonal_d.index(0)+i)
                if altura  == altura_accion:
                    #Movimiento prioritario(columna)
                    priority_moves2.append(diagonal_d.index(0)+i)

            if diagonal_i.count(1) == 3 and diagonal_i.count(0) == 1:
                #altura del 0 a completar
                altura = diagonal_i.index(0)+altura
                x_duda = i - diagonal_i.index(0)
                altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                print('diagonal izquierda 1',i - diagonal_i.index(0))
                print('altura',altura)
                print('altura_accion',altura_accion)
                if altura  == altura_accion:

                    #Movimiento prioritario(columna)
                    priority_moves.append(i -diagonal_i.index(0))

            if diagonal_i.count(2) == 3 and diagonal_i.count(0) == 1:
                #altura del 0 a completar
                altura = diagonal_i.index(0)+altura
                x_duda = i - diagonal_i.index(0)
                print(x_duda)
                altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                print('diagonal izquierda 2',i-diagonal_i.index(0))
                print('altura',altura)
                print('altura accion',altura_accion)
                if altura  == altura_accion:
                    #Movimiento prioritario(columna)
                    priority_moves2.append(i-diagonal_i.index(0))
    if player == 2:
        priority_moves,priority_moves2 = priority_moves2,priority_moves

    return priority_moves,priority_moves2

# Create game environment
env = make("connectx", debug=True, configuration={ "actTimeout": 9999999999 })


#agente

import random
import numpy as np

def agentV2(observation, configuration):
    # Get the number of columns in the board
    number_of_columns = configuration.columns
    
    grid = np.asarray(observation.board).reshape(configuration.rows, configuration.columns)
    
    # Movimientos prioritariooos
    priority1 ,priority2 = checkcolum(grid,observation.mark)
    priority1_raw,priority2_raw= checkraw(grid,observation.mark)
    priority1_diagonal,priority2_diagonal = checkdiagonal(grid,observation.mark)
    print(priority1)
    valid_moves = []
     
    # TODO: Choose a random move (column) from the list
    if bool(priority1):
        chosen_move = random.choice(priority1)
    elif bool(priority1_raw):
        chosen_move = random.choice(priority1_raw) 
    elif bool(priority1_diagonal):
        chosen_move = random.choice(priority1_diagonal)
    elif bool(priority2):
        chosen_move = random.choice(priority2)
    elif bool(priority2_raw):
        chosen_move = random.choice(priority2_raw)
    elif bool(priority2_diagonal):
        chosen_move = random.choice(priority2_diagonal)
    
    
    
        
    else:
        primera_fila = grid[0]
        for i in range(len(primera_fila)):
            if primera_fila[i]  == 0:
                valid_moves.append(i)
        chosen_move = random.choice(valid_moves)
    
    #print(grid)
    #print(chosen_move)
    # ...and return it
    return int(chosen_move) 