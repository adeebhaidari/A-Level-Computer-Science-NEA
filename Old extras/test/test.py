from collections import deque
import copy

# Face indices in self.state list:
# 0 = U (Up)
# 1 = L (Left)
# 2 = F (Front)
# 3 = R (Right)
# 4 = B (Back)
# 5 = D (Down)
#
# Each face is a list of 9 stickers, indexed row-major:
# [0 1 2
#  3 4 5
#  6 7 8]

class Cube:
    def __init__(self, state=None):
        if state is None:
            # Solved colours: U=W, L=O, F=G, R=R, B=B, D=Y
            self.state = [
                ['W'] * 9,  # U
                ['O'] * 9,  # L
                ['G'] * 9,  # F
                ['R'] * 9,  # R
                ['B'] * 9,  # B
                ['Y'] * 9   # D
            ]
        else:
            self.state = copy.deepcopy(state)

    def clone(self):
        return Cube(self.state)

    def get_state_id(self):
        # Return hashable representation
        return tuple(tuple(face) for face in self.state)

    # rotate a face clockwise (in-place)
    def rotate_face_cw(self, face_index):
        f = self.state[face_index]
        self.state[face_index] = [f[6], f[3], f[0],
                                  f[7], f[4], f[1],
                                  f[8], f[5], f[2]]

    # rotate a face counter-clockwise (in-place)
    def rotate_face_ccw(self, face_index):
        f = self.state[face_index]
        self.state[face_index] = [f[2], f[5], f[8],
                                  f[1], f[4], f[7],
                                  f[0], f[3], f[6]]

    # ---------- Moves ----------
    # The neighbor updates are implemented explicitly.
    # Indices are based on the face layouts described above.

    # U move: rotate Up face clockwise
    def move_U(self):
        self.rotate_face_cw(0)
        # cycle top rows of F, R, B, L
        temp = self.state[2][0:3]  # F top
        self.state[2][0:3] = self.state[3][0:3]  # F<-R
        self.state[3][0:3] = self.state[4][0:3]  # R<-B
        self.state[4][0:3] = self.state[1][0:3]  # B<-L
        self.state[1][0:3] = temp                # L<-temp

    def move_U_prime(self):
        # 3x cw = ccw, but implement directly
        self.rotate_face_ccw(0)
        temp = self.state[2][0:3]
        self.state[2][0:3] = self.state[1][0:3]
        self.state[1][0:3] = self.state[4][0:3]
        self.state[4][0:3] = self.state[3][0:3]
        self.state[3][0:3] = temp

    # D move: rotate Down face clockwise
    def move_D(self):
        self.rotate_face_cw(5)
        # cycle bottom rows of F, L, B, R (note direction)
        temp = self.state[2][6:9]  # F bottom
        self.state[2][6:9] = self.state[1][6:9]  # F<-L
        self.state[1][6:9] = self.state[4][6:9]  # L<-B
        self.state[4][6:9] = self.state[3][6:9]  # B<-R
        self.state[3][6:9] = temp                # R<-temp

    def move_D_prime(self):
        self.rotate_face_ccw(5)
        temp = self.state[2][6:9]
        self.state[2][6:9] = self.state[3][6:9]
        self.state[3][6:9] = self.state[4][6:9]
        self.state[4][6:9] = self.state[1][6:9]
        self.state[1][6:9] = temp

    # F move: rotate Front face clockwise
    def move_F(self):
        self.rotate_face_cw(2)
        # Affected strips: U bottom (6,7,8), L right column (2,5,8),
        # D top (2,1,0) reversed, R left column (6,3,0) reversed in assignment order
        temp = [self.state[0][6], self.state[0][7], self.state[0][8]]  # U bottom
        # U bottom <- L right col (in order 8,5,2)
        self.state[0][6], self.state[0][7], self.state[0][8] = \
            self.state[1][8], self.state[1][5], self.state[1][2]
        # L right col (2,5,8) <- D top (2,1,0)
        self.state[1][2], self.state[1][5], self.state[1][8] = \
            self.state[5][2], self.state[5][1], self.state[5][0]
        # D top (0,1,2) <- R left col (6,3,0) reversed to match orientation
        self.state[5][0], self.state[5][1], self.state[5][2] = \
            self.state[3][6], self.state[3][3], self.state[3][0]
        # R left col (0,3,6) <- temp (U bottom)
        self.state[3][0], self.state[3][3], self.state[3][6] = \
            temp[0], temp[1], temp[2]

    def move_F_prime(self):
        # inverse of F
        self.rotate_face_ccw(2)
        temp = [self.state[0][6], self.state[0][7], self.state[0][8]]
        # U bottom <- R left col (0,3,6)
        self.state[0][6], self.state[0][7], self.state[0][8] = \
            self.state[3][0], self.state[3][3], self.state[3][6]
        # R left col (0,3,6) <- D top (0,1,2) reversed
        self.state[3][0], self.state[3][3], self.state[3][6] = \
            self.state[5][2], self.state[5][1], self.state[5][0]
        # D top <- L right col (2,5,8)
        self.state[5][0], self.state[5][1], self.state[5][2] = \
            self.state[1][2], self.state[1][5], self.state[1][8]
        # L right col <- temp
        self.state[1][2], self.state[1][5], self.state[1][8] = \
            temp[0], temp[1], temp[2]

    # B move: rotate Back face clockwise
    def move_B(self):
        self.rotate_face_cw(4)
        # Affected strips: U top (0,1,2), R right column (2,5,8),
        # D bottom (8,7,6), L left column (6,3,0) -- orientation matters
        temp = [self.state[0][0], self.state[0][1], self.state[0][2]]  # U top
        # U top <- R right col (2,5,8)
        self.state[0][0], self.state[0][1], self.state[0][2] = \
            self.state[3][2], self.state[3][5], self.state[3][8]
        # R right col <- D bottom (8,7,6) (in order)
        self.state[3][2], self.state[3][5], self.state[3][8] = \
            self.state[5][8], self.state[5][7], self.state[5][6]
        # D bottom <- L left col (6,3,0)
        self.state[5][6], self.state[5][7], self.state[5][8] = \
            self.state[1][6], self.state[1][3], self.state[1][0]
        # L left col <- temp (U top) in order (0,1,2) -> (0,3,6)
        self.state[1][0], self.state[1][3], self.state[1][6] = \
            temp[2], temp[1], temp[0]

    def move_B_prime(self):
        self.rotate_face_ccw(4)
        temp = [self.state[0][0], self.state[0][1], self.state[0][2]]
        # U top <- L left col (0,3,6) reversed
        self.state[0][0], self.state[0][1], self.state[0][2] = \
            self.state[1][6], self.state[1][3], self.state[1][0]
        # L left col <- D bottom (6,7,8) -> place appropriately
        self.state[1][0], self.state[1][3], self.state[1][6] = \
            self.state[5][6], self.state[5][7], self.state[5][8]
        # D bottom <- R right col (2,5,8)
        self.state[5][6], self.state[5][7], self.state[5][8] = \
            self.state[3][8], self.state[3][5], self.state[3][2]
        # R right col <- temp
        self.state[3][2], self.state[3][5], self.state[3][8] = \
            temp[0], temp[1], temp[2]

    # R move: rotate Right face clockwise
    def move_R(self):
        self.rotate_face_cw(3)
        # Affects U right col (2,5,8), F right col (2,5,8), D right col (2,5,8), B left col (6,3,0)
        temp = [self.state[0][2], self.state[0][5], self.state[0][8]]  # U right col
        # U right <- F right
        self.state[0][2], self.state[0][5], self.state[0][8] = \
            self.state[2][2], self.state[2][5], self.state[2][8]
        # F right <- D right
        self.state[2][2], self.state[2][5], self.state[2][8] = \
            self.state[5][2], self.state[5][5], self.state[5][8]
        # D right <- B left (in reversed order)
        self.state[5][2], self.state[5][5], self.state[5][8] = \
            self.state[4][6], self.state[4][3], self.state[4][0]
        # B left <- temp (in reversed placement)
        self.state[4][0], self.state[4][3], self.state[4][6] = \
            temp[2], temp[1], temp[0]

    def move_R_prime(self):
        self.rotate_face_ccw(3)
        temp = [self.state[0][2], self.state[0][5], self.state[0][8]]
        self.state[0][2], self.state[0][5], self.state[0][8] = \
            self.state[4][0], self.state[4][3], self.state[4][6]
        self.state[4][0], self.state[4][3], self.state[4][6] = \
            self.state[5][8], self.state[5][5], self.state[5][2]
        self.state[5][2], self.state[5][5], self.state[5][8] = \
            self.state[2][2], self.state[2][5], self.state[2][8]
        self.state[2][2], self.state[2][5], self.state[2][8] = \
            temp[0], temp[1], temp[2]

    # L move: rotate Left face clockwise
    def move_L(self):
        self.rotate_face_cw(1)
        # Affects U left col (0,3,6), B right col (2,5,8), D left col (0,3,6), F left col (0,3,6)
        temp = [self.state[0][0], self.state[0][3], self.state[0][6]]  # U left col
        # U left <- B right (in reversed placement)
        self.state[0][0], self.state[0][3], self.state[0][6] = \
            self.state[4][8], self.state[4][5], self.state[4][2]
        # B right <- D left (reversed)
        self.state[4][2], self.state[4][5], self.state[4][8] = \
            self.state[5][6], self.state[5][3], self.state[5][0]
        # D left <- F left
        self.state[5][0], self.state[5][3], self.state[5][6] = \
            self.state[2][0], self.state[2][3], self.state[2][6]
        # F left <- temp
        self.state[2][0], self.state[2][3], self.state[2][6] = \
            temp[0], temp[1], temp[2]

    def move_L_prime(self):
        self.rotate_face_ccw(1)
        temp = [self.state[0][0], self.state[0][3], self.state[0][6]]
        self.state[0][0], self.state[0][3], self.state[0][6] = \
            self.state[2][0], self.state[2][3], self.state[2][6]
        self.state[2][0], self.state[2][3], self.state[2][6] = \
            self.state[5][0], self.state[5][3], self.state[5][6]
        self.state[5][0], self.state[5][3], self.state[5][6] = \
            self.state[4][2], self.state[4][5], self.state[4][8]
        self.state[4][2], self.state[4][5], self.state[4][8] = \
            temp[2], temp[1], temp[0]

    # generic move dispatcher
    def move(self, notation):
        """Apply a move notation like 'R', "R'", 'U2' etc."""
        # support doubled moves like 'R2'
        if notation.endswith('2'):
            base = notation[:-1]
            self.move(base)
            self.move(base)
            return

        if notation == 'U':
            self.move_U()
        elif notation == "U'":
            self.move_U_prime()
        elif notation == 'D':
            self.move_D()
        elif notation == "D'":
            self.move_D_prime()
        elif notation == 'F':
            self.move_F()
        elif notation == "F'":
            self.move_F_prime()
        elif notation == 'B':
            self.move_B()
        elif notation == "B'":
            self.move_B_prime()
        elif notation == 'R':
            self.move_R()
        elif notation == "R'":
            self.move_R_prime()
        elif notation == 'L':
            self.move_L()
        elif notation == "L'":
            self.move_L_prime()
        else:
            raise ValueError(f"Unknown move: {notation}")

    def generate_moves(self):
        moves = ['U', "U'", 'D', "D'", 'F', "F'", 'B', "B'", 'L', "L'", 'R', "R'"]
        next_states = []
        for m in moves:
            new_cube = self.clone()
            new_cube.move(m)
            next_states.append((new_cube, m))
        return next_states

    def is_white_cross_solved(self):
        # white cross on Down face (face 5): ensure the four edge stickers are white
        # and their adjacent side-centers match (i.e., edge aligned correctly).
        # Down face indices: 0..8, edges at 1,3,5,7.
        down = self.state[5]
        if not all(down[i] == 'W' for i in (1, 3, 5, 7)):
            return False

        # now check adjacent facelets for correct alignment:
        # Map each down-edge to the corresponding adjacent face center:
        # D[1] (down top middle) matches F[7] center? Actually for alignment:
        # We'll check the sticker adjacent to each white edge on the side faces:
        # - D[1] corresponds to face 2 (F) at index 7
        # - D[3] corresponds to face 1 (L) at index 7
        # - D[5] corresponds to face 3 (R) at index 7
        # - D[7] corresponds to face 4 (B) at index 7
        # The center color of each side face is at index 4.
        D = self.state
        checks = [
            (5, 1, 2, 7),  # (down face, down index, side face, side index)
            (5, 3, 1, 7),
            (5, 5, 3, 7),
            (5, 7, 4, 7)
        ]
        for _, d_idx, side_face, side_idx in checks:
            side_center = self.state[side_face][4]
            # the sticker on the side adjacent to the down edge:
            side_sticker = self.state[side_face][side_idx]
            if side_sticker != side_center:
                return False

        return True

    def __str__(self):
        # simple display for debugging
        lines = []
        for i, face in enumerate(self.state):
            lines.append(f"Face {i}: {face}")
        return "\n".join(lines)


