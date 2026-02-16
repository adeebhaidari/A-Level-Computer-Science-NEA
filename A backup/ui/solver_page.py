from ursina import Entity, Button, Text, camera, color, Ursina, EditorCamera
from threed_cube import VisualCube
from scanner import CubeScanner
from solver import Solver

class SolverPage(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.visual_cube = VisualCube()
        self.visual_cube.x = 3 # this just moves the cube a bit to the right of the window
        self.solver = Solver()
        self.scanner = CubeScanner()
        
        # this just instantiate the entities for the buttons and its background
        # then pressed, these buttons will also run their specified assigned method
        self.background = Entity(parent = self, model='quad', scale = (0.4, 0.5), x = -0.6, color = color.black)
        self.scan_button = Button(parent = self, text = 'Scan Cube', y = 0.1, x = -0.6, scale = (0.3, 0.05), color = color.azure, on_click = self.run_scan)
        self.solve_button = Button(parent = self, text = 'Compute solution', x = -0.6, scale = (0.3, 0.05), color = color.blue, on_click = self.run_solve)
        self.status_text = Text(parent = self, text = 'Ready', y = -0.1, x = -0.6, origin = (0,0))
        self.cube_faces = []
        
        
    def run_scan(self):
        self.status_text.text = 'Scanning... Check the pop up window'
        scanned_data = self.scanner.run()
        
        if scanned_data is not None:
            print('Scan is complete!')
            # this feeds the 3d cube the current state of the users scanned cube
            self.visual_cube.recolour_cubies(scanned_data)
            # we now assign the logical cube the state of ghe uers current cube
            self.solver.cube = scanned_data
            
            for i in range(0,6):
                start_x, start_y = 0.6, 0.6
                for i in range()
            
            
            
            
            
            self.status_text.text = 'Scan is complete. Ready to solve!'
            self.solve_button.color = color.green
        else:
            self.status_text.text = 'The scan failed or was cancelled...'
    
    def run_solve(self):
        if not self.visual_cube.moves_queue:
            self.status_text.text = 'Computing solution...'
        
            full_solution = []
            # here we will not compuete the solution to each the white cross, f2l, oll and pll separately and then put them all together in the right order and append it into the solutions array
            '''
            white_cross_solution, _ = self.solver.solve_white_cross()
            if white_cross_solution:
                full_solution.extend(white_cross_solution)
            _, oll_solution = self.solver.solve_oll()
            #
            # this section will be for f2l once its finished
            #
            if oll_solution:
                full_solution.extend(oll_solution.split())
            '''
            _, pll_solution = self.solver.solve_pll()
            if pll_solution:
                full_solution.extend(pll_solution.split())
            print(f'Solution found!: {full_solution}')
            self.status_text.text = f'Solving: {len(full_solution)} moves'
            
            # we now need to feed this information to the 3d cube and the moves queue so its executed in the right order correctly
            self.visual_cube.moves_queue = full_solution
            self.visual_cube.process_queue()

app = Ursina()
solver_page = SolverPage()
EditorCamera()
app.run()