'''

defines the cube class

'''


import numpy as np

FACE_U, FACE_L, FACE_F, FACE_R, FACE_B, FACE_D = 0,1,2,3,4,5

class Cube:
    def __init__(self):
        self.cube = np.array([[[colour for i in range(3)] for j in range(3)] for colour in ['W', 'B', 'R', 'G', 'O', 'Y']])

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
    import numpy as np

    def map_to_white_cross_view(self,cross_color):
        """
        Maps the cube colors so that the given cross_color is treated as white.
        Returns the mapped cube and the color mapping dictionary.
        
        cube_array: np.array of shape (6,3,3) representing cube faces in order [U,L,F,R,B,D]
        cross_color: str, the color of the bottom cross
        """
        
        # Standard cube order (white cross view)
        standard_faces = ['W','O','G','R','B','Y']  # U,L,F,R,B,D
        
        # Determine rotation mapping for the cross
        # Map the cross_color to 'W' (white)
        # Map opposite face to 'Y' (yellow)
        # Map side colors to O,G,R,B in clockwise order starting from the left face relative to cross
        side_colors = [c for c in ['W','O','G','R','B','Y'] if c != cross_color and c != self.get_opposite_color(cross_color)]
        
        # Create color mapping
        color_mapping = {cross_color: 'W', self.get_opposite_color(cross_color): 'Y'}
        
        # Map the side colors clockwise starting from 'L'
        standard_side_order = ['O','G','R','B']
        for orig, mapped in zip(side_colors, standard_side_order):
            color_mapping[orig] = mapped
        
        # Apply the mapping to the cube
        mapped_cube = np.empty_like(self.cube)
        for f in range(6):
            for i in range(3):
                for j in range(3):
                    mapped_cube[f,i,j] = color_mapping[self.cube[f,i,j]]
                    
        return mapped_cube, color_mapping


    def get_opposite_color(self,color):
        """Return the opposite face color."""
        opposites = {'W':'Y', 'Y':'W', 'O':'R', 'R':'O', 'G':'B', 'B':'G'}
        return opposites[color]


# --- Example Usage ---
cube = Cube()
cross_color = 'R'
mapped_cube, mapping = cube.map_to_white_cross_view('B')
print(cube.cube)
print()
print("Color Mapping:", mapping)
print("Mapped Cube:\n", mapped_cube)

    