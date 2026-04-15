from ursina import Ursina, EditorCamera, window
import sys
import os

root_directory = os.path.dirname(os.path.abspath(__file__))
if root_directory not in sys.path:
    sys.path.append(root_directory)

from ui.solver_page import SolverPage

app = Ursina()
s_page = SolverPage()
camera = EditorCamera()
camera.zoom_speed = 0
camera.position = (0, -1, 0)
window.fps_counter.enabled = False 
window.entity_counter.enabled = False
window.collider_counter.enabled = False
window.cog_button.enabled = False
app.run()