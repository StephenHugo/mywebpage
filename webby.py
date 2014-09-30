from flask import Flask, render_template, Blueprint, redirect, send_file, flash
from flask import request as req
import requests
from StringIO import StringIO as sIO
from PIL import Image as img
from numpy import array, double, max, min, vstack, zeros, dstack
from newt import newt

app = Flask(__name__)
app.secret_key = '%\xdb\x1a[\xe9\x1d\x8bF\xd5\xc9\xad\xdc\x805\xd63\xca\xce\x11[\x1e\xe0\x06\xaf'

home = Blueprint('home', __name__)
projects = Blueprint('projects', __name__)
process = Blueprint('process', __name__)
research = Blueprint('research', __name__)

@home.route('/')
def index():
   return render_template('index.html')
	
@research.route('/research')
def index():
	return render_template('researchindex.html')
	
@research.route('/research/asf')
def asf():
	return render_template('asf.html')
	
@home.route('/publications')
def publications():
   return render_template('publications.html')
	
@home.route('/honors')
def honors():
   return render_template('honors.html')
	
@home.route('/about')
def about():
   return render_template('about.html')
	
@projects.route('/projects', methods=['GET', 'POST'])
def index():
	if req.method == 'POST':
		url = req.form['link']
		filtertype = req.form['button']
		if not url:
			return render_template('scientific.html')
		elif (filtertype == 'none'):
			return render_template('scientific.html')
		
		flash(url.replace(':','%3A').replace('/','%2F'))
		
		if (filtertype == 'asf'):
			return render_template('asffilter.html')			
		else:
			return redirect(url)
	else:
		return render_template('scientific.html')
	
@projects.route('/projects/standard', methods=['GET', 'POST'])
def standard():
	if req.method == 'POST':
		url = req.form['link']
		filtertype = req.form['button']
		if not url:
			return render_template('standard.html')
		elif (filtertype == 'none'):
			return render_template('standard.html')
		
		flash(url.replace(':','%3A').replace('/','%2F'))
		if (filtertype == 'highboost'):		
			return render_template('highboost.html')
		elif (filtertype == 'laplacian'):
			return render_template('laplacian.html')
		else:
			return redirect(url)
	else:
		return render_template('standard.html')
	
@process.route('/processed')
def highboost():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=double))
		
		# do a convolution with a 17x17 disk
		pic.highboost('d 17')
		
		# revert to PIL format
		pic = pic.pic - min(pic.pic)
		pic = 255*pic/max(pic)
		im = img.fromarray(pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
		
@process.route('/laplacian')
def laplacian():
	url = req.args.get('link')
	if not url:
		return render_template('scientific.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=double))
		
		# do a convolution with a nearly laplacian kernel (to avoid dividing by 0)
		pic.conv('lap 3')

		# revert to PIL format
		pic = 0.8*255*pic.pic/max(pic.pic)
		im = img.fromarray(pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
		
@process.route('/asf')
def asf():
	url = req.args.get('link')
	if not url:
		return render_template('scientific.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=double))
		
		# do a convolution with a 17x17 disk
		pic.dhat('g 7')
		
		# revert to PIL format
		z = zeros(pic.pic[:,:,0].shape)
		red = dstack((pic.pic[:,:,0],z,z))
		green = dstack((z,pic.pic[:,:,1],z))
		blue = dstack((z,z,pic.pic[:,:,2]))
		red = 255*red/max(red)
		green = 255*green/max(green)
		blue = 255*blue/max(blue)
		pic = vstack((red,green,blue))
		im = img.fromarray(pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
	 
app.register_blueprint(home)
app.register_blueprint(projects)
app.register_blueprint(process)
app.register_blueprint(research)

if __name__ == '__main__':
	app.debug = True
	app.run()