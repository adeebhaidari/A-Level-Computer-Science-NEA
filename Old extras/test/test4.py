from heapq import heappush, heappop
import time

# Face indices
FACE_U, FACE_L, FACE_F, FACE_R, FACE_B, FACE_D = 0, 1, 2, 3, 4, 5
ALL_MOVES = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]
INVERSE = {m: (m[:-1] if m.endswith("'") else m + "'") for m in ALL_MOVES}

def face_of_move(m):
    return m[0]

class Cube:
    def __init__(self, state=None):
        if state is None:
            self.state = tuple(['W']*9 + ['O']*9 + ['G']*9 + ['R']*9 + ['B']*9 + ['Y']*9)
        else:
            self.state = tuple(state)

    def _to_faces(self):
        s = list(self.state)
        return [list(s[i*9:(i+1)*9]) for i in range(6)]

    @staticmethod
    def _faces_to_tuple(faces):
        return tuple(sum(faces, []))

    @staticmethod
    def _rotate_face_cw_inplace(faces, fi):
        f = faces[fi]
        faces[fi] = [f[6], f[3], f[0], f[7], f[4], f[1], f[8], f[5], f[2]]

    @staticmethod
    def _rotate_face_ccw_inplace(faces, fi):
        f = faces[fi]
        faces[fi] = [f[2], f[5], f[8], f[1], f[4], f[7], f[0], f[3], f[6]]
    
    def get_state_id(self):
        return self.state


    # --- Moves ---
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

    def _do_F(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_F)
        temp = [faces[FACE_U][6], faces[FACE_U][7], faces[FACE_U][8]]
        faces[FACE_U][6], faces[FACE_U][7], faces[FACE_U][8] = faces[FACE_L][8], faces[FACE_L][5], faces[FACE_L][2]
        faces[FACE_L][2], faces[FACE_L][5], faces[FACE_L][8] = faces[FACE_D][2], faces[FACE_D][1], faces[FACE_D][0]
        faces[FACE_D][0], faces[FACE_D][1], faces[FACE_D][2] = faces[FACE_R][6], faces[FACE_R][3], faces[FACE_R][0]
        faces[FACE_R][0], faces[FACE_R][3], faces[FACE_R][6] = temp[2], temp[1], temp[0]

    def _do_F_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_F)
        temp = [faces[FACE_U][6], faces[FACE_U][7], faces[FACE_U][8]]
        faces[FACE_U][6], faces[FACE_U][7], faces[FACE_U][8] = faces[FACE_R][0], faces[FACE_R][3], faces[FACE_R][6]
        faces[FACE_R][0], faces[FACE_R][3], faces[FACE_R][6] = faces[FACE_D][2], faces[FACE_D][1], faces[FACE_D][0]
        faces[FACE_D][0], faces[FACE_D][1], faces[FACE_D][2] = faces[FACE_L][2], faces[FACE_L][5], faces[FACE_L][8]
        faces[FACE_L][2], faces[FACE_L][5], faces[FACE_L][8] = temp[0], temp[1], temp[2]

    def _do_B(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_B)
        temp = [faces[FACE_U][0], faces[FACE_U][1], faces[FACE_U][2]]
        faces[FACE_U][0], faces[FACE_U][1], faces[FACE_U][2] = faces[FACE_R][2], faces[FACE_R][5], faces[FACE_R][8]
        faces[FACE_R][2], faces[FACE_R][5], faces[FACE_R][8] = faces[FACE_D][8], faces[FACE_D][7], faces[FACE_D][6]
        faces[FACE_D][6], faces[FACE_D][7], faces[FACE_D][8] = faces[FACE_L][6], faces[FACE_L][3], faces[FACE_L][0]
        faces[FACE_L][0], faces[FACE_L][3], faces[FACE_L][6] = temp[2], temp[1], temp[0]

    def _do_B_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_B)
        temp = [faces[FACE_U][0], faces[FACE_U][1], faces[FACE_U][2]]
        faces[FACE_U][0], faces[FACE_U][1], faces[FACE_U][2] = faces[FACE_L][6], faces[FACE_L][3], faces[FACE_L][0]
        faces[FACE_L][0], faces[FACE_L][3], faces[FACE_L][6] = faces[FACE_D][6], faces[FACE_D][7], faces[FACE_D][8]
        faces[FACE_D][6], faces[FACE_D][7], faces[FACE_D][8] = faces[FACE_R][8], faces[FACE_R][5], faces[FACE_R][2]
        faces[FACE_R][2], faces[FACE_R][5], faces[FACE_R][8] = temp[0], temp[1], temp[2]

    def _do_R(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_R)
        temp = [faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8]]
        faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8] = faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8]
        faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8] = faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8]
        faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8] = faces[FACE_B][6], faces[FACE_B][3], faces[FACE_B][0]
        faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6] = temp[2], temp[1], temp[0]

    def _do_R_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_R)
        temp = [faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8]]
        faces[FACE_U][2], faces[FACE_U][5], faces[FACE_U][8] = faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6]
        faces[FACE_B][0], faces[FACE_B][3], faces[FACE_B][6] = faces[FACE_D][8], faces[FACE_D][5], faces[FACE_D][2]
        faces[FACE_D][2], faces[FACE_D][5], faces[FACE_D][8] = faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8]
        faces[FACE_F][2], faces[FACE_F][5], faces[FACE_F][8] = temp[0], temp[1], temp[2]

    def _do_L(self, faces):
        self._rotate_face_cw_inplace(faces, FACE_L)
        temp = [faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6]]
        faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6] = faces[FACE_B][8], faces[FACE_B][5], faces[FACE_B][2]
        faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8] = faces[FACE_D][6], faces[FACE_D][3], faces[FACE_D][0]
        faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6] = faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6]
        faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6] = temp[0], temp[1], temp[2]

    def _do_L_prime(self, faces):
        self._rotate_face_ccw_inplace(faces, FACE_L)
        temp = [faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6]]
        faces[FACE_U][0], faces[FACE_U][3], faces[FACE_U][6] = faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6]
        faces[FACE_F][0], faces[FACE_F][3], faces[FACE_F][6] = faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6]
        faces[FACE_D][0], faces[FACE_D][3], faces[FACE_D][6] = faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8]
        faces[FACE_B][2], faces[FACE_B][5], faces[FACE_B][8] = temp[2], temp[1], temp[0]

    # Apply move
    def apply_move_to_state(self, move):
        faces = self._to_faces()
        getattr(self, "_do_" + move.replace("'", "_prime"))(faces)
        return self._faces_to_tuple(faces)

    # Check white cross solved
    def is_white_cross_solved(self):
        up_edges = [1, 3, 5, 7]
        neighbor_mapping = {1:(FACE_B,1),3:(FACE_L,5),5:(FACE_R,3),7:(FACE_F,1)}
        faces = self._to_faces()
        for idx in up_edges:
            if faces[FACE_U][idx] != 'W':
                return False
        for u_idx, (f_idx, f_edge_idx) in neighbor_mapping.items():
            if faces[f_idx][f_edge_idx] != faces[f_idx][4]:
                return False
        return True

    def pretty_print(self):
        faces = [list(self.state[i*9:(i+1)*9]) for i in range(6)]
        names = ['U','L','F','R','B','D']
        for idx, f in enumerate(faces):
            print(f"{names[idx]}: {f[0:3]}\n   {f[3:6]}\n   {f[6:9]}\n")

