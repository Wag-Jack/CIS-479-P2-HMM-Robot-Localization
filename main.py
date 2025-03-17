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

maze = ([False, False, True, True, False, False, True, True, False],
       [False, False, False, True, False, False, True, False, False],
       [True, True, True, True, True, True, True, True, True],
       [False, False, True, True, True, True, True, True, False],
       [False, False, False, True, False, False, True, False, False])

ma = m.Maze(maze)
print(ma)