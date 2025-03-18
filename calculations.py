from maze import check_valid_dim

#Directions
WEST = (0,-1)
NORTH = (1,0)
EAST = (0,1)
SOUTH = (-1,0)

DIRECTIONS = [WEST, NORTH, EAST, SOUTH]

#Sensing Probabilities
DO_OP = 0.95  #Detect obstacle w/ obstacle present
NDO_OP = 0.05 #Not detect obstacle w/ obstacle present
DO_NO = 0.15  #Detect obstacle w/ no obstacle present
NDO_NO = 0.85 #Not detect obstacle w/ no obstacle present

#Moving Probabilities
STRAIGHT = 0.7
DRIFT_LEFT = 0.1
DRIFT_RIGHT = 0.2


def evidence_conditional_probability(state, maze, evidence):
    trans_prob = 1
    
    for d in range(3):
        nx = state[1] + DIRECTIONS[d][1]
        ny = state[0] + DIRECTIONS[d][0]

        if check_valid_dim(ny, nx):
            surrounding = maze[ny][nx]
            if evidence[d] == 1: #1 -> obstacle detected
                if surrounding.probability == -1.0:
                    trans_prob *= DO_OP
                else:
                    trans_prob *= NDO_OP
            else: #0 -> obstacle not detected
                if surrounding.probability != -1.0:
                    trans_prob *= DO_NO
                else:
                    trans_prob *= NDO_NO

    return trans_prob


def transitional_probability(state, maze, move):
    def check_bounce_or_obstacle(nx, ny):
        return True if ((nx == -1 or nx == 10) and (ny == -1 or ny == 6)) else True if maze[nx][ny].probability == -1.0 else False

    ev_cond_prob = 1

    relative_directions = [EAST, SOUTH, WEST, NORTH]

    for d in DIRECTIONS:

        #Get coordinates of neighboring state for each direction
        nx = state[1] + DIRECTIONS[d][1]
        ny = state[0] + DIRECTIONS[d][0]

        #Ensure valid location
        if check_bounce_or_obstacle(ny, nx):
            #Determine neighbor's location
            neighbor = maze[ny][nx]
            
            #Same direction non-obstacle does not add to
            #evidence conditional probability
            if d == move and neighbor.probability != -1.0:
                pass 

            #Determine the left and right directions
            dir = DIRECTIONS.index(d)
            left = DIRECTIONS[(dir - 1) % 4]
            right = DIRECTIONS[(dir + 1) % 4]

            #Determine what direction the neighbor will be moving
            neighbor_move = relative_directions[dir]

            #Apply probability based on what direction the neighbor is in
            if neighbor_move == left:
                ev_cond_prob *= 0.1
            elif neighbor_move == right:
                ev_cond_prob *= 0.2
            else:
                ev_cond_prob *= 0.7

    return ev_cond_prob


def filter(maze, spaces, evidence):
    for s in spaces:
        prior = s.probability
        evp = evidence_conditional_probability(s, maze, evidence)
        posterior = evp * prior
        s.probability = posterior


def prediction(maze, spaces, action):
    for s in spaces:
        prior = s.probability
        tp = transitional_probability(s, maze, action)
        posterior = tp * prior #sum of tp?
        s.probability = posterior