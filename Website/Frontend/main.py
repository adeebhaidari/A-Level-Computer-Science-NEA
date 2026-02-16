from flask import Flask, render_template, url_for, redirect

app = Flask(__name__)

@app.route('/home-<name>')
def home(name):
    return render_template('index.html', content=name)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/account')
def account():
    return redirect(url_for('login'))

@app.route('/stats')
def progress():
    return render_template('stats.html')

@app.route('/solver')
def solver():
    return render_template('solver.html')

@app.route('/trainer')
def trainer():
    return render_template('trainer.html')

if __name__ == '__main__':
    app.run()