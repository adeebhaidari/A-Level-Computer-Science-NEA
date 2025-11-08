from heapq import heappush, heappop
import time

# Face indices
FACE_U, FACE_L, FACE_F, FACE_R, FACE_B, FACE_D = 0, 1, 2, 3, 4, 5

# Moves
ALL_MOVES = ['U', "U'", 'D', "D'", 'L', "L'", 'R', "R'", 'F', "F'", 'B', "B'"]
# For Roux 2-blocks, we can optionally skip B/B' if desired. We'll keep them here.
INVERSE = {m: (m[:-1] if m.endswith("'") else m + "'") for m in ALL_MOVES}

def face_of_move(m):
    return m[0]

class Cube:
    def __init__(self, state=None):
        if state is None:
            self.state = tuple(['W']*9 + ['O']*9 + ['G']*9 + ['R']*9 + ['B']*9 + ['Y']*9)
        else:
            self.state = tuple(state)

    def clone(self):
        return Cube(self.state)

    def _to_faces(self):
        s = list(self.state)
        return [list(s[i*9:(i+1)*9]) for i in range(6)]

    @staticmethod
    def _faces_to_tuple(faces):
        return tuple(sum(faces, []))

    # Rotation helpers
    @staticmethod
    def _rotate_face_cw_inplace(faces, fi):
        f = faces[fi]
        faces[fi] = [f[6], f[3], f[0],
                     f[7], f[4], f[1],
                     f[8], f[5], f[2]]

    @staticmethod
    def _rotate_face_ccw_inplace(faces, fi):
        f = faces[fi]
        faces[fi] = [f[2], f[5], f[8],
                     f[1], f[4], f[7],
                     f[0], f[3], f[6]]

    # --- Moves ---
    # Only basic moves; full implementation needed for all moves
    def _do_U(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_U)
        temp = faces[FACE_F][0:3]
        faces[FACE_F][0:3] = faces[FACE_R][0:3]
        faces[FACE_R][0:3] = faces[FACE_B][0:3]
        faces[FACE_B][0:3] = faces[FACE_L][0:3]
        faces[FACE_L][0:3] = temp

    def _do_U_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_U)
        temp = faces[FACE_F][0:3]
        faces[FACE_F][0:3] = faces[FACE_L][0:3]
        faces[FACE_L][0:3] = faces[FACE_B][0:3]
        faces[FACE_B][0:3] = faces[FACE_R][0:3]
        faces[FACE_R][0:3] = temp

    def _do_D(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_D)
        temp = faces[FACE_F][6:9]
        faces[FACE_F][6:9] = faces[FACE_L][6:9]
        faces[FACE_L][6:9] = faces[FACE_B][6:9]
        faces[FACE_B][6:9] = faces[FACE_R][6:9]
        faces[FACE_R][6:9] = temp

    def _do_D_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_D)
        temp = faces[FACE_F][6:9]
        faces[FACE_F][6:9] = faces[FACE_R][6:9]
        faces[FACE_R][6:9] = faces[FACE_B][6:9]
        faces[FACE_B][6:9] = faces[FACE_L][6:9]
        faces[FACE_L][6:9] = temp

    def _do_L(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_L)
        temp = [faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6]]
        faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6] = faces[FACE_B][8], faces[FACE_B][5], faces[FACE_B][2]
        faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8] = faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6]
        faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6] = faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6]
        faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6] = temp[0], temp[1], temp[2]

    def _do_L_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_L)
        temp = [faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6]]
        faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6] = faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6]
        faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6] = faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6]
        faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6] = faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8]
        faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8] = temp[2], temp[1], temp[0]

    def _do_R(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_R)
        temp = [faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8]]
        faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8] = faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8]
        faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8] = faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8]
        faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8] = faces[FACE_B][6], faces[FACE_B][3], faces[FACE_B][0]
        faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6] = temp[0], temp[1], temp[2]

    def _do_R_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_R)
        temp = [faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8]]
        faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8] = faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6]
        faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6] = faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8]
        faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8] = faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8]
        faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8] = temp[0], temp[1], temp[2]

    # Apply a move
    def apply_move_to_state(self, move):
        faces = self._to_faces()
        method_name = "_do_" + move.replace("'", "_prime")
        getattr(self, method_name)(faces)
        return self._faces_to_tuple(faces)

    # --- Roux 2-block check ---
    def is_2block_solved(self):
        faces = self._to_faces()
        # Left block positions
        left = [
            (FACE_L,0),(FACE_L,1),(FACE_L,2),
            (FACE_F,0),(FACE_F,3),(FACE_F,6),
            (FACE_D,0),(FACE_D,1),(FACE_D,2)
        ]
        # Right block positions
        right = [
            (FACE_R,0),(FACE_R,1),(FACE_R,2),
            (FACE_F,2),(FACE_F,5),(FACE_F,8),
            (FACE_D,6),(FACE_D,7),(FACE_D,8)
        ]
        # Check left block
        for f, i in left:
            if faces[f][i] != faces[f][4]:
                return False
        # Check right block
        for f, i in right:
            if faces[f][i] != faces[f][4]:
                return False
        return True

