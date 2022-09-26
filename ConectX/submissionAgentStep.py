from kaggle_environments import make , evaluate
from IPython.display import clear_output
import random
import numpy as np
import time


#Puntua dependiendo de cuantos haya juntos
def points_sistem(priority_me , priority_enemy , secundary_me ,secundary_enemy   ,num_col):
    points = [0] * num_col
    for i in priority_me:
        points[i] +=  100000
    for i in priority_enemy:
        points[i] -=  100
    for i in secundary_me:
        points[i] +=  1
    for i in secundary_enemy:
        points[i] -=1
    return points



def points_sistem_pos(priority_me , secundary_me ,num_col):
    points = [0] * num_col
    for i in priority_me:
        points[i] +=  100000

    for i in secundary_me:
        points[i] +=  1

    return points




#Simula nuevo grid despues de añadir una pieza
def drop_piece(grid, col, mark, config):
    next_grid = grid.copy()
    for row in range(config.rows-1, -1, -1):
        if next_grid[row][col] == 0:
            break
    next_grid[row][col] = mark
    return next_grid





def checkcolum(grid,player): 
    valid_moves =[]
    for i in range(len(grid[0])):
            if grid[0][i]  == 0:
                valid_moves.append(i)
    priority_moves = []
    priority_moves2 = []
    secundary_move = []
    secundary_move2 = []
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
            #print(priority_moves2)
        me = 0 
        enemy = 0
        
        
    #Para 2 seguidos
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
        if me == 2:
            secundary_move.append(x)
            #print('Pririty: ',priority_moves)
        elif enemy == 2:
            secundary_move2.append(x) 
            #print(priority_moves2)
        me = 0 
        enemy = 0
        
    if player == 2:
        priority_moves,priority_moves2 = priority_moves2,priority_moves
        secundary_move,secundary_move2 = secundary_move2,secundary_move

    return priority_moves,priority_moves2,secundary_move,secundary_move2




def checkraw(grid,player):

    priority_moves = []
    priority_moves2 = []
    secundary_move = []
    secundary_move2 = []

    for i in range(grid.shape[0]):
        #print(grid[i,:])
        raw = np.array(grid[i,:])
        for x in range(4):
            raw_slice = list(raw[0 + x:4 + x])
            #print(raw_slice)
            if raw_slice.count(1) == 3 and raw_slice.count(0) == 1:
                #print(raw_slice.count(1))
                if i == list(grid[:,raw_slice.index(0)+x]).count(0) - 1:
                    priority_moves.append(raw_slice.index(0)+x)
            if raw_slice.count(2) == 3 and raw_slice.count(0) == 1:
                #print(raw_slice.count(1))
                if i == list(grid[:,raw_slice.index(0)+x]).count(0) - 1:
                    priority_moves2.append(raw_slice.index(0)+x)
                    
            ##########################################################
            #Filas de 2
            if raw_slice.count(1) == 2 and raw_slice.count(0) == 2:
                #print(raw_slice.count(1))
                if i == list(grid[:,raw_slice.index(0)+x]).count(0) - 1:
                    secundary_move.append(raw_slice.index(0)+x)
                    
            if raw_slice.count(2) == 2 and raw_slice.count(0) == 2:
                #print(raw_slice.count(1))
                if i == list(grid[:,raw_slice.index(0)+x]).count(0) - 1:
                    secundary_move2.append(raw_slice.index(0)+x)            

            
    if player == 2:
        priority_moves,priority_moves2 = priority_moves2,priority_moves
        secundary_move,secundary_move2 = secundary_move2,secundary_move

    return priority_moves,priority_moves2,secundary_move,secundary_move2


