from ursina import *

app = Ursina()

# --- 1. SETUP COLORS AND DATA ---
colors = {
    'top':    color.white,
    'bottom': color.yellow,
    'left':   color.orange,
    'right':  color.red,
    'front':  color.green,
    'back':   color.blue
}

cubes = []

# This empty entity will act as the handle for rotating sides
pivot = Entity()

# --- 2. GENERATE THE CUBE ---
for x in range(3):
    for y in range(3):
        for z in range(3):
            # Create a parent for the 6 colored faces
            # The 1.05 multiplier adds a tiny gap between cubes
            sub_cube = Entity(position=Vec3(x-1, y-1, z-1) * 1.05)
            
            # Attach 6 quads (stickers) to each sub-cube
            Entity(parent=sub_cube, model='quad', y=0.5, rotation_x=90, color=colors['top'])
            Entity(parent=sub_cube, model='quad', y=-0.5, rotation_x=-90, color=colors['bottom'])
            Entity(parent=sub_cube, model='quad', x=0.5, rotation_y=90, color=colors['right'])
            Entity(parent=sub_cube, model='quad', x=-0.5, rotation_y=-90, color=colors['left'])
            Entity(parent=sub_cube, model='quad', z=-0.5, color=colors['front'])
            Entity(parent=sub_cube, model='quad', z=0.5, rotation_y=180, color=colors['back'])
            
            # Add a black core so it looks like plastic, not hollow paper
            Entity(parent=sub_cube, model='cube', scale=0.99, color=color.black)
            
            cubes.append(sub_cube)

# --- 3. ROTATION LOGIC ---
def rotate_side(side_name):
    # Reset pivot for a clean rotation
    pivot.rotation = (0,0,0)
    
    for c in cubes:
        c.parent = scene # Detach from pivot first
        
        # Check which cubes belong to which side
        if side_name == 'top' and c.y > 0.5:
            c.parent = pivot
        elif side_name == 'right' and c.x > 0.5:
            c.parent = pivot
            
    # Smoothly rotate 90 degrees
    if side_name == 'top':
        pivot.animate_rotation((0, 90, 0), duration=0.2)
    elif side_name == 'right':
        pivot.animate_rotation((90, 0, 0), duration=0.2)

# --- 4. INPUT HANDLING ---
def input(key):
    if key == 'u': # Top face
        rotate_side('top')
    if key == 'r': # Right face
        rotate_side('right')

# Add a camera so we can move around the cube
EditorCamera()

app.run()