# --- Dijkstra solver ---
def dijkstra_white_cross_solver(start_cube, max_depth=20, time_limit=30.0):
    start_state = start_cube.get_state_id()
    heap = []
    heappush(heap, (0, start_state, []))  # priority = g (number of moves so far)
    visited = set([start_state])
    start_time = time.time()

    while heap:
        if time.time() - start_time > time_limit:
            return None

        g, state, path = heappop(heap)
        if g > max_depth:
            continue

        cube = Cube(state)
        if cube.is_white_cross_solved():
            return path

        for move in ALL_MOVES:
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
            heappush(heap, (g+1, new_state, new_path))  # priority = g only
    return None

# --- Usage Example ---
if __name__ == "__main__":
    c = Cube()
    scramble = ['F', "R'", 'U', 'B', "L'", 'D', 'F', 'R', 'U', "B'", "L'", 'D','F', 'U', "R'", 'B', "L'", 'D', "F'", 'R', 'U', "L'", 'B', 'D', 'F', "R'", "U'", "B'", "L'", 'D']

    for m in scramble:
        c = Cube(c.apply_move_to_state(m))

    print("Applied scramble:", scramble)
    c.pretty_print()

    print("Searching for white cross (Dijkstra)...")
    sol = dijkstra_white_cross_solver(c, max_depth=25, time_limit=60.0)
    if sol:
        print(f"Solution (length={len(sol)}): {sol}")
        test = Cube(c.state)
        for mv in sol:
            test = Cube(test.apply_move_to_state(mv))
        print("After applying solution:")
        test.pretty_print()
    else:
        print("No solution found within depth/time limits.")
