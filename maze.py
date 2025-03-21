"""
     |||| |||| |||| |||| |||| |||| |||| |||| ||||
|||| #### #### 4.35 4.35 #### #### 4.35 4.35 #### ||||

|||| #### #### #### 4.35 #### #### 4.35 #### #### ||||

|||| 4.35 4.35 4.35 4.35 4.35 4.35 4.35 4.35 4.35 ||||

|||| #### #### 4.35 4.35 4.35 4.35 4.35 4.35 #### ||||

|||| #### #### #### 4.35 #### #### 4.35 #### #### ||||
     |||| |||| |||| |||| |||| |||| |||| |||| ||||
"""

#row and column constants
ROW = 7
COL = 11

#Class to define each square in the maze w/ probability
class Location:
    #initializer
    def __init__(self, s, p):
        self.space = (s[0], s[1]) #(row, column)
        self.probability = p

    #method to help print space w/ probability
    def __str__(self):
        return f'{self.space}'

    #method to get coordinates of space on maze
    def get_location(self):
        return self.space

#Class to define the maze itself
class Maze:
    #initializer
    def __init__(self, m):
        #self.maze is a 2d list
        self.maze = list()
        for r in range(ROW):
            temp = list()
            for c in range(COL):
                if m[r][c]: #not an obstacle/wall
                    temp.append(Location((r, c), 0.0435))
                else: #is an obstacle/wall
                    temp.append(Location((r, c), -1.0))
            self.maze.append(temp)

    #method to print out the entire map without the walls
    def __str__(self):
        output = ''
        for r in range(1,ROW-1):
            for c in range(1,COL-1):
                prob = self.maze[r][c].probability
                if prob == -1.0: #is an obstacle
                    output += ' #### ' 
                else:
                    #Probabiity represented out of 100 to two decimal places
                    round_prob = round(prob, 4) * 100
                    if round_prob < 10.00:
                        output += ' ' #Adjust spacing if only three digits shown 
                    output += f'{round_prob:.2f} '
            output += '\n' #Next row
        return output
    
    #Get Location object from space for coordinates and probability
    def read_state(self, r, c):
        return self.maze[r][c]