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


def evidence_conditional_probability(state, maze, evidence):
    def check_valid_dim(col, row):
        return True if 0 <= row <= ROW-1 and 0 <= col <= COL-1 else False
    
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
    trans_prob = 0

    relative_directions = [EAST,SOUTH,WEST,NORTH]

    state_loc = state.get_location()



def transitional_probability(state, maze, move):
    #TODO: Differentiate between bounce and obstacle
    def check_bounce_or_obstacle(ny, nx):
        if (nx == -1 or nx == COL) and (ny == -1 or ny == ROW):
            return True
        else:
            neighbor = maze.read_state(ny, nx)
            if neighbor.probability == -1:
                return True
            else:
                return False

    ev_cond_prob = 1

    relative_directions = [EAST, SOUTH, WEST, NORTH]

    state_loc = state.get_location()

    for d in range(3):
        #Get coordinates of neighboring state for each direction
        nx = state_loc[1] + DIRECTIONS[d][1]
        ny = state_loc[0] + DIRECTIONS[d][0]
        #print((ny, nx))

        #Ensure valid location
        if check_bounce_or_obstacle(ny, nx):
            #Determine neighbor's location
            neighbor = maze.read_state(ny, nx)
            
            #Same direction non-obstacle does not add to
            #evidence conditional probability
            if d == move and neighbor.probability != -1.0:
                pass 

            #Determine the left and right directions
            left = DIRECTIONS[(d - 1) % 4]
            right = DIRECTIONS[(d + 1) % 4]

            #Determine what direction the neighbor will be moving
            neighbor_move = relative_directions[d]

            #Apply probability based on what direction the neighbor is in
            if neighbor_move == left:
                ev_cond_prob *= 0.1
            elif neighbor_move == right:
                ev_cond_prob *= 0.2
            else:
                ev_cond_prob *= 0.7

    return ev_cond_prob

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
        
        prior = curr.probability
        tp = transitional_probability(curr, maze, action)
        posterior = tp * prior #sum of tp?
        curr.probability = posterior

    return maze