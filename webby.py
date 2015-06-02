from flask import Flask, render_template, Blueprint, redirect, send_file, flash
from flask import request as req
import requests
from StringIO import StringIO as sIO
from PIL import Image as img
from numpy import array, double, max, min, vstack, zeros, dstack, random, sum, zeros
from newt import newt

app = Flask(__name__)
app.secret_key = '%\xdb\x1a[\xe9\x1d\x8bF\xd5\xc9\xad\xdc\x805\xd63\xca\xce\x11[\x1e\xe0\x06\xaf'

home = Blueprint('home', __name__)
projects = Blueprint('projects', __name__)
process = Blueprint('process', __name__)
research = Blueprint('research', __name__)
mapgenerator = Blueprint('mapgenerator',__name__)

@home.route('/')
def index():
   return render_template('index.html')
	
@research.route('/research')
def index():
	return render_template('researchindex.html')
	
@research.route('/research/asf')
def asf():
	return render_template('asf.html')
	
@research.route('/research/migration')
def migration():
	return render_template('migration.html')
	
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
		
		flash(url.replace(':','%3A').replace('/','%2F').replace('?','%3F').replace('=','%3D').replace('&','%26'))
		
		if (filtertype == 'asf'):
			return render_template('asffilter.html')	
		elif (filtertype == 'varfilt'):
			return render_template('varfilter.html')	 
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
		
		flash(url.replace(':','%3A').replace('/','%2F').replace('?','%3F').replace('=','%3D').replace('&','%26'))
		
		if (filtertype == 'highboost'):		
			return render_template('highboost.html')
		elif (filtertype == 'laplacian'):
			return render_template('laplacian.html')
		elif (filtertype == 'phasesym'):
			return render_template('phasesym.html')	
		elif (filtertype == 'phasesym2'):
			return render_template('phasesym2.html')
		elif (filtertype == 'srtfilt'):
			return render_template('srtfilt.html')
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
		
@process.route('/varfilt')
def varfilt():
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
		pic.varfilt('g 5')
		
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
		