# --- BFS White Cross Solver (depth-limited) ---
def bfs_white_cross_solver(start_cube, max_depth=8):
    queue = deque([(start_cube, [])])  # (cube, path)
    visited = set()
    while queue:
        cube, path = queue.popleft()
        sid = cube.get_state_id()
        if sid in visited:
            continue
        visited.add(sid)

        if cube.is_white_cross_solved():
            return path

        if len(path) >= max_depth:
            continue

        for nxt, mv in cube.generate_moves():
            queue.append((nxt, path + [mv]))

    return None


# --- Example usage ---
if __name__ == "__main__":
    # Create a solved cube and apply a small scramble (F, U, R for example)
    c = Cube()
    scramble = ['F', 'U', "R'", 'D']
    print("Applying scramble:", scramble)
    for s in scramble:
        c.move(s)

    print("Scrambled cube (brief):")
    print(c)

    print("\nSearching for white cross (BFS, depth-limited)...")
    solution = bfs_white_cross_solver(c, max_depth=10)

    if solution is None:
        print("No solution found within depth limit.")
    else:
        print("Solution found (length={}):".format(len(solution)), solution)
        # Show result by applying the solution to a fresh clone and printing down face
        test = c.clone()
        for m in solution:
            test.move(m)
        print("\nDown face after applying solution:", test.state[5])
