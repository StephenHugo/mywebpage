import os
from flask import Flask, render_template
from flask import Blueprint

app = Flask(__name__)

home = Blueprint('home', __name__)
conway = Blueprint('conway', __name__)
about = Blueprint('about', __name__)

@home.route('/')
def index():
    return render_template('index.html')
	 
@conway.route('/conway')
def index():
    return render_template('conway.html')
	 
@about.route('/about')
def index():
    return render_template('about.html')
	 
app.register_blueprint(home)
app.register_blueprint(conway)
app.register_blueprint(about)

if __name__ == '__main__':
	app.debug = True
	app.run()