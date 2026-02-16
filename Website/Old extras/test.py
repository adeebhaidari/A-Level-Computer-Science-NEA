'''
defines the cube class
'''
import numpy as np
from pprint import pprint as pp

# Standard face numbering: U, D, F, B, L, R
FACE_U, FACE_D, FACE_F, FACE_B, FACE_L, FACE_R = 0, 1, 2, 3, 4, 5

class Cube:
    def __init__(self):
        self.cube = {
            FACE_U: np.array([['Y' for _ in range(3)] for _ in range(3)]),  # Up - Yellow
            FACE_D: np.array([['W' for _ in range(3)] for _ in range(3)]),  # Down - White
            FACE_F: np.array([['R' for _ in range(3)] for _ in range(3)]),  # Front - Red
            FACE_B: np.array([['O' for _ in range(3)] for _ in range(3)]),  # Back - Orange
            FACE_L: np.array([['B' for _ in range(3)] for _ in range(3)]),  # Left - Blue
            FACE_R: np.array([['G' for _ in range(3)] for _ in range(3)]),  # Right - Green
        }
        
        self.matcher = {
            'yellow': FACE_U,
            'white': FACE_D,
            'red': FACE_F,
            'orange': FACE_B,
            'blue': FACE_L,
            'green': FACE_R
        }
        
        # Define face relationships for easier reference
        self.opposite_face = {
            FACE_U: FACE_D, FACE_D: FACE_U,
            FACE_F: FACE_B, FACE_B: FACE_F,
            FACE_L: FACE_R, FACE_R: FACE_L
        }
    
    def get_adjacent_faces(self, front_face):
        """Get left, right, up, down faces relative to front face"""
        if front_face == FACE_F:  # Front
            return FACE_L, FACE_R, FACE_U, FACE_D
        elif front_face == FACE_B:  # Back
            return FACE_R, FACE_L, FACE_U, FACE_D
        elif front_face == FACE_L:  # Left
            return FACE_B, FACE_F, FACE_U, FACE_D
        elif front_face == FACE_R:  # Right
            return FACE_F, FACE_B, FACE_U, FACE_D
        elif front_face == FACE_U:  # Up
            return FACE_L, FACE_R, FACE_B, FACE_F
        else:  # Down
            return FACE_L, FACE_R, FACE_F, FACE_B
    
    # these rotates a given face only, not the adjacent corners and edges with it
    def rotate_face_clockwise(self, face):
        self.cube[face] = np.rot90(self.cube[face], 3)
    
    def rotate_face_anticlockwise(self, face):
        self.cube[face] = np.rot90(self.cube[face])
    
    def do_U(self, front_face):
        """U move - rotate upper face clockwise"""
        front_face = self.matcher[front_face]
        left_face, right_face, up_face, down_face = self.get_adjacent_faces(front_face)
        
        # Always rotate the actual U face
        self.rotate_face_clockwise(FACE_U)
        
        # For U move, we rotate the top layer of F, L, B, R faces
        temp = self.cube[FACE_F][0].copy()
        self.cube[FACE_F][0] = self.cube[FACE_R][0]
        self.cube[FACE_R][0] = self.cube[FACE_B][0]
        self.cube[FACE_B][0] = self.cube[FACE_L][0]
        self.cube[FACE_L][0] = temp
        
        return self.cube
    
    def do_D(self, front_face):
        """D move - rotate down face clockwise"""
        front_face = self.matcher[front_face]
        
        # Always rotate the actual D face
        self.rotate_face_clockwise(FACE_D)
        
        # For D move, we rotate the bottom layer of F, R, B, L faces
        temp = self.cube[FACE_F][2].copy()
        self.cube[FACE_F][2] = self.cube[FACE_L][2]
        self.cube[FACE_L][2] = self.cube[FACE_B][2]
        self.cube[FACE_B][2] = self.cube[FACE_R][2]
        self.cube[FACE_R][2] = temp
        
        return self.cube
    
    def do_L(self, front_face):
        """L move - rotate left face clockwise"""
        front_face = self.matcher[front_face]
        
        # Always rotate the actual L face
        self.rotate_face_clockwise(FACE_L)
        
        # For L move, we rotate the left column
        temp = self.cube[FACE_U][:, 0].copy()
        self.cube[FACE_U][:, 0] = self.cube[FACE_B][:, 2][::-1]  # Reverse for correct orientation
        self.cube[FACE_B][:, 2] = self.cube[FACE_D][:, 0][::-1]  # Reverse for correct orientation
        self.cube[FACE_D][:, 0] = self.cube[FACE_F][:, 0]
        self.cube[FACE_F][:, 0] = temp
        
        return self.cube
    
    def do_R(self, front_face):
        """R move - rotate right face clockwise"""
        front_face = self.matcher[front_face]
        
        # Always rotate the actual R face
        self.rotate_face_clockwise(FACE_R)
        
        # For R move, we rotate the right column
        temp = self.cube[FACE_U][:, 2].copy()
        self.cube[FACE_U][:, 2] = self.cube[FACE_F][:, 2]
        self.cube[FACE_F][:, 2] = self.cube[FACE_D][:, 2]
        self.cube[FACE_D][:, 2] = self.cube[FACE_B][:, 0][::-1]  # Reverse for correct orientation
        self.cube[FACE_B][:, 0] = temp[::-1]  # Reverse for correct orientation
        
        return self.cube
    
    def do_F(self, front_face):
        """F move - rotate front face clockwise"""
        front_face = self.matcher[front_face]
        
        # Always rotate the actual F face
        self.rotate_face_clockwise(FACE_F)
        
        # For F move, we rotate the front slice
        temp = self.cube[FACE_U][2].copy()
        self.cube[FACE_U][2] = self.cube[FACE_L][:, 2][::-1]  # Reverse for correct orientation
        self.cube[FACE_L][:, 2] = self.cube[FACE_D][0]
        self.cube[FACE_D][0] = self.cube[FACE_R][:, 0][::-1]  # Reverse for correct orientation
        self.cube[FACE_R][:, 0] = temp
        
        return self.cube
    
    def do_B(self, front_face):
        """B move - rotate back face clockwise"""
        front_face = self.matcher[front_face]
        
        # Always rotate the actual B face
        self.rotate_face_clockwise(FACE_B)
        
        # For B move, we rotate the back slice
        temp = self.cube[FACE_U][0].copy()
        self.cube[FACE_U][0] = self.cube[FACE_R][:, 2]
        self.cube[FACE_R][:, 2] = self.cube[FACE_D][2][::-1]  # Reverse for correct orientation
        self.cube[FACE_D][2] = self.cube[FACE_L][:, 0]
        self.cube[FACE_L][:, 0] = temp[::-1]  # Reverse for correct orientation
        
        return self.cube
    
    # Add counterclockwise moves
    def do_U_prime(self, front_face):
        """U' move - rotate upper face counterclockwise"""
        for _ in range(3):
            self.do_U(front_face)
    
    def do_D_prime(self, front_face):
        """D' move - rotate down face counterclockwise"""
        for _ in range(3):
            self.do_D(front_face)
    
    def do_L_prime(self, front_face):
        """L' move - rotate left face counterclockwise"""
        for _ in range(3):
            self.do_L(front_face)
    
    def do_R_prime(self, front_face):
        """R' move - rotate right face counterclockwise"""
        for _ in range(3):
            self.do_R(front_face)
    
    def do_F_prime(self, front_face):
        """F' move - rotate front face counterclockwise"""
        for _ in range(3):
            self.do_F(front_face)
    
    def do_B_prime(self, front_face):
        """B' move - rotate back face counterclockwise"""
        for _ in range(3):
            self.do_B(front_face)
    
    def rotate(self):
        pass
    
    def scramble(self):
        pass
    
    def reset(self):
        pass
    
    def check_solved(self):
        pass

    def map_colours_relative_to_bottom_cross(self, cross_colour):
        # map the colours relative to the white cross
        pass

    def get_opposite_colour(self, colour):
        pass


# --- Example Usage ---
cube = Cube()
cube.do_R('blue')
cube.do_L('red')  
cube.do_U('green')
pp(cube.cube)