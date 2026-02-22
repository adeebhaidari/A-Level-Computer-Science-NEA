from ursina import Ursina, Entity, Vec3, color, scene, invoke, EditorCamera

class VisualCube(Entity):
    def __init__(self, **kwargs):
        super().__init__(model = None, **kwargs)
        # self.parent = scene # this forces trhe entity to be in 3d space
        self.cubies = [] # this will store each individual small 1x1 cube that makes up the cube - except the cube that is in the middle of the 3d shape as there isnt a piece there
        self.rotation_helper = Entity()
        self.create_cube()
        self.is_animating = False
        self.moves_queue = [] # this will store the list of moves to execite that have been computed by the solver class
        self.COLOUR_LOOKUP = {
            'W': color.white,
            'Y': color.yellow,
            'R': color.red,
            'O': color.orange,
            'G': color.green,
            'B': color.blue,
            '?': color.gray
        }
    
    def create_cubie(self, grid_pos):
        # this parent class is an empty entity that holds the stickers of the rubiks cube together
        cubie = Entity(position=grid_pos * 1.05)
        cubie.stickers = []
        # this method handles the process or creating the stickern entities such that there parent class is the cubie class
        def make_sticker(axis, position, rotation, name, default_colour):
            s = Entity(parent=cubie, model='quad', color=default_colour)
            setattr(s, axis, position)
            s.rotation = rotation
            s.name = name
            cubie.stickers.append(s)
        
        # we now create 6 faces and attach them to the cubie since each little cubie has 6 faces
        # and so that it looks like a cube - to form a cube shape - we move them some small amoutn away from the center
        if grid_pos.y == 1:
            make_sticker('y', 0.501, (90,0,0), 'top', color.yellow)
        if grid_pos.y == -1:
            make_sticker('y', -0.501, (-90,0,0), 'bottom', color.white)
        if grid_pos.x == 1:
            make_sticker('x', 0.501, (0,-90,0), 'right', color.green)
        if grid_pos.x == -1:
            make_sticker('x', -0.501, (0,90,0), 'left', color.blue)
        if grid_pos.z == -1:
            make_sticker('z', -0.501, (0,0,0), 'front', color.red)
        if grid_pos.z == 1:
            make_sticker('z', 0.501, (0,180,0), 'back', color.orange)

        # finally we add a black internal cube entity to fill in the gaps as if they havev a black outline to make the colours look like stickers on the cube
        Entity(parent=cubie, model='cube', scale=0.99, color=color.black)
        return cubie

    def create_cube(self):
        for x in range(-1,2):
            for y in range(-1,2):
                for z in range(-1,2):
                    if x == 0 and y == 0 and z == 0: # this skips the position of the center of the cube since there is no cubie in the center of the cube
                        continue
                    # here we append each cubie entity into the cubies array
                    cubie = self.create_cubie(Vec3(x,y,z)) # we multiple the positions by a small scale to add a small gao between each cubie
                    self.cubies.append(cubie)

    def recolour_cubies(self, scanner_data):
        for cubie in self.cubies:
            x, y, z = int(round(cubie.x)),int(round(cubie.y)), int(round(cubie.z))

            # this will take the colour value element from each position in the 3x3x6 array that is returned from the data returns frm the cube scanner class after its ran
            for sticker in cubie.stickers:
                cubie_code = '?'
                if sticker.name == 'top': # the yellow centered face
                    cubie_code = scanner_data[5][z + 1][x + 1]
                elif sticker.name == 'bottom': # the white centered face
                    cubie_code = scanner_data[0][z + 1][x + 1]
                elif sticker.name == 'front': # the red centered face
                    cubie_code = scanner_data[2][-y + 1][x + 1]
                elif sticker.name == 'back': # the orange centered face
                    cubie_code = scanner_data[4][-y + 1][-x + 1]
                elif sticker.name == 'left': # the blue centered face
                    cubie_code = scanner_data[1][-y + 1][-z + 1]
                elif sticker.name == 'right': # the green centered face
                    cubie_code = scanner_data[3][-y + 1][z + 1]
                
                if cubie_code in self.COLOUR_LOOKUP: # this assigns the correct colour to the sticker
                    sticker.color = self.COLOUR_LOOKUP[cubie_code]

    def rotate_side(self, side_axis, layer_pos, direction = 1):
        if self.is_animating: # if the cube is already animating, dont do anything
            return
        self.is_animating = True
        
        self.rotation_helper.rotation = (0,0,0)
        for cubie in self.cubies:
            cubie.parent = scene # this releases the cubies from the previous rotations/moves
            # this checks which layer the cubie is in
            # if it is in the right layer, that will become the child class of the rotation_helper entity so that when the entity rotates, the correct cubies on that layer can move with it after
            if round(getattr(cubie, side_axis) / 1.05) == layer_pos:
                cubie.parent = self.rotation_helper
        
        # this will now animate the turns to be smooth and not instant
        rotation = Vec3(0,0,0)
        if side_axis == 'x':
            rotation = Vec3(90 * direction,0,0)
        if side_axis == 'y':
            rotation = Vec3(0,90 * direction,0)
        if side_axis == 'z':
            rotation = Vec3(0,0,90 * direction) # direction can be 1 for single turns or 2 for double turns e.g. R2 or F2
        
        self.rotation_helper.animate_rotation(rotation, duration=0.25)
        # after executing a single turn, we need to tell the app that it should wait themn it should run the logic which resets the parent entity of the cubies
        invoke(self.reset_cubie_parents, delay = 0.5)

    def reset_cubie_parents(self):
        for cubie in self.cubies:
            # this will calculate the cubies position relative to the world/environment they are in so they dont jump when they are released from their previous parent entity
            world_position, world_rotation = cubie.world_position, cubie.world_rotation
            cubie.parent = scene # this makes the cubies new parent entity the current part of the environment they are in, the 'scene'
            cubie.position, cubie.rotation = world_position, world_rotation
        self.is_animating = False
        self.process_queue() # this should then trigger the next move - this is just for testing to see fi the program can execute each move one by one on its own, the later i will allow the user to go back and forth with how the cube moves when executing the moves for the computed solution
    
    def process_queue(self): # this will prepare the next move to be executed at the right moment by checking if the queue is not empty to prevent an underflow and by also chekcing if the cube isnt being animated as moving
        if self.moves_queue and not self.is_animating:
            move = self.moves_queue.pop(0)
            self.execute_move(move)
    
    def execute_move(self, move):
        if not move or self.is_animating:
            return
        
        base = move[0]
        modifier = move[1:] if len(move) > 1 else ''
        
        move_map = {
            'R': ('x', 1, 1),
            'L': ('x', -1, -1),
            'U': ('y', 1, 1),
            'D': ('y', -1, -1),
            'F': ('z', -1, 1),
            'B': ('z', 1, -1),
            'y': ('y', 'all', 1),
            'x': ('x', 'all', 1),
            'z': ('z', 'all', 1),
        }
        
        if base not in move_map:
            return
        
        axis, layer, direction = move_map[base]
        
        if '"' in modifier:
            direction *= -1
        
        if '2' in modifier:
            direction *= 2
        
        if layer == 'all':
            self.rotate_cube(axis, direction)
        else:
            self.rotate_side(axis, layer, direction)
    
    def rotate_cube(self, axis, direction):
        if self.is_animating:
            return
        self.is_animating = True
        
        self.rotation_helper.rotation = (0,0,0)
        for cubie in self.cubies:
            cubie.parent = self.rotation_helper
        
        rotation_vector = Vec3(0,0,0)
        setattr(rotation_vector, axis, 90 * direction)
        
        self.rotation_helper.animate_rotation(rotation_vector, duration = 0.25)
        invoke(self.reset_cubie_parents, delay = 0.5)
