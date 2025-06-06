"""
Expected Final HMM
S1 -> Z1 [1, 0, 1, 1]
| N
S2 -> Z2 [0, 0, 1, 1]
| E
S3 -> Z3 [0, 0, 0, 1]
| N
S4 -> Z4 [0, 1, 0, 0]
| W
S5 -> Z5 [0, 0, 0, 0]
| S
S6 -> Z6 [0, 0, 0, 0]
"""
import maze as m
import calculations as c

#Direction constants
WEST = (0,-1)
NORTH = (-1,0)
EAST = (0,1)
SOUTH = (1,0)

#Evidence for HMM
evidence = [[1,0,1,1], #Z1
          [0,0,1,1],   #Z2
          [0,0,0,1],   #Z3
          [0,1,0,0],   #Z4
          [0,0,0,0],   #Z5
          [0,0,0,0]]   #Z6

#Actions to go between the states
actions = [NORTH, EAST, NORTH, WEST, SOUTH]
#          S1-2   S2-3  S3-4   S4-5  S5-6

#Dictionary to help map direction constants to characters for printing
directions = {WEST: "W",
              NORTH: "N",
              EAST: "E",
              SOUTH: "S"}

#Maze represented by booleans
maze = [[False, False, False, False, False, False, False, False, False, False, False],
        [False, False, False,  True,  True, False, False,  True,  True, False, False],
        [False, False, False, False,  True, False, False,  True, False, False, False],
        [False,  True,  True,  True,  True,  True,  True,  True,  True,  True, False],
        [False, False, False,  True,  True,  True,  True,  True,  True, False, False],
        [False, False, False, False,  True, False, False,  True, False, False, False],
        [False, False, False, False, False, False, False, False, False, False, False]]

#Retrieve a list of all the non-obstacle squares within the maze (anything True)
open_squares = [(r, c) for r in range(m.ROW) for c in range(m.COL) if maze[r][c] == True]

#Initialize and print inital maze
ma = m.Maze(maze)
print("Initial Location Probabilities")
print(ma)

#Iterate through the HMM and get calculations
for n in zip(evidence[:-1], actions):
    #Evidence and Action respectively
    ev = n[0]
    ac = directions[n[1]]
    
    #Conduct filtering and print maze
    print(f"Filtering after Evidence {ev}")
    ma = c.filter(ma, open_squares, ev)
    print(ma)

    #Conduct prediction and print maze
    print(f"Prediction after Action {ac}")
    ma = c.prediction(ma, open_squares, ac)
    print(ma)
    
#Do the last filtering and print out the final maze
print(f"Filtering after Evidence {ev}")
ma = c.filter(ma, open_squares, evidence[5])
print(ma)