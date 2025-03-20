"""
#### #### 0.00 0.00 #### #### 0.00 0.00 ####

#### #### #### 0.00 #### #### 0.00 #### ####

0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00

#### #### 0.00 0.00 0.00 0.00 0.00 0.00 ####

#### #### #### 0.00 #### #### 0.00 #### ####
"""

ROW = 5
COL = 9

class Location:
    def __init__(self, s, p):
        self.space = (s[1], s[0])
        self.probability = p

    def get_location(self):
        return self.space

class Maze:
    def __init__(self, m):
        self.maze = list()
        for r in range(ROW):
            temp = list()
            for c in range(COL):
                if m[r][c]:
                    temp.append(Location((c, r), 4.35))
                else:
                    temp.append(Location((c, r), -1.0))
            self.maze.append(temp)

    def __str__(self):
        output = ''
        for r in range(ROW):
            for c in range(COL):
                prob = self.maze[r][c].probability
                if prob == -1.0:
                    output += ' XXXX ' #print(' XXXX ', end='')
                else:
                    round_prob = round(prob, 2)
                    if round_prob < 10.00:
                        output += ' ' #print(' ', end='')
                    output += f'{round_prob} ' #print(f'{round_prob} ', end='')
            output += '\n' #print()
        return output
    
    def read_state(self, c, r):
        return self.maze[c][r]