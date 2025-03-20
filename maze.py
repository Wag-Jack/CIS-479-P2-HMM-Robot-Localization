"""
     |||| |||| |||| |||| |||| |||| |||| |||| ||||
|||| #### #### 0.00 0.00 #### #### 0.00 0.00 #### ||||

|||| #### #### #### 0.00 #### #### 0.00 #### #### ||||

|||| 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 0.00 ||||

|||| #### #### 0.00 0.00 0.00 0.00 0.00 0.00 #### ||||

|||| #### #### #### 0.00 #### #### 0.00 #### #### ||||
     |||| |||| |||| |||| |||| |||| |||| |||| ||||
"""

ROW = 7
COL = 11

class Location:
    def __init__(self, s, p):
        self.space = (s[0], s[1])
        self.probability = p

    def __str__(self):
        return f'{self.space}'

    def get_location(self):
        return self.space

class Maze:
    def __init__(self, m):
        self.maze = list()
        for r in range(ROW):
            temp = list()
            for c in range(COL):

                if m[r][c]:
                    temp.append(Location((r, c), 0.0435))
                else:
                    temp.append(Location((r, c), -1.0))
            self.maze.append(temp)

    def __str__(self):
        output = ''
        for r in range(1,ROW-1):
            for c in range(1,COL-1):
                prob = self.maze[r][c].probability
                if prob == -1.0:
                    output += ' #### ' 
                elif prob != None:
                    round_prob = round(prob, 4) * 100
                    if round_prob < 10.00:
                        output += ' ' 
                    output += f'{round_prob:.2f} '
            output += '\n'
        return output
    
    def read_state(self, r, c):
        return self.maze[r][c]