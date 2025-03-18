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

#Directions
WEST = (0,-1)
NORTH = (1,0)
EAST = (0,1)
SOUTH = (-1,0)

evidence = [[1,0,1,1],
          [0,0,1,1],
          [0,0,0,1],
          [0,1,0,0],
          [0,0,0,0],
          [0,0,0,0]]

actions = [NORTH, EAST, NORTH, WEST, SOUTH]

maze = [[False, False, True, True, False, False, True, True, False],
       [False, False, False, True, False, False, True, False, False],
       [True, True, True, True, True, True, True, True, True],
       [False, False, True, True, True, True, True, True, False],
       [False, False, False, True, False, False, True, False, False]]

open_squares = [(c, r) for r in range(5) for c in range(9) if maze[r][c] == True]

ma = m.Maze(maze)

for n in zip(evidence[:-1], actions):
    #Evidence and Action respectively
    ev = n[0]
    ac = n[1]
    
    #Conduct filtering and print maze
    ma = c.filter(ma, open_squares, ev)
    print(f"Filtering after Evidence {ev}")
    print(ma)

    #Conduction prediction and print maze
    ma = c.prediction(ma, open_squares, ac)
    print(f"Prediction after Action {ac}")
    print(ma)

#Do the last filtering and print out the final maze
ma = c.filter(ma, open_squares, evidence[5])
print(f"Filtering after Evidence {ev}")
print(ma)