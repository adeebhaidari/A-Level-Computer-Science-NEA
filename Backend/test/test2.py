from collections import deque
import time

# Face indices (face * 9 + index)
# Face order: U=0, L=1, F=2, R=3, B=4, D=5
FACE_U, FACE_L, FACE_F, FACE_R, FACE_B, FACE_D = 0, 1, 2, 3, 4, 5

ALL_MOVES = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]

# inverse mapping for pruning
INVERSE = {
    "U": "U'", "U'": "U",
    "D": "D'", "D'": "D",
    "F": "F'", "F'": "F",
    "B": "B'", "B'": "B",
    "L": "L'", "L'": "L",
    "R": "R'", "R'": "R"
}

def face_of_move(m):
    """Return face letter for a move notation (e.g., 'R' or 'R'' -> 'R')"""
    return m[0]

class Cube:
    def __init__(self, state=None):
        if state is None:
            # Solved cube: U=W, L=O, F=G, R=R, B=B, D=Y
            self.state = tuple(
                ['W']*9 +  # U
                ['O']*9 +  # L
                ['G']*9 +  # F
                ['R']*9 +  # R
                ['B']*9 +  # B
                ['Y']*9    # D
            )
        else:
            if len(state) != 54:
                raise ValueError("State must be length 54")
            self.state = tuple(state)

    def clone(self):
        return Cube(self.state)

    def get_state_id(self):
        return self.state  # tuples are hashable

    # --- helpers to convert to face lists for manipulation ---
    def _to_faces(self):
        s = list(self.state)
        return [s[i*9:(i+1)*9] for i in range(6)]

    @staticmethod
    def _faces_to_tuple(faces):
        flat = []
        for f in faces:
            flat.extend(f)
        return tuple(flat)

    # --- face rotation ---
    @staticmethod
    def _rotate_face_cw_inplace(f):
        f[:] = [f[6], f[3], f[0],
                f[7], f[4], f[1],
                f[8], f[5], f[2]]

    @staticmethod
    def _rotate_face_ccw_inplace(f):
        f[:] = [f[2], f[5], f[8],
                f[1], f[4], f[7],
                f[0], f[3], f[6]]

    # --- move implementations ---
    def _do_U(self, faces):
        self._rotate_face_cw_inplace(faces[FACE_U])
        temp = faces[FACE_F][0:3]
        faces[FACE_F][0:3] = faces[FACE_R][0:3]
        faces[FACE_R][0:3] = faces[FACE_B][0:3]
        faces[FACE_B][0:3] = faces[FACE_L][0:3]
        faces[FACE_L][0:3] = temp

    def _do_U_prime(self, faces):
        self._rotate_face_ccw_inplace(faces[FACE_U])
        temp = faces[FACE_F][0:3]
        faces[FACE_F][0:3] = faces[FACE_L][0:3]
        faces[FACE_L][0:3] = faces[FACE_B][0:3]
        faces[FACE_B][0:3] = faces[FACE_R][0:3]
        faces[FACE_R][0:3] = temp

    def _do_D(self, faces):
        self._rotate_face_cw_inplace(faces[FACE_D])
        temp = faces[FACE_F][6:9]
        faces[FACE_F][6:9] = faces[FACE_L][6:9]
        faces[FACE_L][6:9] = faces[FACE_B][6:9]
        faces[FACE_B][6:9] = faces[FACE_R][6:9]
        faces[FACE_R][6:9] = temp

    def _do_D_prime(self, faces):
        self._rotate_face_ccw_inplace(faces[FACE_D])
        temp = faces[FACE_F][6:9]
        faces[FACE_F][6:9] = faces[FACE_R][6:9]
        faces[FACE_R][6:9] = faces[FACE_B][6:9]
        faces[FACE_B][6:9] = faces[FACE_L][6:9]
        faces[FACE_L][6:9] = temp

    def _do_F(self, faces):
        self._rotate_face_cw_inplace(faces[FACE_F])
        temp = faces[FACE_U][6:9]
        faces[FACE_U][6], faces[FACE_U][7], faces[FACE_U][8] = faces[FACE_L][8], faces[FACE_L][5], faces[FACE_L][2]
        faces[FACE_L][2], faces[FACE_L][5], faces[FACE_L][8] = faces[FACE_D][2], faces[FACE_D][1], faces[FACE_D][0]
        faces[FACE_D][0], faces[FACE_D][1], faces[FACE_D][2] = faces[FACE_R][6], faces[FACE_R][3], faces[FACE_R][0]
        faces[FACE_R][0], faces[FACE_R][3], faces[FACE_R][6] = temp[2], temp[1], temp[0]

    def _do_F_prime(self, faces):
        self._rotate_face_ccw_inplace(faces[FACE_F])
        temp = faces[FACE_U][6:9]
        faces[FACE_U][6], faces[FACE_U][7], faces[FACE_U][8] = faces[FACE_R][0], faces[FACE_R][3], faces[FACE_R][6]
        faces[FACE_R][0], faces[FACE_R][3], faces[FACE_R][6] = faces[FACE_D][2], faces[FACE_D][1], faces[FACE_D][0]
        faces[FACE_D][0], faces[FACE_D][1], faces[FACE_D][2] = faces[FACE_L][2], faces[FACE_L][5], faces[FACE_L][8]
        faces[FACE_L][2], faces[FACE_L][5], faces[FACE_L][8] = temp[0], temp[1], temp[2]

    def _do_B(self, faces):
        self._rotate_face_cw_inplace(faces[FACE_B])
        temp = faces[FACE_U][0:3]
        faces[FACE_U][0], faces[FACE_U][1], faces[FACE_U][2] = faces[FACE_R][2], faces[FACE_R][5], faces[FACE_R][8]
        faces[FACE_R][2], faces[FACE_R][5], faces[FACE_R][8] = faces[FACE_D][8], faces[FACE_D][7], faces[FACE_D][6]
        faces[FACE_D][6], faces[FACE_D][7], faces[FACE_D][8] = faces[FACE_L][6], faces[FACE_L][3], faces[FACE_L][0]
        faces[FACE_L][0], faces[FACE_L][3], faces[FACE_L][6] = temp[2], temp[1], temp[0]

    def _do_B_prime(self, faces):
        self._rotate_face_ccw_inplace(faces[FACE_B])
        temp = faces[FACE_U][0:3]
        faces[FACE_U][0], faces[FACE_U][1], faces[FACE_U][2] = faces[FACE_L][6], faces[FACE_L][3], faces[FACE_L][0]
        faces[FACE_L][0], faces[FACE_L][3], faces[FACE_L][6] = faces[FACE_D][6], faces[FACE_D][7], faces[FACE_D][8]
        faces[FACE_D][6], faces[FACE_D][7], faces[FACE_D][8] = faces[FACE_R][8], faces[FACE_R][5], faces[FACE_R][2]
        faces[FACE_R][2], faces[FACE_R][5], faces[FACE_R][8] = temp[0], temp[1], temp[2]

    def _do_R(self, faces):
        self._rotate_face_cw_inplace(faces[FACE_R])
        temp = [faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8]]
        faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8] = faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8]
        faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8] = faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8]
        faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8] = faces[FACE_B][6], faces[FACE_B][3], faces[FACE_B][0]
        faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6] = temp[2], temp[1], temp[0]

    def _do_R_prime(self, faces):
        self._rotate_face_ccw_inplace(faces[FACE_R])
        temp = [faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8]]
        faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8] = faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6]
        faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6] = faces[FACE_D][8], faces[FACE_D][5], faces[FACE_D][2]
        faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8] = faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8]
        faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8] = temp[0], temp[1], temp[2]

    def _do_L(self, faces):
        self._rotate_face_cw_inplace(faces[FACE_L])
        temp = [faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6]]
        faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6] = faces[FACE_B][8], faces[FACE_B][5], faces[FACE_B][2]
        faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8] = faces[FACE_D][6], faces[FACE_D][3], faces[FACE_D][0]
        faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6] = faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6]
        faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6] = temp[0], temp[1], temp[2]

    def _do_L_prime(self, faces):
        self._rotate_face_ccw_inplace(faces[FACE_L])
        temp = [faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6]]
        faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6] = faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6]
        faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6] = faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6]
        faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6] = faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8]
        faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8] = temp[2], temp[1], temp[0]

    # apply move to generate new state
    def apply_move_to_state(self, move):
        faces = self._to_faces()
        getattr(self, f"_do_{move.replace("'", "_prime")}")(faces)
        return self._faces_to_tuple(faces)

    # --- white cross check ---
    def is_white_cross_solved(self):
        faces = self._to_faces()
        U, L, F, R, B = faces[FACE_U], faces[FACE_L], faces[FACE_F], faces[FACE_R], faces[FACE_B]
        # U edge indices: 1,3,5,7
        up_edges = [1,3,5,7]
        for idx in up_edges:
            if U[idx] != 'W':
                return False
        # Check adjacent stickers
        if L[5] != L[4] or F[1] != F[4] or R[3] != R[4] or B[1] != B[4]:
            return False
        return True

    # pretty print for debugging
    def pretty_print(self):
        faces = self._to_faces()
        names = ['U','L','F','R','B','D']
        for i, f in enumerate(faces):
            print(f"{names[i]}: {f[0:3]}\n   {f[3:6]}\n   {f[6:9]}\n")

# BFS solver
def bfs_white_cross_solver(start_cube, max_depth=10, time_limit=60.0):
    start_state = start_cube.get_state_id()
    if start_cube.is_white_cross_solved():
        return []

    q = deque()
    q.append((start_state, []))
    visited = set([start_state])
    start_time = time.time()

    while q:
        if time.time() - start_time > time_limit:
            return None
        state, path = q.popleft()
        if len(path) >= max_depth:
            continue

        for move in ALL_MOVES:
            # pruning rules
            if path:
                last = path[-1]
                if INVERSE[last] == move:
                    continue
                if len(path) >= 2 and face_of_move(path[-1]) == face_of_move(path[-2]) == face_of_move(move):
                    continue

            cube = Cube(state)
            new_state = cube.apply_move_to_state(move)
            if new_state in visited:
                continue
            visited.add(new_state)
            new_path = path + [move]
            if Cube(new_state).is_white_cross_solved():
                return new_path
            q.append((new_state, new_path))
    return None

# --- Example usage ---
if __name__ == "__main__":
    c = Cube()
    scramble = ['F', "R'", 'U', 'B', "L'", 'D', 'F', 'R', 'U', "B'", "L'", 'D', 'F', 'U', "R'", 'B', "L'", 'D', "U'", 'F',
            'R', 'D', "L'", 'B', 'U', "F'", "R'", 'D', 'L' ]

    for m in scramble:
        c = Cube(c.apply_move_to_state(m))

    print("Applied scramble:", scramble)
    c.pretty_print()

    print("Searching for white cross...")
    sol = bfs_white_cross_solver(c, max_depth=15, time_limit=60)
    if sol is None:
        print("No solution found within depth/time limits.")
    else:
        print("Solution (length={}):".format(len(sol)), sol)
        # verify
        test = c.clone()
        for mv in sol:
            test = Cube(test.apply_move_to_state(mv))
        print("After applying solution, cube state:")
        test.pretty_print()
