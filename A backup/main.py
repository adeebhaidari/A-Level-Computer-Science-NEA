from ursina import Ursina, EditorCamera
from ui import *

app = Ursina()
page = solver_page.SolverPage()
EditorCamera()
app.run()