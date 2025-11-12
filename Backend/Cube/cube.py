'''

defines the cube class

'''


import numpy as np

# 'W', 'B', 'R', 'G', 'O', 'Y' VVV
FACE_D, FACE_L, FACE_F, FACE_R, FACE_B, FACE_U = 0,1,2,3,4,5

class Cube:
    def __init__(self):
        self.cube = np.array([[[colour for i in range(3)] for j in range(3)] for colour in ['W', 'B', 'R', 'G', 'O', 'Y']])
        self.edge_map = None
        
    def rotate_face(self,face_index,clockwise=True):
        pass
    
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

    def map_colours_relative_to_bottom_cross(self,cross_colour):
        # map the colours relative to the white cross
        pass

    def get_opposite_colour(self,colour):
        pass


# --- Example Usage ---
cube = Cube()
cross_colour = 'R'
mapped_cube, mapping = cube.map_to_white_cross_view('B')
print(cube.cube)
print()
print("colour Mapping:", mapping)
print("Mapped Cube:\n", mapped_cube)


    