from maze import ROW, COL

#Directions
WEST = (0,-1)
NORTH = (-1,0)
EAST = (0,1)
SOUTH = (1,0)

DIRECTIONS = [WEST, NORTH, EAST, SOUTH]

#Sensing Probabilities
TP = 0.95  #Detect obstacle w/ obstacle present (true positive)
FN = 0.05 #Not detect obstacle w/ obstacle present (false negative)
FP = 0.15  #Detect obstacle w/ no obstacle present (false positive)
TN = 0.85 #Not detect obstacle w/ no obstacle present (true negative)

#Moving Probabilities
STRAIGHT = 0.7
DRIFT_LEFT = 0.1
DRIFT_RIGHT = 0.2

MOVING_PROB = [DRIFT_LEFT, STRAIGHT, DRIFT_RIGHT]

def check_valid_dim(col, row):
    return True if 0 <= row <= ROW-1 and 0 <= col <= COL-1 else False

def evidence_conditional_probability(state, maze, evidence):
    ev_cond_prob = 1
    
    state_loc = state.get_location()

    for d in range(4):
        nx = state_loc[1] + DIRECTIONS[d][1]
        ny = state_loc[0] + DIRECTIONS[d][0]

        if check_valid_dim(nx, ny):
            surrounding = maze.read_state(ny, nx)

            if evidence[d] == 1: #1 -> obstacle detected
                if surrounding.probability == -1.0:
                    ev_cond_prob *= TP
                else:
                    ev_cond_prob *= FP
            else: #0 -> obstacle not detected
                if surrounding.probability != -1.0:
                    ev_cond_prob *= TN
                else:
                    ev_cond_prob *= FN

    return ev_cond_prob

"""
1. Look at surrounding states
2. Check if border/obstacle or not
    a. Yes? Add movement * prior of current state.
    b. No? Add movement * prior of neighbor
3. Sum all three probabilities and return
"""

#TODO: Fix transitional probability :)
def sum_transitional_probability(state, maze, move):
    def is_obstacle(ny, nx):
        #Obstacle = True, No obstacle = False
        return True if maze.read_state(ny, nx).probability == -1.0 else False
    
    m = {'W': WEST,
        'N': NORTH,
        'E': EAST,
        'S': SOUTH}

    mo = m[move]

    sum_trans_prob = 0

    state_loc = state.get_location()

    relative_directions =  {WEST: EAST,
                           NORTH: SOUTH,
                           EAST: WEST,
                           SOUTH: NORTH}

    """
    Relative moving directions
    _____ down_ _____
    right state left_
    _____ _up__ _____
    """

    #Get indices for relative locations
    d = (DIRECTIONS.index(mo) - 2) % 4
    l_index = (d + 1) % 4
    r_index = (d - 1) % 4

    #Find "left" and "right" neighbors
    left = DIRECTIONS[l_index]
    right = DIRECTIONS[r_index] 
    opposite = DIRECTIONS[d]

    moves = [left, opposite, right]
    #print(moves)

    for action in zip(moves, MOVING_PROB):
        #print(action)
        nx = state_loc[1] + relative_directions[action[0]][1]
        ny = state_loc[0] + relative_directions[action[0]][0]
        
        if check_valid_dim(ny, nx):
            neighbor = maze.read_state(ny, nx)

            if is_obstacle(ny, nx):
                sum_trans_prob += action[1] * state.probability
            else:
                sum_trans_prob += action[1] * neighbor.probability

    return sum_trans_prob


def filter(maze, spaces, evidence):
    normalization_constant = 0
    
    for s in spaces:
        #Access spot in the maxe
        curr = maze.read_state(s[0], s[1])
        
        prior = curr.probability
        evp = evidence_conditional_probability(curr, maze, evidence)
        posterior = evp * prior

        curr.probability = posterior

        normalization_constant += posterior
            
    for s in spaces:
        curr = maze.read_state(s[0], s[1])
        curr.probability /= normalization_constant

    return maze


def prediction(maze, spaces, action):
    for s in spaces:
        #Access spot in the maze
        curr = maze.read_state(s[0], s[1])
        curr.probability = sum_transitional_probability(curr, maze, action)

    return maze