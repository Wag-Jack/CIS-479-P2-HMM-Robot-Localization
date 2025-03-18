from maze import check_valid_dim

#Directions
WEST = (0,-1)
NORTH = (1,0)
EAST = (0,1)
SOUTH = (-1,0)

DIRECTIONS = (WEST, NORTH, EAST, SOUTH)

#Sensing Probabilities
DO_OP = 0.95  #Detect object w/ object present
NDO_OP = 0.05 #Not detect object w/ object present
DO_NO = 0.15  #Detect object w/ no object present
NDO_NO = 0.85 #Not detect object w/ no object present

#Moving Probabilities
STRAIGHT = 0.7
DRIFT_LEFT = 0.1
DRIFT_RIGHT = 0.2


def transitional_probability(state, maze, sense):
    trans_prob = 1
    
    for d in range[3]:
        nx = state[1] + DIRECTIONS[d][1]
        ny = state[0] + DIRECTIONS[d][0]

        if check_valid_dim(ny, nx):
            surrounding = maze[ny][nx]
            if sense[d] == 1:
                if surrounding.probability == -1.0:
                    trans_prob *= DO_OP
                else:
                    trans_prob *= NDO_OP
            else:
                if surrounding.probability != -1.0:
                    trans_prob *= DO_NO
                else:
                    trans_prob *= NDO_NO

    return trans_prob


def evidence_conditional_probability(state, maze, move):
    for d in DIRECTIONS:
        nx = state[1] + d[1]
        ny = state[0] + d[1]

        if check_valid_dim(ny, nx):
            surround = maze[ny][nx]
            


def filter(maze):
    pass


def prediction(maze):
    pass