# --- Heuristic ---
def two_block_heuristic(cube):
    faces = cube._to_faces()
    h = 0
    left = [
        (FACE_L,0),(FACE_L,1),(FACE_L,2),
        (FACE_F,0),(FACE_F,3),(FACE_F,6),
        (FACE_D,0),(FACE_D,1),(FACE_D,2)
    ]
    right = [
        (FACE_R,0),(FACE_R,1),(FACE_R,2),
        (FACE_F,2),(FACE_F,5),(FACE_F,8),
        (FACE_D,6),(FACE_D,7),(FACE_D,8)
    ]
    for f,i in left+right:
        if faces[f][i] != faces[f][4]:
            h += 1
    return h

# --- A* solver ---
def astar_2block_solver(start_cube, max_depth=20, time_limit=30.0):
    start_state = start_cube.state
    heap = []
    heappush(heap, (two_block_heuristic(start_cube), 0, start_state, []))
    visited = set([start_state])
    start_time = time.time()

    while heap:
        if time.time() - start_time > time_limit:
            return None

        f, g, state, path = heappop(heap)
        if g > max_depth:
            continue

        cube = Cube(state)
        if cube.is_2block_solved():
            return path

        for move in ALL_MOVES:
            # Pruning rules
            if path:
                last = path[-1]
                if INVERSE[last] == move:
                    continue
                if len(path) >= 2 and face_of_move(path[-1]) == face_of_move(path[-2]) == face_of_move(move):
                    continue

            new_state = cube.apply_move_to_state(move)
            if new_state in visited:
                continue
            visited.add(new_state)
            new_path = path + [move]
            h = two_block_heuristic(Cube(new_state))
            heappush(heap, (g+1+h, g+1, new_state, new_path))
    return None

# --- Example usage ---
if __name__ == "__main__":
    c = Cube()
    # Sample scramble
    scramble = ['F', 'R', 'U', "L'", 'D', 'F', "R'", 'U', "L'", 'D']
    for m in scramble:
        c = Cube(c.apply_move_to_state(m))

    print("Applied scramble:", scramble)
    print("Cube state after scramble:")
    faces = c._to_faces()
    names = ['U','L','F','R','B','D']
    for idx, f in enumerate(faces):
        print(f"{names[idx]}: {f[0:3]}\n   {f[3:6]}\n   {f[6:9]}\n")

    print("Searching for Roux 2-blocks solution...")
    sol = astar_2block_solver(c, max_depth=15, time_limit=30)
    if sol:
        print(f"Solution (length={len(sol)}): {sol}")
        test = Cube(c.state)
        for mv in sol:
            test = Cube(test.apply_move_to_state(mv))
        print("After applying solution:")
        faces = test._to_faces()
        for idx, f in enumerate(faces):
            print(f"{names[idx]}: {f[0:3]}\n   {f[3:6]}\n   {f[6:9]}\n")
    else:
        print("No solution found within depth/time limits.")