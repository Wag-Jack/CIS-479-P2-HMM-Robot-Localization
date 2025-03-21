from maze import ROW, COL

#Direction constants
WEST = (0,-1)
NORTH = (-1,0)
EAST = (0,1)
SOUTH = (1,0)

#List of directions to iterate for probability functions
DIRECTIONS = [WEST, NORTH, EAST, SOUTH]

#Sensing Probabilities
TP = 0.95  #Detect obstacle w/ obstacle present (true positive)
FN = 0.05 #Not detect obstacle w/ obstacle present (false negative)
FP = 0.15  #Detect obstacle w/ no obstacle present (false positive)
TN = 0.85 #Not detect obstacle w/ no obstacle present (true negative)

#Moving Probabilities
STRAIGHT = 0.7 #Move straight in given direction
DRIFT_LEFT = 0.1 #Robot drifts left in given direction
DRIFT_RIGHT = 0.2 #Robot drifts right in given direction

#Lists to help match for transitional probabilities
MOVING_PROB = [DRIFT_RIGHT, DRIFT_LEFT, STRAIGHT]
RELATIVE_MOVING_PROB = [DRIFT_LEFT, DRIFT_RIGHT, None]

#Ensure space is either wall or in maze
def check_valid_dim(col, row):
    return True if 0 <= row <= ROW-1 and 0 <= col <= COL-1 else False

#Function to determine evidence conditional probability in filtering
#P(Z_t|S_t) = P(Z_W,t|S_t)P(Z_N,t|S_t)P(Z_E,t|S_t)P(Z_S,t|S_t)
def evidence_conditional_probability(state, maze, evidence):
    #Will be multiplied by probability of each direction
    ev_cond_prob = 1
    
    #Save the location of the state
    state_loc = state.get_location()

    #Look at the neighbors in all four direction 
    for d in range(4):
        #Get neighbor's coordinates
        nx = state_loc[1] + DIRECTIONS[d][1]
        ny = state_loc[0] + DIRECTIONS[d][0]

        #Ensure neighbor is a valid state
        if check_valid_dim(nx, ny):
            #Get information about the neighboring state
            surrounding = maze.read_state(ny, nx)

            if evidence[d] == 1: #1 -> obstacle detected
                if surrounding.probability == -1.0:
                    ev_cond_prob *= TP #obstacle present
                else:
                    ev_cond_prob *= FP #no obstacle present
            else: #0 -> obstacle not detected
                if surrounding.probability != -1.0:
                    ev_cond_prob *= TN #obstacle present
                else:
                    ev_cond_prob *= FN #no obstacle present

    #Return evidence conditional probability after multiplying all four directions
    return ev_cond_prob

#Function to determine the sum of transitional probabilities in prediction
#P(S_t+1|Z_1=z_1,...,Z_t=z_t) = \sum_s{P(S_t+1|S_t=s)P(S_t|Z_1=z_1,...,Z_t=z_t)}
def sum_transitional_probability(state, maze, move):
    #Helper function to check if state is an obstacle or not
    def is_obstacle(ny, nx):
        #Obstacle = True, No obstacle = False
        return True if maze.read_state(ny, nx).probability == -1.0 else False
    
    #Convert string variable move to actual directions
    m = {'W': WEST,
        'N': NORTH,
        'E': EAST,
        'S': SOUTH}

    #Record move as actual tuple constant
    mo = m[move]

    #Initial sum set to zero for given state
    sum_trans_prob = 0

    #Save the location of the state
    state_loc = state.get_location()

    #Get indices for relative locations
    d = (DIRECTIONS.index(mo) - 2) % 4
    l_index = (d + 1) % 4
    r_index = (d - 1) % 4

    #Find "left", "right", and "opposite" neighbors
    left = DIRECTIONS[l_index]
    right = DIRECTIONS[r_index] 
    opposite = DIRECTIONS[d]

    #Record neighbors as potential moves into this state
    moves = [left, right, opposite]

    #Run through each neighbor and see how it affects the current state
    for action in zip(moves, MOVING_PROB, RELATIVE_MOVING_PROB):
        #Get neighbor's coordinates
        nx = state_loc[1] + action[0][1]
        ny = state_loc[0] + action[0][0]
        
        #Check that neighbor is valid neighbor
        if check_valid_dim(nx, ny):
            #Get information about the neighboring state
            neighbor = maze.read_state(ny, nx)

            #Check if neighbor is an obstacle or not
            if is_obstacle(ny, nx): #Is an obstacle
                #Ensure the obstacle is not behind this state
                #Will lead to inaccurate calculations
                if action[0] != opposite:
                    #Add the probability of bouncing into an obstacle
                    sum_trans_prob += action[2] * state.probability
            else:
                #Add probability of neighbor moving into this state
                sum_trans_prob += action[1] * neighbor.probability

    #This last check is to check if the state straight ahead of this state is an obstacle
    #and if we need to account the probability of bouncing back into this state.
    
    #Get the coordinates of the state in front of this one
    nx = state_loc[1] + mo[1]
    ny = state_loc[0] + mo[0]

    #Ensure front neighbor is valid
    if check_valid_dim(nx, ny):
        #Read information about state in front of this one
        ahead = maze.read_state(ny, nx)
        
        #Check if ahead state is an obstacle
        if ahead.probability == -1.0:
            #Add this bouncing probability and return it
            return sum_trans_prob + (STRAIGHT * state.probability)

    #If not, return the sum calculated already
    return sum_trans_prob

#Function to determine the filtering probability
#P(S_t|Z_1=z_1,...,Z_t=z_t) proportional to P(Z_t=z_t|S_t)P(S_t|Z_1=z_1,...,Z_t-1=z_t-1)
def filter(maze, spaces, evidence):
    #Initialize normalization constant
    normalization_constant = 0
    
    #Run through each non-obstacle space in the maze
    for s in spaces:
        #Access spot in the maxe
        curr = maze.read_state(s[0], s[1])
        
        #Read the state's prior probability
        prior = curr.probability

        #Calculate the evidence conditional probability for this state
        evp = evidence_conditional_probability(curr, maze, evidence)

        #Multiply to determine the posterior probability
        posterior = evp * prior

        #Save the posterior probability to each state
        curr.probability = posterior

        #Add each posterior probability to determine normalization constant
        normalization_constant += posterior
            
    #Run through all non-obstacle spaces in the maze again
    for s in spaces:
        #Access spot in the maze
        curr = maze.read_state(s[0], s[1])
        
        #Conduct normalization on every state
        curr.probability /= normalization_constant

    #Return the resulting maze following filtering
    return maze

#Function to determine the prediction probability
#Same as sum_transitional_probability
def prediction(maze, spaces, action):
    #Initialize list of probabilities before applying them to final maze
    temp_prob = list()
    
    #Run through each non-obstacle space in the maze
    for s in spaces:
        #Access spot in the maze
        curr = maze.read_state(s[0], s[1])

        #Save the probabilities we calculated, but don't apply them to the maze yet
        temp_prob.append(sum_transitional_probability(curr, maze, action))

    #Run through each non-obstacle space again, keeping track of calculated probabilities
    for s in zip(spaces, temp_prob):
        #Get information about space on the maze
        space = s[0]
        curr = maze.read_state(space[0], space[1])

        #Set probability of each space to calculated probability
        curr.probability = s[1]

    #Return the final maze
    return maze