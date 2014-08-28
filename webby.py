import os
from flask import Flask, render_template, Blueprint, redirect, send_file, flash
from flask import request as req
import requests
from StringIO import StringIO as sIO
from PIL import Image as img
import numpy as np
from newt import newt

app = Flask(__name__)
app.secret_key = 'fez'

home = Blueprint('home', __name__)
projects = Blueprint('projects', __name__)
process = Blueprint('process', __name__)
about = Blueprint('about', __name__)

@home.route('/')
def index():
   return render_template('index.html')
	
@projects.route('/projects', methods=['GET', 'POST'])
def index():
	if req.method == 'POST':
		url = req.form['link']
		flash(url.replace(':','%3A').replace('/','%2F'))
		return redirect('/projects')
	else:
		return render_template('projects.html')
	 
@process.route('/processed')
def index():
	url = req.args.get('link')
	if not url:
		return render_template('projects.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(np.array(im, dtype=np.double))
		
		# do a convolution with a 7x7 disk
		pic.dhat('d 7')
		
		# revert to PIL format
		pic = 255*pic.pic/np.max(pic.pic)
		im = img.fromarray(pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
	 
@about.route('/about')
def index():
   return render_template('about.html')
	 
app.register_blueprint(home)
app.register_blueprint(projects)
app.register_blueprint(process)
app.register_blueprint(about)

if __name__ == '__main__':
	app.debug = True
	app.run()