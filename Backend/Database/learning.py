from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
a = False

@app.route('/home') # you write the name of the page here
def home():
    return 'THIS IS THE MAIN PAGE'

@app.route('/<name>') # whatever is in the <> will be used when mentioned in the fuction
def user(name):
    return f'Hello {name}, how are you?'

@app.route('/admin')
def admin():
    if not a:
        return redirect(url_for('home')) # you put the name of the function as a string

@app.route('/admin2')
def admin2():
    return redirect(url_for('user', name='BOB')) # this alows you redirect and alo given parameters for the function



if __name__ == '__main__':
    app.run()