def checkdiagonal(grid,player_ai):
    priority_moves = []
    priority_moves2 = []
    secundary_move = []
    secundary_move2 = []
    
    #Es 3 porque hay 7 columnas, sino sería otro número(mitad de 7)
    MID = 3
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
            
            if i < MID:
                diagonal_d.append(grid[x,i])
                diagonal_d.append(grid[x-1,i+1])
                diagonal_d.append(grid[x-2,i+2])
                diagonal_d.append(grid[x-3,i+3])
            elif i>MID:
                diagonal_i.append(grid[x,i])
                diagonal_i.append(grid[x-1,i-1])
                diagonal_i.append(grid[x-2,i-2])
                diagonal_i.append(grid[x-3,i-3])
            elif i == MID:
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
            
            #checkdiagonal_auxiliar_d(diagonal_d,player,num_check,moves,altura,i)
            #checkdiagonal_auxiliar_d(diagonal_d,1,3,priority_moves,altura,i)
            
            player = 1
            num_check = 3
            moves = priority_moves
            if diagonal_d.count(player) == num_check and diagonal_d.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_d) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i + empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                    #print('diagonal derecha 1',x_duda)
                    #print('altura',altura2)
                    #print('altura_accion',altura_accion)
                    if altura2  == altura_accion:
                        #Movimiento prioritario(columna)
                        moves.append(i + empty_x)
            
            
            #(Toda esta seccion debería funcionar con subsecciones fuera del agente funciona perfecto, pero dentro se lia, ni puta idea de porque)
            ##############################################################################################################
            #checkdiagonal_auxiliar_d(diagonal_d,2,3,priority_moves2,altura,i)
            player = 2
            num_check = 3
            moves = priority_moves2
            if diagonal_d.count(player) == num_check and diagonal_d.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_d) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i + empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                    #print('diagonal derecha 2',x_duda)
                    #print('altura',altura2)
                    #print('altura_accion',altura_accion)
                    if altura2  == altura_accion:
                        moves.append(i + empty_x)
            
            
            #checkdiagonal_auxiliar_i(diagonal_i,1,3,priority_moves,altura,i)
            player = 1
            num_check = 3
            moves = priority_moves
            
            if diagonal_i.count(player) == num_check and diagonal_i.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_i) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i - empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1

                    if altura2  == altura_accion:
                        #Movimiento prioritario(columna)
                        moves.append(i -empty_x)

            #checkdiagonal_auxiliar_i(diagonal_i,2,3,priority_moves2,altura,i)
            
            player = 2
            num_check = 3
            moves = priority_moves
            
            if diagonal_i.count(player) == num_check and diagonal_i.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_i) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i - empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1

                    if altura2  == altura_accion:
                        #Movimiento prioritario(columna)
                        moves.append(i -empty_x)
            ######################################################################
            #Diagonal of 2
            
            #checkdiagonal_auxiliar_d(diagonal_d,1,2,secundary_move,altura,i)
            
            player = 1
            num_check = 2
            moves = secundary_move
            
            if diagonal_d.count(player) == num_check and diagonal_d.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_d) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i + empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                    #print('diagonal derecha 2 _ sec',x_duda)
                    #print('altura',altura2)
                    #print('altura_accion',altura_accion)
                    if altura2  == altura_accion:
                        #Movimiento prioritario(columna)
                        moves.append(i + empty_x)

            #checkdiagonal_auxiliar_d(diagonal_d,2,2,secundary_move2,altura,i)
            
            player = 2
            num_check = 2
            moves = secundary_move2
            
            if diagonal_d.count(player) == num_check and diagonal_d.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_d) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i + empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1
                    #print('diagonal derecha 2 _ sec',x_duda)
                    #print('altura',altura2)
                    #print('altura_accion',altura_accion)
                    if altura2  == altura_accion:
                        #Movimiento prioritario(columna)
                        moves.append(i + empty_x)

            #checkdiagonal_auxiliar_i(diagonal_i,1,2,secundary_move,altura,i)
            
            player = 1
            num_check = 2
            #moves = secundary_move
            
            if diagonal_i.count(player) == num_check and diagonal_i.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_i) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i - empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1

                    if altura2  == altura_accion:
                        #Movimiento prioritario(columna)
                        secundary_move.append(i -empty_x)

            #checkdiagonal_auxiliar_i(diagonal_i,2,2,secundary_move2,altura,i)
            
            player = 2
            num_check = 2
            #moves = secundary_move2
            
            if diagonal_i.count(player) == num_check and diagonal_i.count(0) == 4-num_check:
                pos_0 = [i for i, e in enumerate(diagonal_i) if e == 0]
                for empty_x in pos_0:
                    #altura del 0 a completar
                    altura2 = empty_x+altura
                    x_duda = i - empty_x
                    altura_accion = grid.shape[1]-list(grid[:,x_duda]).count(0) - 1

                    if altura2  == altura_accion:
                        #Movimiento prioritario(columna)
                        secundary_move2.append(i -empty_x)

            
            ###########################################################################################################
            
            
    if player_ai == 2:
        priority_moves,priority_moves2 = priority_moves2,priority_moves
        secundary_move,secundary_move2 = secundary_move2,secundary_move

    return priority_moves,priority_moves2,secundary_move,secundary_move2



