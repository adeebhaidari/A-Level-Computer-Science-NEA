'''
this will handle stats, averages, graphs etc

'''
from flask import Blueprint, render_template
import sqlite3

training_bp = Blueprint('training_bp', __name__)

@training_bp.route('/trainer')
def login():
    return render_template('trainer.html')