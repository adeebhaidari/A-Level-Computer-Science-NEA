from ursina import Ursina, EditorCamera
import sys
import os

root_directory = os.path.dirname(os.path.abspath(__file__))
if root_directory not in sys.path:
    sys.path.append(root_directory)

from ui.solver_page import SolverPage

app = Ursina()
s_page = SolverPage()
EditorCamera()
app.run()