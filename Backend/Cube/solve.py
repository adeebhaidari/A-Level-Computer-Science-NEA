from queue import PriorityQueue
import main_cube
import itertools
import numpy as np
from pprint import pprint as pp

class Solver(main_cube.Cube):
    def __init__(self):
        super().__init__()
    
    # --------- helper functions  ------------- #
    
    def cube_to_state(self, cube):
        return tuple(tuple(tuple(row) for row in face) for face in cube)
    
    def state_to_cube(self, state):
        return np.array(state, dtype=object)
    
    # -------- cube state validation  ------------- #
    
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
    
    # ------------- Solving PLL ---------------- #

main = Solver()
pp(main.scramble())
pp(main.cube)
print()
pp(main.solve_white_cross())