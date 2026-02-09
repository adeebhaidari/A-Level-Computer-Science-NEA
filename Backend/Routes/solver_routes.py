from flask import Blueprint, jsonify, render_template
# This looks inside the Cube folder for camera_scanner.py
from Backend.Cube.camera_scanner import CubeScanner 

# Define this as a blueprint instead of a second Flask app
solver_bp = Blueprint('solver_bp', __name__)

@solver_bp.route('/scan-cube', methods=['POST'])
def scan_cube():
    scanner = CubeScanner()
    # This opens the OpenCV window
    result = scanner.run() 
    
    if result:
        # result is the colour_map dictionary
        return jsonify({"status": "success", "data": result})
    else:
        return jsonify({"status": "error", "message": "Scanning failed"}), 400