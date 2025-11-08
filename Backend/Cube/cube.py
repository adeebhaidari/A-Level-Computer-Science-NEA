'''

defines the cube class

'''


import numpy as np

FACE_U, FACE_L, FACE_F, FACE_R, FACE_B, FACE_D = 0,1,2,3,4,5

class Cube:
    def __init__(self, cross_colour):
        self.cube = np.array([[[colour for i in range(3)] for j in range(3)] for colour in ['W', 'B', 'R', 'G', 'O', 'Y']])
        self.down_down_face = cross_colour

    def do_L(self,down_face):
        pass
    
    def do_R(self,down_face):
        pass
    
    def do_U(self,down_face):
        pass
    
    def do_D(self,down_face):
        pass
    
    def do_F(self,down_face):
        pass
    
    def do_B(self,down_face):
        pass
    
    def rotate(self,down_face):
        pass
    
    def scramble(self):
        pass
    
    def reset(self):
        pass
    
    def check_solved(self):
        pass
    
    
cube = Cube()
print(cube.cube)