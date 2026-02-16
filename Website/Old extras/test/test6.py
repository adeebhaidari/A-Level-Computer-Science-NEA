# ida_white_cross.py
# IDA* solver for the Rubik-style "white cross" subgoal.
# Paste into your project — uses the same Cube/move semantics as before.

from heapq import heappush, heappop
import time

# Face indices
FACE_U, FACE_L, FACE_F, FACE_R, FACE_B, FACE_D = 0, 1, 2, 3, 4, 5
ALL_MOVES = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]
INVERSE = {m: (m[:-1] if m.endswith("'") else m + "'") for m in ALL_MOVES}

def face_of_move(m):
    return m[0]

# -------------------------
# Cube class (same semantics as your original; kept explicit for clarity)
# -------------------------
class Cube:
    def __init__(self, state=None):
        if state is None:
            # solved state: U=White, L=Orange, F=Green, R=Red, B=Blue, D=Yellow
            self.state = tuple(['W']*9 + ['O']*9 + ['G']*9 + ['R']*9 + ['B']*9 + ['Y']*9)
        else:
            self.state = tuple(state)

    def clone(self):
        return Cube(self.state)

    def get_state_id(self):
        return self.state

    def _to_faces(self):
        s = list(self.state)
        return [list(s[i*9:(i+1)*9]) for i in range(6)]

    @staticmethod
    def _faces_to_tuple(faces):
        return tuple(sum(faces, []))

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

    # Moves (matching your earlier implementation)
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

    def apply_move_to_state(self, move):
        faces = self._to_faces()
        method_name = "_do_" + move.replace("'", "_prime")
        getattr(self, method_name)(faces)
        return self._faces_to_tuple(faces)

    # Check white cross solved
    def is_white_cross_solved(self):
        up_edges = [1, 3, 5, 7]
        # neighbor_mapping maps the U-edge position -> (face index, face edge index)
        neighbor_mapping = {1: (FACE_B,1), 3: (FACE_L,5), 5: (FACE_R,3), 7: (FACE_F,1)}
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

# -------------------------
# Heuristic: improved but admissible for white-cross subgoal
# - For each of the 4 target edges we check if the edge is already correct
# - heuristic = number of edges that are not already fully correct
# This is admissible (each not-fully-correct edge needs at least one move).
# -------------------------
TARGET_UP_EDGE_POSITIONS = {
    # u_idx : (neighbor_face_index, neighbor_face_edge_index)
    1: (FACE_B, 1),
    3: (FACE_L, 5),
    5: (FACE_R, 3),
    7: (FACE_F, 1)
}

def white_cross_heuristic(cube):
    faces = cube._to_faces()
    h = 0
    for u_idx, (f_idx, f_edge_idx) in TARGET_UP_EDGE_POSITIONS.items():
        if faces[FACE_U][u_idx] != 'W':
            h += 1
        else:
            # up sticker is white — check the adjacent sticker color against center
            if faces[f_idx][f_edge_idx] != faces[f_idx][4]:
                h += 1
    # Note: an edge that has both wrong up-sticker and wrong adjacent color counts 1 or 2.
    # To be strictly admissible we'd want to avoid overestimate: cap each edge at 1.
    # Above we might count 2 for the same edge; to ensure admissible, cap per edge at 1:
    # (Let's implement the cap to be safe.)
    # We'll recompute with cap:
    h = 0
    for u_idx, (f_idx, f_edge_idx) in TARGET_UP_EDGE_POSITIONS.items():
        bad = 0
        if faces[FACE_U][u_idx] != 'W':
            bad = 1
        else:
            if faces[f_idx][f_edge_idx] != faces[f_idx][4]:
                bad = 1
        h += bad
    return h

