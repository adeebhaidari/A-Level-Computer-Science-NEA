from queue import PriorityQueue
import main_cube
import itertools
import numpy as np
from pprint import pprint as pp
import sqlite3

class Solver(main_cube.Cube):
    def __init__(self):
        super().__init__()
        self.pll_mappings = {
            '131212323444': 'Ub Perm',
            '121232313444': 'Ua Perm',
            '141232323414': 'Z Perm',
            '131242313424': 'H Perm',
            
            '214123431341': 'E Perm',
            '122331243414': 'Aa Perm',
            '244112323431': 'Ab Perm',
            
            '131223412344': 'T Perm',
            '111243432324': 'F Perm',
            '441222334113': 'Ja Perm',
            '111233422344': 'Jb Perm',
            '141223432314': 'Ra Perm',
            '411232324143': 'Rb Perm',
            
            '311224143432': 'V Perm',
            '341224133412': 'Y Perm',
            '133422311244': 'Na Perm',
            '331224113442': 'Nb Perm',
            
            '141233412324': 'Ga Perm',
            '132311243424': 'Gb Perm',
            '121243412334': 'Gc Perm',
            '131213442324': 'Gd Perm'
            }
        
    # --------- helper functions  ------------- #
    
    def cube_to_state(self, cube):
        return tuple(tuple(tuple(row) for row in face) for face in cube)
    
    def state_to_cube(self, state):
        return np.array(state, dtype=object)
    
    # -------- cube state validation  ------------- #
    # make soon
    
    # ------- Getting algorithms from data base ----- #
    def get_algorithm(self, case):
        connection = sqlite3.connect('speedcubing.db')
        cursor = connection.cursor()
        
        cursor.execute('SELECT Notation from Algorithms WHERE Name=?', (case,))
        result = cursor.fetchone()
        connection.close()
        return result[0]

    # ------------ A* for solving the white cross ------- #
    
    def heuristic(self, state):
        cube = self.state_to_cube(state)
        # this is in the form of (x1,y1,f2,x2,y2) where (x1,y1) are the coordinates of where the white edtge faces are meant to be on the white face
        # (f2,x2,y2) is the face and coordinates of the adjacent face of the edge piece that has white as well
        # the letter at the end is the colour of the adjacent edge piece
        edges = [
            (0,1,2,2,1,'R'),
            (1,0,1,2,1,'B'),
            (1,2,3,2,1,'G'),
            (2,1,4,2,1,'O')
        ]
        count = 0
        for r1,c1,f2,r2,c2,colour in edges:
            if cube[0][r1,c1] != 'W' or cube[f2][r2,c2] != colour:
                count += 1
        return count
    
    def is_white_cross_solved(self, state):
        cube = self.state_to_cube(state)
        edges = [
            (0,1,2,2,1,'R'),
            (1,0,1,2,1,'B'),
            (1,2,3,2,1,'G'),
            (2,1,4,2,1,'O')
        ]
        for r1,c1,f2,r2,c2,colour in edges:
            if cube[0][r1,c1] != 'W' or cube[f2][r2,c2] != colour:
                return False
        return True
    
    def reconstruct_path(self, came_from, current_state):
        moves = []
        while current_state in came_from:
            current_state, move = came_from[current_state]
            moves.append(move)
        moves.reverse()
        return moves
    
    def solve_white_cross(self, max_depth=8):
        open_set = PriorityQueue()
        closed_set = set()
        came_from = {}
        g_score = {}
        f_score = {}
        counter = itertools.count()
        start_state = self.cube_to_state(self.cube)
        g_score[start_state] = 0
        f_score[start_state] = self.heuristic(start_state)
        open_set.put((f_score[start_state], next(counter), start_state))
        ALL_MOVES = list(self.notation_map.keys())
        while not open_set.empty():
            f, c, current_state = open_set.get()
            if self.is_white_cross_solved(current_state):
                return self.reconstruct_path(came_from, current_state), self.state_to_cube(current_state)
            if current_state in closed_set:
                continue
            closed_set.add(current_state)
            if g_score[current_state] >= max_depth: 
                continue
            last_move = None
            for move in ALL_MOVES:
                if last_move is not None and move == last_move:
                    continue
                new_cube = self.state_to_cube(current_state).copy()
                self.cube = new_cube
                self.apply_move(move)
                next_state = self.cube_to_state(self.cube)
                if next_state in closed_set:
                    continue
                temp_g_score = g_score[current_state] + 1
                if temp_g_score < g_score.get(next_state, float('inf')):
                    came_from[next_state] = (current_state, move)
                    last_move = move
                    g_score[next_state] = temp_g_score
                    f_score[next_state] = temp_g_score + self.heuristic(next_state)
                    open_set.put((f_score[next_state], next(counter), next_state))
        return False
    
    # ------------- Solving F2L ---------------- #
    # --> i need to create methods to detect f2l cases, if not found then use a localised A* to move some pieces to then detect any f2l cases
    
    
    
    # ------------- Solving OLL ---------------- #
    def top_face_mapping(self):
        mapping = ''
        top_face = self.cube[5]
        for i in range(0,3):
            for j in range(0,3):
                if top_face[i,j] == 'Y':
                    mapping += 'Y'
                else:
                    mapping += 'X'
        return mapping
    
    def side_faces_mapping(self):
        mapping = ''
        for i in range(1,5):
            for j in range(0,3):
                if self.cube[i][0,j] == 'Y':
                    mapping += 'Y'
                else:
                    mapping  += 'X'
        return mapping
    '''
    def solve_oll(self):
        connection = sqlite3.connect('speedcubing.db')
        cursor = connection.cursor()
        cursor.execute('SELECT Name FROM Algorithms WHERE CategoryID == 2')
        names = cursor.fetchall()
        states = [item[0] for item in names]
        connection.close()
        for y in range(4):
            for u in range(4):
                state = ''
                state += self.top_face_mapping()
                state += self.side_faces_mapping()
                if state in states:
                    algorithm = self.get_algorithm(state)
                    self.apply_move_sequence(algorithm)
                    return self.cube, ''
                elif np.all(self.cube[5] == 'Y') == True:
                    return self.cube, ''
                self.apply_move('U')
        return self.cube, 'OLL case not recognised.'
        '''
    def solve_oll(self):
            connection = sqlite3.connect('speedcubing.db')
            cursor = connection.cursor()
            cursor.execute('SELECT Name FROM Algorithms WHERE CategoryID == 2')
            names = cursor.fetchall()
            states = [item[0] for item in names]
            connection.close()

            # Try to find a match from all 4 viewing angles (y rotations)
            # This is required because some PDF algorithms (like OLL 29/30) use 'y' moves
            for y_rot in range(4):
                # Try to match the pattern with U alignments
                for u_adj in range(4):
                    state = ''
                    state += self.top_face_mapping()
                    state += self.side_faces_mapping()
                    
                    if state in states:
                        algorithm = self.get_algorithm(state)
                        self.apply_move_sequence(algorithm)
                        return self.cube, ''
                    
                    self.apply_move('U')
                
                # If no match found after 4 U turns, rotate the whole cube and try again
                self.rotate_y()
            
            # Check if it was already solved (all Yellow)
            if np.all(self.cube[5] == 'Y'):
                return self.cube, ''

            return self.cube, 'OLL case not recognised.'
    
    # ------------- Solving PLL ---------------- #
    def read_pll_state(self):
        mappings = {
            self.cube[1][1,1]:'1',
            self.cube[2][1,1]:'2',
            self.cube[3][1,1]:'3',
            self.cube[4][1,1]:'4',
        }
        state = ''
        for i in range(1,5):
            for j in range(0,3):
                state += mappings[self.cube[i][0,j]]
        return state
    
    def solve_pll(self):
        for u in range(4):
            for y in range(4):
                state = self.read_pll_state()
                if state in self.pll_mappings:
                    case = self.pll_mappings[state]
                    algorithm = self.get_algorithm(case)
                    self.apply_move_sequence(algorithm)
                    return self.cube
                self.rotate_y()
            self.apply_move('U')
        return 'PLL case not recognised.'

    
if __name__ == '__main__':
    main = Solver()
    connection = sqlite3.connect('speedcubing.db')
    cursor = connection.cursor()
    cursor.execute('SELECT Notation FROM Algorithms WHERE CategoryID == 2')
    temp_moves = cursor.fetchall()
    moves = [item[0] for item in temp_moves]
    right = []
    wrong = []
    for move in moves:
        main.cube = main.reset()
        main.reorient('R', 'W')
        main.apply_move_sequence(f'{move}')
        cube, stat = main.solve_oll()
        if stat == 'OLL case not recognised.':
            wrong.append(move)
        else:
            right.append(move)
    pp(wrong)
    pp(len(wrong))
    pp(right)
    pp(len(right)) 