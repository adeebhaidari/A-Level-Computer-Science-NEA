'''
this will handle login, registration and user settings

'''
from flask import Blueprint, render_template
import sqlite3

account_bp = Blueprint('account_bp', __name__)

@account_bp.route('/login')
def login():
    return render_template('login.html')
