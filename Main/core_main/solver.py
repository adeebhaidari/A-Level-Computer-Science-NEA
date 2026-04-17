import sys
import os

current_directory = os.path.dirname(os.path.abspath(__file__))
parent_directory = os.path.dirname(current_directory)
sys.path.append(parent_directory)

from queue import PriorityQueue
from core_main import cube_logic
import itertools
import numpy as np
import sqlite3
from database import algorithm_data
from abc import ABC, abstractmethod
import kociemba


class BaseSolver(ABC, cube_logic.Cube):
    @abstractmethod
    def solve(self):
        pass   

class CFOP(BaseSolver):
    def __init__(self):
        super().__init__()
        self.pll_mappings = algorithm_data.pll_mappings
        
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

    def get_inverse_move(self, move):
        inverse_mapping = {
            'R': 'R"',
            'R"': 'R',
            'R2': 'R2',
            'L': 'L"',
            'L"': 'L',
            'L2': 'L2',
            'U': 'U"',
            'U"': 'U',
            'U2': 'U2',
            'D': 'D"',
            'D"': 'D',
            'D2': 'D2',
            'F': 'F"',
            'F"': 'F',
            'F2': 'F2',
            'B': 'B"',
            'B"': 'B',
            'B2': 'B2',
            'y': 'y"',
            'y"': 'y',
            'y2': 'y2',
            'x': 'x"',
            'x"': 'x',
            'x2': 'x2',
            'z': 'z"',
            'z"': 'z',
            'z2': 'z2'
        }
        
        return inverse_mapping[move]
    
    def optimise_moves(self, moves):
        if not moves: return []
        
        sequence_sets = [
            [['R', 'U', 'R"', 'U"'], ['U', 'R', 'U"', 'R"']],
            [['L"', 'U"', 'L', 'U'], ['U"', 'L"', 'U', 'L']],
            [['U', 'R', 'U"', 'R"'], ['R', 'U', 'R"', 'U"']],
            [['U"', 'L"', 'U', 'L'], ['L"', 'U"', 'L', 'U']]
        ]
        
        rotations_sets = [
            [['y', 'y', 'y'], ['y"']],
            [['U', 'U', 'U'], ['U"']],
            [['U"', 'U"', 'U"'], ['U']],
            [['U"', 'U"', 'U"','U"'], []],
            [['U', 'U', 'U', 'U'], []]
        ]
                        
        for sequence in sequence_sets:
            for i in reversed(range(4,6)):
                for j in range(len(moves) - len(sequence[0]) + 1):
                    if moves[j:j+(4*i)] == sequence[0]*i:
                        moves[j:j+(4*i)] = sequence[1]*(6-i)
        
        for rotations in rotations_sets:
            size = len(rotations)
            for j in range(len(moves) - size + 1):
                if moves[j:j+(size) + 1] == rotations[0]:
                    moves[j:j+(size) + 1] = rotations[1]
        
        moves = [m.replace('"', "'") for m in moves]
        
        optimised = True
        while optimised:
            optimised = False
            new_moves = []
            i = 0
            while i < len(moves):
                current_move = moves[i]
                
                if i + 1 < len(moves) and moves[i+1][0] == current_move[0]:
                    face = current_move[0]
                    
                    def get_val(m):
                        if len(m) == 1: return 1
                        if '2' in m: return 2
                        if "'" in m: return 3
                        return 0

                    total_rotation = (get_val(current_move) + get_val(moves[i+1])) % 4
                    
                    combined = None
                    if total_rotation == 1: combined = face
                    elif total_rotation == 2: combined = face + "2"
                    elif total_rotation == 3: combined = face + "'"
                    
                    if combined:
                        new_moves.append(combined)
                    
                    i += 2
                    optimised = True
                else:
                    new_moves.append(current_move)
                    i += 1
            moves = new_moves
        
        return [m.replace("'", '"') for m in moves]

    # ------------ A* for solving the white cross ------- #
    
    def heuristic(self, state):
        cube = self.state_to_cube(state)
        # this is in the form of (x1,y1,f2,x2,y2) where (x1,y1) are the coordinates of where the white edge faces are meant to be on the white face
        # (f2,x2,y2) is the face and coordinates of the adjacent face of the edge piece that has white as well
        # the letter at the end is the colour of the adjacent edge piece
        # f(n) = g(n) + h(n)
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
    
    # describe this lightly with comments
    # describe most of this in documentation
    # add white space !!!
    # clean up the code...
    def solve_white_cross(self, max_depth=12):
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
        
        ALL_MOVES = ['R', 'R"', 'R2', 'L', 'L"', 'L2', 'U', 'U"', 'U2', 'D', 'D"', 'D2', 'F', 'F"', 'F2', 'B', 'B"', 'B2']
        
        while not open_set.empty():
            f, c, current_state = open_set.get()
            
            last_move = came_from[current_state][1] if current_state in came_from else None
            
            if self.is_white_cross_solved(current_state):
                self.cube = self.state_to_cube(current_state)
                return self.reconstruct_path(came_from, current_state), self.state_to_cube(current_state)
            
            if current_state in closed_set:
                continue
            
            closed_set.add(current_state)
            
            if g_score[current_state] >= max_depth: 
                continue
            
            last_move = None
            
            for move in ALL_MOVES:
                if last_move == self.get_inverse_move(move):
                    continue
                
                #if last_move is not None and move == last_move:
                #    continue
                
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
    # use beginner method to solve f2l, corners first then edges. possiby use a localised A star to change the state s;lightly so a corner piece canbe found in the right position to ten insert into the correct corner position
    
    def find_corner(self, colours):
        # these are the physical corner locations
        # each tuple is (face, row, column)
        corners = [
            # bottom layer corners
            {(0, 2, 0), (1, 2, 0), (4, 2, 2)},
            {(0, 2, 2), (3, 2, 2), (4, 2, 0)},
            {(0, 0, 0), (1, 2, 2), (2, 2, 0)},
            {(0, 0, 2), (2, 2, 2), (3, 2, 0)},
            
            # top layer corners
            {(5, 0, 0), (1, 0, 0), (4, 0, 2)},
            {(5, 0, 2), (3, 0, 2), (4, 0, 0)},
            {(5, 2, 0), (1, 0, 2), (2, 0, 0)},
            {(5, 2, 2), (2, 0, 2), (3, 0, 0)}
        ]
        
        for corner_coords in corners:
            # this gets the colours at the current cooridinate location
            current_colours = {self.cube[f][r, c] for f, r, c in corner_coords}
            if current_colours == colours:
                return list(corner_coords)
        return None

    def find_edge(self, colours):
        # colours is a set like {'R', 'G'} for example
        # these are in the form (face, row, column) as well
        edges = [
            [(1,1,0), (4,1,2)], [(1,1,2), (2,1,0)], [(2,1,2), (3,1,0)], [(3,1,2), (4,1,0)], # Middle
            [(0,0,1), (4,2,1)], [(0,1,0), (1,2,1)], [(0,1,2), (3,2,1)], [(0,2,1), (2,2,1)], # Bottom
            [(5,0,1), (4,0,1)], [(5,1,0), (1,0,1)], [(5,1,2), (3,0,1)], [(5,2,1), (2,0,1)]  # Top
        ]
        for edge in edges:
            current_colours = {self.cube[f][r,c] for f,r,c in edge}
            if current_colours == colours:
                return edge
        return None
    
    def solve_white_corners(self):
        corner_slots = [('R', 'G'), ('G', 'O'), ('O', 'B'), ('B', 'R')]
        all_corner_moves = []

        for c1, c2 in corner_slots:
            # this aligns the front face so that the front center is the same colour as c1
            while self.cube[2][1,1] != c1:
                self.apply_move('y')
                all_corner_moves.append('y')
            
            timeout = 0
            # this identifies the target of white on bottom face - index 0, front right being (0,0,2), front face - index 2 is c1, and right face - index 3 - is c2
            while not (self.cube[0][0,2] == 'W' and self.cube[2][2,2] == c1 and self.cube[3][2,0] == c2):
                if timeout > 30: 
                    print(f'Timeout solving corner {c1}-{c2}')
                    break
                
                target_colours = {'W', c1, c2}
                current_pos = self.find_corner(target_colours)
                
                if current_pos is None:
                    print(f'Error: Corner {target_colours} not found!')
                    break

                # this checks if the target piece is on the top layer
                in_top = any(p[0] == 5 for p in current_pos)

                if not in_top:
                    # this means the piece is on the bottom layer
                    is_in_current_slot = any(p == (0,0,2) for p in current_pos)
                    
                    if is_in_current_slot:
                        # this deals with the problem whejn the piece is in the right slot but it isnt oriented
                        self.apply_move_sequence('R U R" U"')
                        all_corner_moves.extend(['R', 'U', 'R"', 'U"'])
                    else:
                        # if its in a different target slot, this will rotate 'y' until it is in the front right slot to then be inserted into its correct position after
                        # Rotate 'y' until it is in the front-right slot (0,0,2)
                        while not any(p == (0,0,2) for p in self.find_corner(target_colours)):
                            self.apply_move('y')
                            all_corner_moves.append('y')
                            
                        self.apply_move_sequence('R U R" U"')
                        all_corner_moves.extend(['R', 'U', 'R"', 'U"'])
                        
                        # this then restores the correct reorientation for the given target slot
                        while self.cube[2][1,1] != c1:
                            self.apply_move('y')
                            all_corner_moves.append('y')
                    
                    timeout += 1
                    continue

                # now that the piece is in the top layer, we need to move it until it is right above the target slot
                current_pos = self.find_corner(target_colours)
                if not any(p == (5,2,2) for p in current_pos):
                    self.apply_move("U")
                    all_corner_moves.append("U")
                    continue

                # this just inserts the corner into its correct position
                self.apply_move_sequence('R U R" U"')
                all_corner_moves.extend(['R', 'U', 'R"', 'U"'])
                timeout += 1

        # optimised_moves = self.optimise_moves(all_corner_moves)
        optimised_moves = all_corner_moves
        return optimised_moves, self.cube
    
    def solve_f2l_edges(self):
        all_edge_moves = []
        # this is just a helper to check if the middle layer is fully solved
        def is_f2l_solved():
            for f in range(1, 5):
                # this checks if the left and right edges match the center colour
                if self.cube[f][1, 0] != self.cube[f][1, 1] or self.cube[f][1, 2] != self.cube[f][1, 1]:
                    return False
            return True

        timeout = 0
        while not is_f2l_solved() and timeout < 100:
            timeout += 1
            
            # this looks for a non-yellow edge currently sitting on the top layer
            top_edges = [
                ((5, 2, 1), (2, 0, 1)),
                ((5, 1, 2), (3, 0, 1)),
                ((5, 0, 1), (4, 0, 1)),
                ((5, 1, 0), (1, 0, 1))
            ]
            
            found_non_yellow = False
            
            for top_coord, side_coord in top_edges:
                top_colour = self.cube[top_coord[0]][top_coord[1], top_coord[2]]
                side_colour = self.cube[side_coord[0]][side_coord[1], side_coord[2]]
                
                # this indicates that an f2l piece has been found
                if top_colour != 'Y' and side_colour != 'Y':
                    found_non_yellow = True
                    
                    # this rotates the entire cube using 'y' until the side colour matches the front center colour
                    while self.cube[2][1, 1] != side_colour:
                        self.apply_move('y')
                        all_edge_moves.append('y')
                    
                    # his rotates the top layer using 'U' until that specific piece is at the front top position
                    while self.cube[2][0, 1] != side_colour or self.cube[5][2, 1] != top_colour:
                        self.apply_move('U')
                        all_edge_moves.append('U')
                        
                    # this section now inserts the piece
                    # it checks if the top colour matches the right center or the left center
                    if top_colour == self.cube[3][1, 1]:
                        seq = 'U R U" R" U" F" U F'
                    else:
                        seq = 'U" L" U L U F U" F"'
                        
                    self.apply_move_sequence(seq)
                    all_edge_moves.extend(seq.split())
                    break

            # if no non yellow pieces are on the top an F2L piece is either stuck or flipped in the middle layer
            if not found_non_yellow:
                # this rotates the cube and looks at the front right slot
                for _ in range(4):
                    front_sticker = self.cube[2][1, 2]
                    right_sticker = self.cube[3][1, 0]
                    front_center = self.cube[2][1, 1]
                    right_center = self.cube[3][1, 1]
                    
                    # this checks if the currenr slot is incorrect
                    if front_sticker != front_center or right_sticker != right_center:
                        
                        # this moves it out from its current position to the top layer
                        seq = 'U R U" R" U" F" U F'
                        self.apply_move_sequence(seq)
                        all_edge_moves.extend(seq.split())
                        
                        break
                    else:
                        # this means the slot is fine and will rotate to look at the next slot
                        self.apply_move('y')
                        all_edge_moves.append('y')
        
        # optimised_moves = self.optimise_moves(all_edge_moves)               
        optimised_moves = all_edge_moves
        return optimised_moves, self.cube
    
    
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
    
    def solve_oll(self):
        if np.all(self.cube[5] == 'Y'):
            return [], self.cube
        
        connection = sqlite3.connect('speedcubing.db')
        cursor = connection.cursor()
        cursor.execute('''
            SELECT Name FROM Algorithms 
            WHERE CategoryID == 1
        ''')
        
        names = cursor.fetchall()
        states = [item[0] for item in names]
        connection.close()
        
        for y_rot in range(4):
            for u_adj in range(4):
                state = ''
                state += self.top_face_mapping()
                state += self.side_faces_mapping()
                
                if state in states:
                    algorithm = self.get_algorithm(state)
                    self.apply_move_sequence(algorithm)
                    
                    setup_moves = []
                    if y_rot > 0:
                        setup_moves.extend(['y '] * y_rot)
                    if u_adj > 0:
                        setup_moves.extend(['U '] * u_adj)
                        
                    setup_str = ''.join(setup_moves)
                    full_algorithm = f'{setup_str} {algorithm}'.strip()
                    
                    return full_algorithm.split(), self.cube
                
                self.apply_move('U')
            self.rotate_y()

        return ['OLL error...'], self.cube
    
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
        is_pll_solved = True
        for face in range(1, 5):
            if not np.all(self.cube[face][0, :] == self.cube[face][1,1]):
                is_pll_solved = False
                break
            last_moves = []
            for u in range(3):
                if self.cube[1][0,1] == self.cube[1][1,1] and self.cube[3][0,1] == self.cube[3][1,1]:
                    return last_moves, self.cube
                self.apply_move('U')
                last_moves.append('U')
            
        if is_pll_solved:
            return [], self.cube
        
        for y in range(4):
            for u in range(4):
                state = self.read_pll_state()
                
                if state in self.pll_mappings:
                    case = self.pll_mappings[state]
                    algorithm = self.get_algorithm(case)
                    self.apply_move_sequence(algorithm)
                    
                    setup_moves = []
                    if u > 0:
                        setup_moves.extend(['U '] * u)
                    if y > 0:
                        setup_moves.extend(['y '] * y)
                    
                    setup_str = ''.join(setup_moves)
                    full_algorithm = f'{setup_str} {algorithm}'.strip()
                    
                    return full_algorithm.split(), self.cube
                
                self.apply_move('U')
            self.rotate_y()
        return ['PLL error...'], self.cube
    
    def pruned_full_solution(self, state = None):
        full_solution = []
            
        step_order = [
            self.solve_white_cross,
            self.solve_white_corners,
            self.solve_f2l_edges,
            self.solve_oll,
            self.solve_pll
        ]
        
        for step in step_order:
            solution = step()
            if not solution or (solution and 'error' in solution[0]):
                print(f'Solver aborted at {step.__name__}')
                return ['Error']
            
            if solution and solution[0]:
                full_solution.extend(solution[0])
        
        optimised_solution = self.optimise_moves(full_solution)
        
        return optimised_solution
    
    def solve(self, state = None):
        if self.is_solved():
            return ['All ready solved']
        return self.pruned_full_solution()

class Kociemba(BaseSolver):
    def convert_to_string(self, cube_state):
        face_order = [5, 3, 2, 0, 1, 4]
        state_str = ''
        colour_to_letter = {
            'Y': 'U',
            'G': 'R',
            'R': 'F',
            'W': 'D',
            'B': 'L',
            'O': 'B'
        }
        
        for index in face_order:
            face = cube_state[index]
            for row in range(3):
                for col in range(3):
                    colour = face[row, col]
                    state_str += colour_to_letter[colour]
        
        return state_str
    
    def solve(self, state=None):
        if self.is_solved():
            return ['All ready solved']
        
        self.reorient('R', 'W')
        
        state_string = self.convert_to_string(self.cube)
        try:
            solution_str = kociemba.solve(state_string)
            
            if not solution_str:
                return ['All ready solved']
            self.apply_move_sequence(solution_str)
            
            solution = solution_str.split()
            return solution
        except Exception as e:
            print(f'Kociemba error: {e}')
            return ['Error']