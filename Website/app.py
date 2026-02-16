from flask import Flask, render_template, jsonify, request
from Backend.Routes.solver_routes import solver_bp 

app = Flask(__name__, 
            static_folder='Frontend/static', 
            template_folder='Frontend/templates')

app.register_blueprint(solver_bp)

@app.route('/')
def index():
    return render_template('solver.html')

if __name__ == '__main__':
    app.run(debug=True)