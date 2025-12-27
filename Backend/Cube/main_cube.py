import numpy as np
from pprint import pprint as pp
import random

# indexes: white = 0, blue = 1, red = 2, green = 3, orange = 4, yellow = 5 
# the bottom face is white, front face is red, left face is blue, right face is green, back face is orange, top face is yellow. everything is relative this.

class Cube:
    def __init__(self):
        self.cube = self.reset()
        # this dictionary stores the method references without calling them, these will be called later by adding the brackets ()
        # dont think ill be using this yet
        '''
        self.pruning_map = {
            'R': ['R"', 'R2'],
            'L': ['L"', 'L2'],
            'U': ['U"', 'U2'],
            'D': ['D"', 'D2'],
            'F': ['F"', 'F2'],
            'B': ['B"', 'B2'],
            'R"': 'R',
            'L"': 'L',
            'U"': 'U',
            'D"': 'D',
            'F"': 'F',
            'B"': 'B',
            'R2': 'R2',
            'L2': 'L2',
            'U2': 'U2',
            'D2': 'D2',
            'F2': 'F2',
            'B2': 'B2'
        }
        '''
        self.notation_map = {
            'R': self.R,
            'R"': self.R_prime,
            'L': self.L,
            'L"': self.L_prime,
            'U': self.U,
            'U"': self.U_prime,
            'D': self.D,
            'D"': self.D_prime,
            'F': self.F,
            'F"': self.F_prime,
            'B': self.B,
            'B"': self.B_prime,
            'R2': self.R2,
            'L2': self.L2,
            'U2': self.U2,
            'D2': self.D2,
            'F2': self.F2,
            'B2': self.B2,
            'x': self.rotate_x,
            'x"': self.rotate_x_prime,
            'y': self.rotate_y,
            'y"': self.rotate_y_prime,
            'x': self.rotate_z,
            'x"': self.rotate_z_prime
        }
    
    def reset(self):
        cube = [[[sticker]*3 for i in range(3)] for sticker in ['W', 'B', 'R', 'G', 'O', 'Y']]
        return np.array(cube, dtype=object)
    
    def copy(self):
        pass
    
    # ------------------------------- #
    # helper methods for cube movement
    
    def rotate_face_cw(self, face):
        self.cube[face] = np.rot90(self.cube[face], -1)
    
    def rotate_face_acw(self, face):
        self.cube[face] = np.rot90(self.cube[face], 1)
    
    def cycle_stickers(self, direction, positions):
        groups = positions if direction=='cw' else positions[::-1]
        tmp_values = [self.cube[f,r,c] for f,r,c in groups[-1]]
        # shiftingh the stickers from the previous group to current group - except the last one
        for i in reversed(range(1, len(groups))):
            for j, (f,r,c) in enumerate(groups[i]):
                f_prev, r_prev, c_prev = groups[i-1][j]
                self.cube[f,r,c] = self.cube[f_prev, r_prev, c_prev]
        # permuting the last group in positions
        for j, (f,r,c) in enumerate(groups[0]):
            self.cube[f,r,c] = tmp_values[j]

    
    # ------------------------------ #
    # cube move methods
    
    # the positions variable holds the positions of each sticker to be permuted with there respecive edge/corner face sticker
        # (a,b,c) = (face,row,col)
        # for each face value in the tuples in each array, there next one is the clockwise rotation
    
    def U(self):
        self.rotate_face_cw(5)
        positions = [
            [(2,0,0),(2,0,1),(2,0,2)],
            [(1,0,0),(1,0,1),(1,0,2)],
            [(4,0,0),(4,0,1),(4,0,2)],
            [(3,0,0),(3,0,1),(3,0,2)]
        ]
        self.cycle_stickers('cw', positions)

    def D(self):
        self.rotate_face_cw(0)
        positions = [
            [(2,2,0),(2,2,1),(2,2,2)],
            [(3,2,0),(3,2,1),(3,2,2)],
            [(4,2,0),(4,2,1),(4,2,2)],
            [(1,2,0),(1,2,1),(1,2,2)]
        ]
        self.cycle_stickers('cw', positions)
    
    def L(self):
            self.rotate_face_cw(1)
            positions = [
                [(2,0,0),(2,1,0),(2,2,0)],
                [(0,0,0),(0,1,0),(0,2,0)],
                [(4,2,2),(4,1,2),(4,0,2)],
                [(5,0,0),(5,1,0),(5,2,0)]
            ]
            self.cycle_stickers('cw', positions)
        
    def R(self):
            self.rotate_face_cw(3)
            # the back face is 'upside down' relative to the front when rotating over the top
            positions = [
                [(2,0,2),(2,1,2),(2,2,2)],
                [(5,0,2),(5,1,2),(5,2,2)],
                [(4,2,0),(4,1,0),(4,0,0)],
                [(0,0,2),(0,1,2),(0,2,2)]
            ]
            self.cycle_stickers('cw', positions)

    def F(self):
        self.rotate_face_cw(2)
        positions = [
            [(5,2,0),(5,2,1),(5,2,2)],
            [(3,0,0),(3,1,0),(3,2,0)],
            [(0,0,2),(0,0,1),(0,0,0)],
            [(1,2,2),(1,1,2),(1,0,2)]
        ]
        self.cycle_stickers('cw', positions)

    def B(self):
        self.rotate_face_cw(4)
        positions = [
            [(5,0,2),(5,0,1),(5,0,0)],
            [(1,0,0),(1,1,0),(1,2,0)],
            [(0,2,0),(0,2,1),(0,2,2)],
            [(3,2,2),(3,1,2),(3,0,2)]
        ]
        self.cycle_stickers('cw', positions)

    def U_prime(self):
        for i in range(3):
            self.U()

    def D_prime(self):
        for i in range(3):
            self.D()

    def L_prime(self):
        for i in range(3):
            self.L()

    def R_prime(self):
        for i in range(3):
            self.R()

    def F_prime(self):
        for i in range(3):
            self.F()

    def B_prime(self):
        for i in range(3):
            self.B()
    
    def U2(self):
        for i in range(2):
            self.U()

    def D2(self):
        for i in range(2):
            self.D()

    def L2(self):
        for i in range(2):
            self.L()

    def R2(self):
        for i in range(2):
            self.R()

    def F2(self):
        for i in range(2):
            self.F()

    def B2(self):
        for i in range(2):
            self.B()
            
    def rotate_x(self):
        self.rotate_face_acw(1)
        self.rotate_face_cw(3)
        old_cube = self.cube.copy()
        self.cube[2] = old_cube[0]
        self.cube[5] = old_cube[2]
        self.cube[4] = np.rot90(old_cube[5], 2)
        self.cube[0] = np.rot90(old_cube[4], 2)
    
    def rotate_y(self):
        self.rotate_face_cw(5)
        self.rotate_face_acw(0)
        old_cube = self.cube.copy()
        self.cube[2] = old_cube[3]
        self.cube[3] = old_cube[4]
        self.cube[4] = old_cube[1]
        self.cube[1] = old_cube[2]
    
    def rotate_z(self):
        self.rotate_face_cw(2)
        self.rotate_face_acw(4)
        old_cube = self.cube.copy()
        self.cube[3] = np.rot90(old_cube[5], 1)
        self.cube[0] = np.rot90(old_cube[3], 1)
        self.cube[1] = np.rot90(old_cube[0], 1)
        self.cube[5] = np.rot90(old_cube[1], 1)
        
    def rotate_x_prime(self):
        for i in range(3):
            self.rotate_x()
    
    def rotate_y_prime(self):
        for i in range(3):
            self.rotate_y()
    
    def rotate_z_prime(self):
        for i in range(3):
            self.rotate_z()
    
    # ------------------------- #
    # applying movement methods
    
    def apply_move(self, move):
        self.notation_map[move]()
    
    def apply_move_sequence(self, sequence):
        moves = sequence.split()
        for move in moves:
            self.notation_map[move]()
    
    def reorient(self, front, bottom):
        # this method will reorient the cube into a certain position based onn a given front and bottom face
        # think of it as rotating the cube in the x, y and z axis until it matches the given description of its orientation
        for i in range(4):
            if self.cube[2][1,1] == front:
                break
            self.rotate_y()
        if self.cube[2][1,1] != front:
            for j in range(4):
                if self.cube[2][1,1] == front:
                    break
            self.rotate_x()
        for k in range(4):
            if self.cube[0][1,1] == bottom:
                break
            self.rotate_z()
    
    # --------------------- #
    # state inspection methods
    
    def is_solved(self):
        return self.cube == self.reset()
    
    def get_face(self, face):
        return self.cube[face]
        
    # ------------------------ #
    # scramble method/s - may need more methods later on
    
    def scramble(self, scramble=None):
        # instead of using a while loop within the for loop for pruning, I will be only using a for loop but constantly regenerating the potential moves - this heavily reduces the time complexity down to O(L) where L is the length of the scramble
        # fix the logic error so X or X" or X2 arent next to each other in the scramble - do later
        if scramble == None:
            moves = ['R', 'R"', 'R2', 'L', 'L"', 'L2', 'D', 'D"', 'D2', 'U', 'U"', 'U2', 'F', 'F"', 'F2', 'B', 'B"', 'B2']
            scramble = []
            prev_move = None
            for i in range(25):
                potential_moves = [move for move in moves if prev_move is None or move[0] != prev_move[0]]
                move = random.choice(potential_moves)
                scramble.append(move)
                prev_move = move
        complete_scramble = ' '.join(scramble)
        self.apply_move_sequence(complete_scramble)
        return complete_scramble