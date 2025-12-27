from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/home-<name>')
def home(name):
    return render_template('index.html', content=name)

@app.route('/login')
def login():
    return render_template('login_in_sign_up.html')

@app.route('/account')
def account():
    return redirect(url_for('login'))

@app.route('/progress-predictor')
def progress():
    return render_template('linear_regression_and_charts.html')

@app.route('/solver')
def solver():
    return render_template('solver.html')

@app.route('/stats')
def stats():
    return render_template('stats.html')

@app.route('/timer')
def timer():
    return render_template('timer.html')

if __name__ == '__main__':
    app.run()