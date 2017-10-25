from flask import render_template

from . import main


# decorators to register functions as handlers for events

# http://localhost:5000/
@main.route('/')
def index():
    return render_template('main/index.html', title='Welcome to MYAPP')
