import cv2 as cv
import numpy as np

class CubeScanner:
    def __init__(self):
        # the top left coordinate of the cube scanning grid
        self.gap = 50
        self.sticker_size = 60
        # in the order of index 0 1 2 3 4 5 being white blue red green orange yellow
        # (This matches: 0:W, 1:B, 2:R, 3:G, 4:O, 5:Y)
        self.face_order = ['white', 'blue', 'red', 'green', 'orange', 'yellow']
        # this stores the colours of each sticker for each face
        self.colour_map = {}
    
    def draw_interface(self, frame):
        # these set the layout of the cube grid with respect to the size of the camera output screen
        height, width, _ = frame.shape
        total_grid_size = (3 * self.sticker_size) + (2 * self.gap)
        start_x = (width - total_grid_size) // 2
        start_y = (height - total_grid_size) // 2
        
        for row in range(3):
            for col in range(3):
                x1 = start_x + (col * (self.sticker_size + self.gap))
                y1 = start_y + (row * (self.sticker_size + self.gap))
                x2 = x1 + self.sticker_size
                y2 = y1 + self.sticker_size
                
                cv.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
        cv.putText(frame, 'Align Cube & Press SPACE', (start_x, start_y - 20), cv.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)       
    
    def get_colour(self, h, s):
        # checks for white first as it tends to have a low saturation value
        if s < 70: 
            return 'W'
        # checks the hue ranges
        if h < 10 or h > 160:
            return 'R'
        elif 10 <= h < 25:
            return 'O'
        elif 25 <= h < 45:
            return 'Y'
        elif 45 <= h < 85:
            return 'G'
        elif 85 <= h < 130:
            return 'B'
        # returns a question mark if no valid colour was detected within these ranges
        return '?' 
    
    def capture_face(self, hsv_frame):
        # we are using the same grid layout as the one in the drae interface method so we know which squares to look at
        height, width, _ = hsv_frame.shape
        total_grid_size = (3 * self.sticker_size) + (2 * self.gap)
        start_x = (width - total_grid_size) // 2
        start_y = (height - total_grid_size) // 2
        
        # this will represent a single face of the cube as 2d array - 3 by 3
        face_data = []

        for row in range(3):
            temp_row = []
            for col in range(3):
                x1 = start_x + (col * (self.sticker_size + self.gap))
                y1 = start_y + (row * (self.sticker_size + self.gap))
                x2 = x1 + self.sticker_size
                y2 = y1 + self.sticker_size
                
                # this looks at a certain region of interest which is a single sticker on the face of the cube
                roi = hsv_frame[y1:y2, x1:x2]
                
                # since all the data of the region of interest (roi) is a numpy array, this will calculate the average hsv value for all the data items in the array to represent a more acurate value of the stickers colour 
                avg_hsv = cv.mean(roi)
                h, s = avg_hsv[0], avg_hsv[1]
                
                colour_char = self.get_colour(h, s)
                temp_row.append(colour_char)
            face_data.append(temp_row)
        
        return face_data
    
    def run(self):
        # this opens the deafult camera
        capture = cv.VideoCapture(0)
        current_face_index = 0 # this is the index of the current face of the cube
        
        # Array to store the 6 faces for the logical cube
        cube_array = [None] * 6

        while True:
            # ret is a boolean value indicating if the capturing of the frame was successful, frame is the actual frame captured by the camera
            ret, frame = capture.read()
            if not ret:
                break
            # this flips the frame so if an object moves in direction X, it will also look to move in direction X on the camera feed as well
            frame = cv.flip(frame, 1)
            # this converts the colour data of the frame from BGR to HSV allowing for more accurate colour values
            hsv_frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            self.draw_interface(frame)
            
            # this outputs text in the camera feed guiding the user which face to scan at a time
            if current_face_index < 6:
                temp_instruction = f'Scan the {self.face_order[current_face_index]} face!'
                cv.putText(frame, temp_instruction, (10, 30), 
                        cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            else:
                cv.putText(frame, 'Scan Complete! Press Q to exit', (10, 30), cv.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

            cv.imshow('Cube Scanner', frame)
            # if the user presses q they quit the system, if they press the space bar, they scan the cube in the frame
            key = cv.waitKey(1) 
            if key == ord('q'):
                break
            elif key == 32: # the spacebar
                if current_face_index < 6:
                    face_result = self.capture_face(hsv_frame)
                    # store in the map for your records and the array for the logic
                    self.colour_map[self.face_order[current_face_index]] = face_result
                    cube_array[current_face_index] = face_result
                    
                    print(f'The {self.face_order[current_face_index]} face has been captured!')
                    current_face_index += 1
                else:
                    print('Already captured all faces!')

        capture.release()
        cv.destroyAllWindows()
        
        # Return the data formatted as a numpy array for the logical Cube
        return np.array(cube_array)