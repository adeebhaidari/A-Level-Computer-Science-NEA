from ursina import Entity, Button, Text, destroy, camera, color, Ursina, EditorCamera, held_keys
from ui.threed_cube import VisualCube
from vision_main import scanner
from core_main import solver
import numpy as np

class SolverPage(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.visual_cube = VisualCube()
        
        self.visual_cube.x = 2 # this just moves the cube a bit to the right of the window
        self.solvers = {
            'CFOP': solver.CFOP(),
            'Kociemba': solver.Kociemba()
        }
        self.active_solver = self.solvers['CFOP'] # this is the default method of solving the cube
        self.scanner = scanner.CubeScanner()
        
        # this just instantiate the entities for the buttons and its background
        # then pressed, these buttons will also run their specified assigned method
        self.background = Entity(parent = self, model='quad', scale=(0.35, 0.6), x=-0.70, color=color.black66)
        
        self.cfop_btn = Button(parent=self, text='Use CFOP', y=0.25, x=-0.70, scale=(0.3, 0.05), color=color.gray, on_click=self.set_cfop)
        
        self.kociemba_btn = Button(parent=self, text='Use Kociemba', y=0.18, x=-0.70, scale=(0.3, 0.05), color=color.gray, on_click=self.set_kociemba)
        
        self.scan_button = Button(parent=self, text='Scan Cube', y=0.05, x=-0.70, scale=(0.3, 0.05), color=color.azure, on_click=self.run_scan)
        
        self.solve_button = Button(parent=self, text='Compute solution', y=-0.02, x=-0.70, scale=(0.3, 0.05), color=color.blue, on_click=self.run_solve)
        
        self.status_text = Text(parent=self, text='Ready', y=-0.15, x=-0.70, origin=(0,0), scale=0.8)
        
        self.cube_faces = []
        
        self.colours = ['W', 'B', 'R', 'G', 'O', 'Y']
        self.sticker_buttons = []
        self.editor_container = Entity(parent=self, enabled=False)
        
        self.key_map = {
            'u': 'U', 
            'd': 'D',
            'l': 'L', 
            'r': 'R',
            'f': 'F',
            'b': 'B'
        }
        
        self.wide_moves = {
            'r': ['R', 'M"'],
            'l': ['L', 'M'],
            'f': ['F', 'S'],
        }
    
    def input(self, key):
        # 1. Don't allow manual moves if the solver is currently running
        if self.visual_cube.moves_queue:
            return

        # 2. Check if the key pressed is one of our move keys
        if key in self.key_map:
            move = self.key_map[key]
            
            logical_move = move
            visual_move = move
            
            # to execute prime moves (e.g., R')
            if held_keys['shift']:
                logical_move = move + '"'
                visual_move = move + "'"
                
            self.visual_cube.execute_move(visual_move)
            try:
                self.active_solver.apply_move(logical_move)
                print(f'Logic sync: applied {logical_move}')
            except KeyError:
                print(f'Error: {logical_move} not found in notation map...')
            
            self.status_text.text = f'Manual Move: {move}'
    
    def run_scan(self):
        self.status_text.text = 'Scanning... Check the pop up window'
        scanned_data = self.scanner.run()
        
        if scanned_data is not None:
            scanned_data[2] = np.fliplr(scanned_data[2])
            scanned_data[3] = np.fliplr(scanned_data[3])
            scanned_data[4] = np.fliplr(scanned_data[4])
                
            print('Scan is complete!')
            # this feeds the 3d cube the current state of the users scanned cube
            self.visual_cube.recolour_cubies(scanned_data)
            # we now assign the logical cube the state of ghe uers current cube
            self.active_solver.cube = scanned_data
            # we allow the user to manually change any sticker colour
            self.manual_editor(scanned_data)
            
            self.status_text.text = 'Scan is complete. Ready to solve!'
            self.solve_button.color = color.green
        else:
            self.status_text.text = 'The scan failed or was cancelled...'
    
    def set_cfop(self):
        old_state = self.active_solver.get_current_state()
        self.active_solver = self.solvers['CFOP']
        self.active_solver.cube = old_state
        self.status_text.text = 'Active Solver: CFOP'
    
    def set_kociemba(self):
        old_state = self.active_solver.get_current_state()
        self.active_solver = self.solvers['Kociemba']
        self.active_solver.cube = old_state
        self.status_text.text = 'Active Solver: Kociemba'
    
    def manual_editor(self, data):
        for button in self.sticker_buttons:
            destroy(button)
        self.sticker_buttons = []
        
        self.editor_container.enabled = True
        self.status_text.text = 'Click the stickers to fix the colours if need be, then click CONFIRM'
        
        off_set = [
            (0,-1),
            (-1,0),
            (0,0),
            (1,0),
            (2,0),
            (0,1)
        ]
        
        base_x = 0.6
        
        for face_index, (off_set_x, off_set_y) in enumerate(off_set):
            for i in range(3):
                for j in range(3):
                    position = (
                        (off_set_x * 0.14) + (j * 0.045),
                        (off_set_y * 0.14) + (0.09 - i * 0.045)
                    )
                    
                    current_colour = data[face_index][i][j]
                    button = Button(parent=self.editor_container, model='quad', scale=0.04, position=position, colour=self.visual_cube.COLOUR_LOOKUP.get(current_colour, color.gray))
                    button.face = face_index
                    button.row = i
                    button.col = j
                    button.c_code = current_colour
                    button.on_click = lambda b = button: self.cycle_colour(b)
                    self.sticker_buttons.append(button)

        self.confirm_button = Button(
            parent=self.editor_container,
            text='CONFIRM',
            scale=(0.15, 0.04),
            y=-0.3,
            x=base_x + 0.07,
            color=color.green,
            on_click=self.manual_edits
        )
    
    def cycle_colour(self, button):
        index = self.colours.index(button.c_code) if button.c_code in self.colours else -1
        next_index = (index + 1) % len(self.colours)
        button.c_code = self.colours[next_index]
        button.color = self.visual_cube.COLOUR_LOOKUP[button.c_code]
    
    def manual_edits(self):
        new_data = np.full((6,3,3), '?', dtype = object)
        for button in self.sticker_buttons:
            new_data[button.face][button.row][button.col] = button.c_code
        
        self.visual_cube.recolour_cubies(new_data)
        self.active_solver.cube = new_data
        
        self.editor_container.enabled = False
        self.status_text.text = 'Cube colours have been updated!'

    def run_solve(self):
        if not self.visual_cube.moves_queue:
            full_solution = self.active_solver.solve()

            if full_solution == ['All ready solved']:
                self.status_text.text = "Cube is already solved!"
                self.status_text.color = color.green
                return

            if not full_solution or "Error" in full_solution:
                self.status_text.text = "Error: Could not find solution"
                self.status_text.color = color.red
                return

            visual_ready_solution = []
            for move in full_solution:
                clean_move = move.replace("'", '"')
                
                if '2' in clean_move:
                    base = clean_move.replace('2', '')
                    visual_ready_solution.append(base)
                    visual_ready_solution.append(base)
                else:
                    visual_ready_solution.append(clean_move)
            
            print(f'Solution found!: {visual_ready_solution}')
            self.status_text.text = f'Solving: {len(visual_ready_solution)} moves'
            self.status_text.color = color.white
            
            self.visual_cube.moves_queue = visual_ready_solution
            self.visual_cube.process_queue()