@process.route('/phasesym2')
def phasesym2():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# shrink very large images
		im.thumbnail((512,512), img.ANTIALIAS)
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=complex))
		
		# do stuff
		pic.phasesym('not energy')
		
		# revert to PIL format
		#pic = pic.pic - min(pic.pic)
		#pic = 255*pic/max(pic)
		im = img.fromarray(pic.pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
		
@process.route('/phasesym')
def phasesym():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# shrink very large images
		im.thumbnail((512,512), img.ANTIALIAS)
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=complex))
		
		# do stuff
		pic.phasesym('energy')
		
		# revert to PIL format
		#pic = pic.pic - min(pic.pic)
		#pic = 255*pic/max(pic)
		im = img.fromarray(pic.pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
		
@process.route('/srtfilt')
def srtfilt():
	url = req.args.get('link')
	if not url:
		return render_template('standard.html')
	
	try:
		# download the image from the url
		res = requests.get(url)
		
		# open the image using PIL
		im = img.open(sIO(res.content))
		
		# shrink very large images
		im.thumbnail((512,512), img.ANTIALIAS)
		
		# convert the PIL image to a numpy array and turn it into a newt image
		pic = newt(array(im, dtype=complex))
		
		# do stuff
		pic.srtfilt()
		
		# revert to PIL format
		#pic = pic.pic - min(pic.pic)
		#pic = 255*pic/max(pic)
		im = img.fromarray(pic.pic.astype('uint8'))
		
		# save the new image
		buff = sIO()
		im.save(buff, 'JPEG', quality=90)
		
		buff.seek(0)
		
		return send_file(buff, mimetype='image/jpeg')
	except:
		return redirect(url)
		
@mapgenerator.route('/mapgen', methods=['GET', 'POST'])
def index():
	if req.method == 'POST':
		dngntype = req.form['button']
		siz = double(req.form['size'])
		flash(siz)
		if (dngntype == 'original'):		
			return render_template('curvy.html')
		elif (dngntype == 'boxes'):
			return render_template('boxes.html')
		else:
			return render_template('mapgen.html')
	else:
		return render_template('mapgen.html')
		
@mapgenerator.route('/curvymap')
def curvymap():
	siz = double(req.args.get('size'))
	siz = min([max([siz, 50]), 200])
	pic = random.randint(-1, 2, size=(siz, siz))
	temp = zeros(pic.shape);
	value = 1

	def pos(x, y):
		if (x<0):
			x=pic.shape[0]-1
		elif (x>pic.shape[0]-1):
			x=0
		if (y<0):
			y=pic.shape[1]-1
		elif (y>pic.shape[1]-1):
			y=0 
		return x, y
	
	while (value !=0):
		for row in range(pic.shape[0]):
			for col in range(pic.shape[1]):
				temp[row, col] = pic[pos(row-1, col-1)] + pic[pos(row, col-1)] + pic[pos(row+1, col-1)] +\
												pic[pos(row-1, col)] + pic[pos(row, col)] + pic[pos(row+1, col)] +\
												pic[pos(row-1, col+1)] + pic[pos(row, col+1)] + pic[pos(row+1, col+1)]
				temp[row, col] =  double(temp[row, col] > 0) - double(temp[row, col] < 0)

		value = sum(pic[:]-temp[:])
		
		for row in range(pic.shape[0]):
			for col in range(pic.shape[1]):
				pic[row, col] = temp[row, col]

	pic = random.randint(-1, 2, size=(siz, siz, 3))

	neg = 255, 255, 255
	zer = 255, 134, 156
	pos = 12, 163, 255

	for row in range(pic.shape[0]):
			for col in range(pic.shape[1]):
				if (temp[row, col] ==-1):
					pic[row,col] = neg
				elif (temp[row, col] ==0):
					pic[row, col] = zer
				else:
					pic[row, col] = pos
					
	im = img.fromarray(pic.astype('uint8'))
	im = im.resize((500, 500)) 
	
	# save the new image
	buff = sIO()
	im.save(buff, 'JPEG', quality=90)
	
	buff.seek(0)
	
	return send_file(buff, mimetype='image/jpeg')
	
@mapgenerator.route('/boxesmap')
def boxesmap():
	siz = double(req.args.get('size'))
	siz = min([max([siz, 50]), 200])
	pic = random.randint(-1, 2, size=(siz, siz))
	temp = zeros(pic.shape);
	value = 1

	def pos(x, y):
		if (x<0):
			x=pic.shape[0]-1
		elif (x>pic.shape[0]-1):
			x=0
		if (y<0):
			y=pic.shape[1]-1
		elif (y>pic.shape[1]-1):
			y=0 
		return x, y
	
	for t in range(20):
		for row in range(pic.shape[0]):
			for col in range(pic.shape[1]):
				temp[row, col] = pic[pos(row, col-1)] +\
												pic[pos(row-1, col)] + pic[pos(row, col)] + pic[pos(row+1, col)] +\
												pic[pos(row, col+1)]
				temp[row, col] =  double(temp[row, col] > 0) - double(temp[row, col] < 0)

		value = sum(pic[:]-temp[:])
		
		for row in range(pic.shape[0]):
			for col in range(pic.shape[1]):
				pic[row, col] = temp[row, col]

	pic = random.randint(-1, 2, size=(siz, siz, 3))

	neg = 255, 255, 255
	zer = 255, 134, 156
	pos = 12, 163, 255

	for row in range(pic.shape[0]):
			for col in range(pic.shape[1]):
				if (temp[row, col] ==-1):
					pic[row,col] = neg
				elif (temp[row, col] ==0):
					pic[row, col] = zer
				else:
					pic[row, col] = pos
					
	im = img.fromarray(pic.astype('uint8'))
	im = im.resize((500, 500)) 
	
	# save the new image
	buff = sIO()
	im.save(buff, 'JPEG', quality=90)
	
	buff.seek(0)
	
	return send_file(buff, mimetype='image/jpeg')
	 
app.register_blueprint(home)
app.register_blueprint(projects)
app.register_blueprint(process)
app.register_blueprint(research)
app.register_blueprint(mapgenerator)

if __name__ == '__main__':
	app.debug = True
	app.run()