from ursina import Entity, color, destroy, Vec3
from ursina.shaders import unlit_shader

# A dictionary to map single letters to Ursina color objects
COLOR_MAP = {
    'W': color.white, 'Y': color.yellow,
    'R': color.red,   'O': color.orange,
    'G': color.green, 'B': color.blue
}

class VisualCube(Entity):
    def __init__(self, logical_cube, **kwargs):
        super().__init__(**kwargs)
        self.logical_cube = logical_cube  # The backend math part of your cube
        self.cubies = []                  # List to keep track of the 26 small cubes
        self.create_cube()

    def create_cube(self):
        """Generates the 3x3x3 grid of black cubes."""
        for x in range(-1, 2):
            for y in range(-1, 2):
                for z in range(-1, 2):
                    # We don't need a cube in the very center (hidden)
                    if x == 0 and y == 0 and z == 0: continue
                    
                    # Create the 'plastic' base of the small cubie
                    c = Entity(
                        parent=self,
                        model='cube',
                        color=color.black,
                        position=(x, y, z),
                        scale=0.98,          # Slightly smaller than 1 to show small gaps
                        shader=unlit_shader
                    )
                    self.cubies.append(c)
        
        # Initial application of colored stickers
        self.update_visuals()

    def add_sticker(self, cubie, color_char, side):
        """Helper to attach a colored quad (sticker) to a specific face of a cubie."""
        clr = COLOR_MAP.get(color_char, color.magenta)
        
        # Create a flat plane (quad) and attach it to the black cubie
        sticker = Entity(
            parent=cubie, 
            model='quad', 
            color=clr, 
            shader=unlit_shader, 
            double_sided=True
        )
        
        # Position the sticker slightly outside the black cube face (0.52) 
        # and rotate it to face the correct direction.
        if side == 'top':    sticker.y=0.52;  sticker.rotation_x=90
        if side == 'bottom': sticker.y=-0.52; sticker.rotation_x=-90
        if side == 'right':  sticker.x=0.52;  sticker.rotation_y=90
        if side == 'left':   sticker.x=-0.52; sticker.rotation_y=-90
        if side == 'front':  sticker.z=-0.52; sticker.rotation_y=0
        if side == 'back':   sticker.z=0.52;  sticker.rotation_y=180

    def update_visuals(self):
        """Maps the logical_cube colors onto the 3D entities."""
        # First, clear any old stickers to avoid overlapping entities
        for c in self.cubies:
            for child in [child for child in c.children if isinstance(child, Entity)]:
                destroy(child)

        # Iterate through every black cubie and check its position to decide its color
        for c in self.cubies:
            # Rounding is vital because rotation math in 3D often results in 0.9999 instead of 1
            x, y, z = round(c.x), round(c.y), round(c.z)

            # TOP (y=1) / BOTTOM (y=-1)
            # The indices [index1][index2] map the 2D array of the logical cube to 3D space
            if y == 1:  self.add_sticker(c, self.logical_cube.cube[5][int(z+1)][int(x+1)], 'top')
            if y == -1: self.add_sticker(c, self.logical_cube.cube[0][int(-z+1)][int(x+1)], 'bottom')
            
            # RIGHT (x=1) / LEFT (x=-1)
            if x == 1:  self.add_sticker(c, self.logical_cube.cube[3][int(-y+1)][int(-z+1)], 'right')
            if x == -1: self.add_sticker(c, self.logical_cube.cube[1][int(-y+1)][int(z+1)], 'left')

            # FRONT (z=-1) / BACK (z=1)
            if z == -1: self.add_sticker(c, self.logical_cube.cube[2][int(-y+1)][int(x+1)], 'front')
            if z == 1:  self.add_sticker(c, self.logical_cube.cube[4][int(-y+1)][int(-x+1)], 'back')