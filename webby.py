import os
from flask import Flask, render_template
from flask import Blueprint

app = Flask(__name__)

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('index.html')
	 
app.register_blueprint(home)

if __name__ == '__main__':
	app.debug = True
	app.run()