def indices(lst, item):
    return [i for i, x in enumerate(lst) if x == item]

# Create game environment
env = make("connectx", debug=True, configuration={ "actTimeout": 9999999999 })




def agent_onestep(observation, configuration):
    
    if observation.mark == 1:
        player_enemy = 2
    else:
        player_enemy = 1
    
    
    #Matriz del tablero
    grid = np.asarray(observation.board).reshape(6, 7)
    #print(grid)
    #Prioridades columnas y puntos
    priority_me_c, priority_enemy_c, secundary_me_c, secundary_enemy_c=  checkcolum(grid,observation.mark)
    points_column = points_sistem_pos(priority_me_c, secundary_me_c,configuration.columns)
    
    #Prioridades diagonales y puntos
    priority_me_d, priority_enemy_d, secundary_me_d, secundary_enemy_d= checkdiagonal(grid,observation.mark)
    points_diag = points_sistem_pos(priority_me_d, secundary_me_d ,configuration.columns)
    
    #Prioridades diagonales y puntos
    priority_me_r, priority_enemy_r, secundary_me_r, secundary_enemy_r= checkraw(grid,observation.mark)
    points_raw = points_sistem_pos(priority_me_r, secundary_me_r,configuration.columns)
    
    
    points = list(np.add(points_column, points_diag))
    points = list(np.add(points, points_raw))
    #print('points',points)
    
    puntos_final_list = []
    for i in range(configuration.columns):
        points_enemy = []
        next_grid  = drop_piece(grid, i , observation.mark , configuration)
        #print(i,next_grid)
        
        for x in range(configuration.columns):
            
            next_grid2  = drop_piece(next_grid, x , player_enemy , configuration)
            
            #Prioridades columnas y puntos
            priority_me_c, priority_enemy_c, secundary_me_c, secundary_enemy_c=  checkcolum(next_grid2,observation.mark)
            points_column = points_sistem(priority_me_c, priority_enemy_c, secundary_me_c, secundary_enemy_c ,configuration.columns)

            #Prioridades diagonales y puntos
            priority_me_d, priority_enemy_d, secundary_me_d, secundary_enemy_d= checkdiagonal(next_grid2,observation.mark)
            points_diag = points_sistem(priority_me_d, priority_enemy_d, secundary_me_d, secundary_enemy_d ,configuration.columns)

            #Prioridades diagonales y puntos
            priority_me_r, priority_enemy_r, secundary_me_r, secundary_enemy_r= checkraw(next_grid2,observation.mark)
            points_raw = points_sistem(priority_me_r, priority_enemy_r, secundary_me_r, secundary_enemy_r,configuration.columns)


            points_s = list(np.add(points_column, points_diag))
            points_s = list(np.add(points_s, points_raw))
            #print(i,points_s)
            neg_nos = [num for num in points_s if num < 0]
            points_enemy.append(sum(neg_nos))
        #print(i,'points_enemy: ' ,points_enemy)
        points_final = points_enemy
        #print(i,'puntos final:',points_final)
        puntos_final_list.append(min(points_final))
        
    #points = list(np.add(points, points_enemy))
    #print('points_enemy:_ ' , points_enemy)
    #print('puntos_final_list: ',puntos_final_list)
    points_f = list(np.add(puntos_final_list, points))
    '''
    print('points_f: ',points_f)
    print('col: ',checkcolum(grid,observation.mark))
    print('diag: ',checkdiagonal(grid,observation.mark))
    print('raw: ',checkraw(grid,observation.mark))
    print('points: ' , points)
    print(observation.board)
    '''
    valid_moves = [col for col in range(configuration.columns) if observation.board[col] == 0]    
    #print(valid_moves)
    for i in range(configuration.columns):
        if valid_moves.count(i) == 0:
            points_f[i] = -10000000000
    #print(points_f)
    choices = indices(points_f, max(points_f))
    
    return random.choice(choices)