from ursina import Ursina, scene, Light, color, window, EditorCamera, destroy
from core.cube_logic import Cube
from ui.visual_cube import VisualCube
from vision.scanner import CubeScanner

app = Ursina()

# --- FLAT LOOK SETUP ---
# Destroy all lights (including default ones)
[destroy(l) for l in scene.entities if isinstance(l, Light)]
window.color = color.black
window.show_ursina_splash = False

# 1. Initialize Logic and Visuals
logical_cube = Cube()
visual_cube = VisualCube(logical_cube)

# 2. Camera setup
EditorCamera() 

def input(key):
    if key == 'c':
        scanner = CubeScanner()
        scanned_data = scanner.run() # This opens the CV window
        
        # Once scanner finishes (Q is pressed), update the logic
        if scanned_data is not None and scanned_data.shape == (6, 3, 3):
            logical_cube.cube = scanned_data
            visual_cube.update_visuals()
            print("Cube state updated from scanner!")
    
    # Standard clockwise moves (r, u, l, f, b, d)
    if key in ['r', 'u', 'l', 'f', 'b', 'd']:
        logical_cube.apply_move(key.upper())
        visual_cube.update_visuals()

    # Counter-clockwise moves (R, U, L, F, B, D - using SHIFT)
    if key in ['R', 'U', 'L', 'F', 'B', 'D']:
        logical_cube.apply_move(key + '"')
        visual_cube.update_visuals()

    # Scramble and Reset
    if key == 's':
        logical_cube.scramble()
        visual_cube.update_visuals()
        
    if key == 'backspace':
        logical_cube.cube = logical_cube.reset()
        visual_cube.update_visuals()

app.run()