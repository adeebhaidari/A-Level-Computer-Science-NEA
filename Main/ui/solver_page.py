from ursina import Entity, Button, Text, destroy, camera, color, Ursina, EditorCamera, held_keys
from ui.threed_cube import VisualCube
# from vision_main import scanner
from core_main import solver
import numpy as np
import random
import sqlite3
import database.data_manager as data_manager

class SolverPage(Entity):
    def __init__(self):
        super().__init__(parent=camera.ui)
        self.visual_cube = VisualCube()
        
        self.visual_cube.x = 2
        self.solvers = {
            'CFOP': solver.CFOP(),
            'Kociemba': solver.Kociemba()
        }
        self.active_solver = None
        self.method_selected = False
        self.move_optimiser = solver.CFOP()
        
        #---> NOT NEEDED NOW self.scanner = scanner.CubeScanner()
        
        # this just instantiate the entities for the buttons and its background
        # then pressed, these buttons will also run their specified assigned method
        self.background = Entity(parent = self, model='quad', scale=(0.4, 0.75), x=-0.70, color=color.black66)
        
        self.cfop_btn = Button(parent=self, text='Use CFOP', y=0.3, x=-0.70, scale=(0.3, 0.05), color=color.gray, on_click=self.set_cfop)
        
        self.kociemba_btn = Button(parent=self, text='Use Kociemba', y=0.22, x=-0.70, scale=(0.3, 0.05), color=color.gray, on_click=self.set_kociemba)
        
        self.reset_btn = Button(parent=self, text='Reset Cube', y=0.14, x=-0.70, scale=(0.3, 0.05), color=color.gray, on_click=self.reset_cube)
        
        self.scramble_generator = Button(parent=self, text='Generate scramble', y=0.06, x=-0.70, scale=(0.3, 0.05), color=color.blue, on_click=self.generate_scramble)
        
        self.solve_button = Button(parent=self, text='Compute solution', y=-0.02, x=-0.70, scale=(0.3, 0.05), color=color.blue, on_click=self.run_solve)
        
        self.auto_move_button = Button(parent=self, text='Auto Move', y=-0.1, x=-0.70, scale=(0.3, 0.05), color=color.blue, on_click=self.auto_move)
        
        self.export_button = Button(parent=self, text='Download History', y=-0.18, x=-0.70, scale=(0.3, 0.05), color=color.orange, on_click=self.handle_export)

        self.preference_text = Text(parent=self, text='Do prefer this solution?', y=-0.35, x=-0.70, origin=(0,0), scale=0.7, enabled=False)
        
        self.yes_button = Button(parent=self, text='Yes', y=-0.4, x=-0.8, scale=(0.1, 0.04), color=color.green, enabled=False, on_click=lambda: self.record_preference('Yes'))
        
        self.no_button = Button(parent=self, text='No', y=-0.4, x=-0.6, scale=(0.1, 0.04), color=color.red, enabled=False, on_click=lambda: self.record_preference('No'))
        
        # ---> NOT NEEDED NOW self.scan_button = Button(parent=self, text='Scan Cube', y=0.01, x=-0.70, scale=(0.3, 0.05), color=color.azure, on_click=self.run_scan)
        
        self.status_text = Text(parent=self, text='Choose a method first \n (CFOP / Kociemba)', y=-0.3, x=-0.70, origin=(0,0), scale=0.8, color=color.yellow)
        
        self.solution = Text(parent=self, text='Solution: ...', y=-0.35, x = 0, origin=(0,0), scale=1)
        
        self.auto_move_scramble = []
        self.auto_move_scramble_full = len(self.auto_move_scramble) > 0
        
        self.moves_to_execute = []
        self.computed_solution_full = len(self.moves_to_execute) > 0
        
        self.executed_moves = []
        
        self.cube_faces = []
        
        self.key_map = {
            'u': 'U', 
            'd': 'D',
            'l': 'L', 
            'r': 'R',
            'f': 'F',
            'b': 'B'
        }
        
        
        '''
        # ---------- to do with camera stuff --------- NOT NEEDED NOW
        self.colours = ['W', 'B', 'R', 'G', 'O', 'Y']
        self.sticker_buttons = []
        self.editor_container = Entity(parent=self, enabled=False)
        '''
    
    def input(self, key):
        if self.active_solver is None:
            return
        
        if key == 'right arrow':
            self.move_forward()
        elif key == 'left arrow':
            self.move_backward()
        
        if not self.method_selected:
            if key in self.key_map:
                self.status_text.text = 'Select a method before scrambling!'
                self.status_text.color = color.red
                
        if self.visual_cube.moves_queue:
            return

        if key in self.key_map:
            move = self.key_map[key]
            
            logical_move = move
            visual_move = move
            
            # to execute prime moves (e.g. R')
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
    
    def reset_cube(self):
        if hasattr(self, 'visual_cube') and (self.visual_cube.is_animating or len(self.visual_cube.moves_queue) > 0):
            self.status_text.text = 'Cannot reset the cube \n while it is moving'
            self.status_text.color = color.red
            return
            
        if hasattr(self, 'visual_cube') and self.visual_cube:
            if hasattr(self.visual_cube, 'cubies'):
                for c in self.visual_cube.cubies:
                    destroy(c)
            destroy(self.visual_cube)
        
        
        for name in self.solvers:
            self.solvers[name].cube = self.solvers[name].reset()
        
        self.visual_cube = VisualCube()
        self.visual_cube.x = 2
        self.status_text.text = 'Cube has reset.'
        self.status_text.color = color.white
        
        if hasattr(self, 'solution'):
            self.solution.text = ''
            
        self.moves_to_execute = []
        self.executed_moves = []
    
    def set_cfop(self):
        self.active_solver = self.solvers['CFOP']
        self.method_selected = True
        self.cfop_btn.color = color.azure
        self.kociemba_btn.color = color.gray
        self.status_text.text = 'Active Solver: CFOP. \n You can now scramble.'
        self.status_text.color = color.white
    
    def set_kociemba(self):
        self.active_solver = self.solvers['Kociemba']
        self.method_selected = True
        self.kociemba_btn.color = color.azure
        self.cfop_btn.color = color.gray
        self.status_text.text = 'Active Solver: Kociemba. \n You can now scramble.'
        self.status_text.color = color.white

    '''
    # ------------------ methods dealing with camera stuff --------------- (may change)
    def run_scan(self):
        if not self.method_selected:
            self.status_text.text = 'Select a method before scanning!'
            self.status_text.color = color.red
            return
        
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
        
    # ---------------------------------------------------------------------------------- 
    '''

    def move_forward(self):
        if self.moves_to_execute and not self.visual_cube.is_animating:
            move = self.moves_to_execute.pop(0)
            self.executed_moves.append(move)
            self.visual_cube.execute_move(move)
            self.status_text.text = f'Executed: {move} \n Moves left: {len(self.moves_to_execute)}'
    
    def move_backward(self):
        if self.executed_moves and not self.visual_cube.is_animating:
            move = self.executed_moves.pop()
            self.moves_to_execute.insert(0, move)
            inverse_move = move[0] if '"' in move else move + '"'
            self.visual_cube.execute_move(inverse_move)
            self.status_text.text = f'Undid: {move} \n Moves left: {len(self.moves_to_execute)}'
    
    def auto_move(self):
        if self.active_solver is None:
            self.status_text.text = 'Select a method before scrambling!'
            self.status_text.color = color.red
            return
        
        if not self.auto_move_scramble and not self.computed_solution_full:
            self.status_text.text = 'Please generate a scramble first!'
            self.status_text.color = color.red
            return
        
        if not self.visual_cube.is_animating:
            if self.auto_move_scramble_full:
                moves = self.auto_move_scramble
                self.auto_move_scramble_full = False
                
                #self.visual_cube.moves_queue = self.auto_move_scramble.copy()
                #self.status_text.text = 'Applying scramble...'
                #self.status_text.color = color.white
                #for move in self.auto_move_scramble:
                #    self.active_solver.apply_move(move)
            else:
                moves = self.moves_to_execute
                
                #self.visual_cube.moves_queue = self.moves_to_execute.copy()
                #self.status_text.text = 'Executing solution...'
                #self.status_text.color = color.white
                #for move in self.moves_to_execute:
                #    if move == 'PLL error':
                #        continue
                #    self.active_solver.apply_move(move)
            self.visual_cube.moves_queue = moves.copy()
            for move in moves:
                if move != 'PLL error':
                    self.active_solver.apply_move(move)
            
            self.moves_to_execute.clear()
            self.auto_move_scramble.clear()
            self.status_text.text = 'Executing moves...'
            

    def generate_scramble(self, scramble=None):
        # instead of using a while loop within the for loop for pruning, I will be only using a for loop but constantly regenerating the potential moves - this heavily reduces the time complexity down to O(L) where L is the length of the scramble
        # fix the logic error so X or X" or X2 arent next to each other in the scramble - do later
        if scramble == None:
            moves = ['R', 'R"', 'R2', 'L', 'L"', 'L2', 'D', 'D"', 'D2', 'U', 'U"', 'U2', 'F', 'F"', 'F2', 'B', 'B"', 'B2']
            scramble = [random.choice(moves) for i in range (40)]
            scramble_optimiser = self.move_optimiser.optimise_moves(scramble)
            self.auto_move_scramble = scramble_optimiser
            
            solution_lines = []
            
            for i in range(0, len(scramble_optimiser), 7):
                part = scramble_optimiser[i:i + 7]
                solution_lines.append(' '.join(part))
            
            formatted_text = 'Scramble:\n' + '\n'.join(solution_lines)
        
            self.status_text.text = formatted_text
            self.status_text.color = color.green
            self.auto_move_scramble_full = True
            self.computed_solution_full = False
            self.moves_to_execute.clear()
            self.executed_moves.clear()
            self.current_scramble = list(self.auto_move_scramble)

    def run_solve(self):
        if not self.visual_cube.moves_queue:
            if self.active_solver is None:
                self.status_text.text = 'Please select a method first.'
                self.status_text.color = color.red
                return
            
            full_solution = self.active_solver.solve()

            if full_solution:
                if full_solution == ['All ready solved']:
                    self.status_text.text = "Cube is already solved!"
                    self.status_text.color = color.green
                    return

                if not full_solution or ['Error'] in full_solution:
                    self.status_text.text = 'Error: Could not find solution'
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
                self.current_solution = list(full_solution)
                
                ###
                self.auto_moves = visual_ready_solution
                solution_lines = []
                
                for i in range(0, len(full_solution), 15):
                    part = full_solution[i:i + 15]
                    solution_lines.append(' '.join(part))
                
                formatted_text = 'Solution:\n' + '\n'.join(solution_lines)
                self.solution.text = formatted_text
                ###
                
                self.auto_move_scramble.clear()
                self.auto_move_scramble_full = False
                
                self.computed_solution_full = True
                
                print(f'Solution found!: {visual_ready_solution}')
                self.status_text.text = f'Solving: {len(visual_ready_solution)} moves'
                self.status_text.color = color.white
                
                self.status_text.text = f'Solved! Use left and right arrows \n to move through. \n Or press auto move.'
                self.status_text.color = color.green
                self.executed_moves.clear()
                self.moves_to_execute = visual_ready_solution
                
                self.preference_text.enabled = True
                self.yes_button.enabled = True
                self.no_button.enabled = True
    
    def handle_export(self):
        try:
            data_manager.download_history()
            self.status_text.text = f'Solve history generated! \n Check your folder.'
            self.status_text.color = color.yellow
        except Exception as e:
            self.status_text.text = 'Error generating PDF...'
            self.status_text.color = color.red
            print(e)
    
    def record_preference(self, choice):
        if not self.current_scramble and not self.current_solution:
            self.status_text.text = 'Error: No data to save...'
            
        data_manager.save_solve(self.current_scramble, self.current_solution, choice)
        
        self.yes_button.enabled = False
        self.no_button.enabled = False
        self.preference_text.text = 'Saved to history!'