# -------------------------
# IDA* solver with improvements:
# - iterative deepening on f = g + h
# - dynamic move ordering by heuristic of successor states (best-first among children)
# - small transposition table mapping state -> best g seen (prunes worse visits)
# - path-state set to avoid cycles
# -------------------------
def ida_star_white_cross_solver(start_cube, max_depth=50, time_limit=30.0):
    start_time = time.time()
    start_state = start_cube.get_state_id()
    if start_cube.is_white_cross_solved():
        return []

    # initial threshold = h(start)
    threshold = white_cross_heuristic(start_cube)

    # transposition table to prune: state_id -> best g seen so far along any path
    transposition = {}

    # helper: generate successor states with quick heuristic ordering
    def ordered_successors(state):
        cube = Cube(state)
        succ = []
        for move in ALL_MOVES:
            new_state = cube.apply_move_to_state(move)
            # quick heuristic on the successor
            h = white_cross_heuristic(Cube(new_state))
            succ.append((h, move, new_state))
        # sort by (h, prefer moves affecting U first) ascending -> smaller h first
        # small tie-break: prefer moves on faces that commonly help (U, F, R, L)
        face_priority = {'U':0, 'F':1, 'R':2, 'L':2, 'B':3, 'D':4}
        succ.sort(key=lambda x: (x[0], face_priority.get(face_of_move(x[1]), 10)))
        return succ

    # DFS limited by f <= threshold
    def dfs(state, g, threshold, path, path_state_set, prev_move):
        # timeout check
        if time.time() - start_time > time_limit:
            return "TIMEOUT", None

        cube = Cube(state)
        h = white_cross_heuristic(cube)
        f = g + h

        if f > threshold:
            return f, None  # signal minimal f that exceeded threshold

        if cube.is_white_cross_solved():
            return "FOUND", path.copy()

        # depth guard
        if g >= max_depth:
            return float('inf'), None

        # transposition prune: if we've seen this state with a smaller or equal g, prune
        prev_best_g = transposition.get(state)
        if prev_best_g is not None and prev_best_g <= g:
            return float('inf'), None
        transposition[state] = g

        min_exceeded = float('inf')

        for succ_h, move, new_state in ordered_successors(state):
            # pruning heuristics:
            if prev_move:
                # don't immediately undo last move
                if INVERSE[prev_move] == move:
                    continue
                # avoid three moves in a row on same face (like R R R)
                # this reduces redundant branches
                if len(path) >= 2 and face_of_move(path[-1]) == face_of_move(path[-2]) == face_of_move(move):
                    continue

            # avoid cycles along current path
            if new_state in path_state_set:
                continue

            # push
            path.append(move)
            path_state_set.add(new_state)

            res, found = dfs(new_state, g+1, threshold, path, path_state_set, move)

            # pop
            path_state_set.remove(new_state)
            path.pop()

            if res == "TIMEOUT":
                return "TIMEOUT", None
            if res == "FOUND":
                return "FOUND", found

            if isinstance(res, (int, float)):
                if res < min_exceeded:
                    min_exceeded = res

        return min_exceeded, None

    # iterative deepening loop
    while True:
        # reset transposition each iteration (keeps memory bounded; could keep but must be careful)
        transposition.clear()
        path = []
        path_state_set = set([start_state])  # prevents immediate cycles with start
        res, found = dfs(start_state, 0, threshold, path, path_state_set, None)

        if res == "TIMEOUT":
            return None
        if res == "FOUND":
            return found
        if res == float('inf'):
            # nothing more to explore
            return None

        # increase threshold to the smallest f that exceeded previous threshold
        threshold = res

        # small safety to avoid runaway thresholds
        if threshold > max_depth + white_cross_heuristic(start_cube) + 40:
            return None

# -------------------------
# Example main: scramble and test
# -------------------------
if __name__ == "__main__":
    # Hard scrambles for white cross practice
    scrambles = [
        # Mix of face, middle, and double turns
        ['F', "U'", "L'", 'R', 'D', "B'", 'U', 'F', 'R', "L'", 'B', "D'", 'F', "U'", 'R', 'B', 'L', "D'", 'F', 'U'],
        ['B', 'D', 'R', "U'", 'L', "F'", "B'", "R'", 'U', "D'", 'L', 'F', 'R', 'U', "F'", 'D', 'L', "R'", "B'", "U'"],
        ['L', 'F', "D'", 'R', 'U', "B'", 'L', "U'", 'F', 'R', "B'", "D'", 'L', "F'", 'U', 'R', "B'", 'D', 'U', "F'"],
        ['R', "U'", 'L', 'D', "B'", 'F', "U'", "R'", 'L', 'D', "B'", 'F', "U'", "L'", 'R', 'F', "D'", 'B', 'U', 'L'],
        ['F', 'R', 'U', 'B', "D'", 'L', "U'", 'R', "F'", "B'", 'D', "L'", 'U', 'F', "R'", "B'", 'D', 'L', "U'", 'F'],
        ['D', "B'", "L'", 'U', "R'", 'F', 'D', "L'", 'B', 'U', "R'", 'F', 'L', "D'", 'B', "U'", 'R', 'F', 'L', "B'"],
        ['B', 'U', 'R', "D'", "F'", 'L', 'U', "B'", 'R', 'D', "L'", 'F', 'U', 'R', "B'", "D'", 'L', 'F', 'U', "R'"],
        ['R', 'F', "D'", 'L', 'B', "U'", 'R', 'F', 'D', "L'", "B'", 'U', "R'", 'F', "D'", 'L', 'B', "U'", 'R', 'F'],
        ['U', 'R', 'F', "L'", 'B', 'D', "U'", 'R', 'F', "L'", 'B', 'D', "U'", 'R', 'F', "L'", 'B', 'D', "U'", 'R'],
        ['F', "R'", 'U', 'L', "D'", "B'", 'F', 'R', "U'", 'L', 'D', 'B', 'F', "R'", "U'", "L'", "D'", 'B', 'F', "U'"],
    ]

    print(f"Testing {len(scrambles)} hard scrambles using IDA* white-cross solver...\n")

    for i, scramble in enumerate(scrambles, 1):
        print(f"===== SCRAMBLE {i} =====")
        c = Cube()
        for m in scramble:
            c = Cube(c.apply_move_to_state(m))

        print("Scramble:", scramble)
        start = time.time()
        sol = ida_star_white_cross_solver(c, max_depth=40, time_limit=20.0)
        elapsed = time.time() - start

        if sol:
            print(f"✅ Found white-cross solution ({len(sol)} moves, {elapsed:.2f}s): {sol}\n")
        else:
            print(f"❌ No solution found within limits ({elapsed:.2f}s)\n")
