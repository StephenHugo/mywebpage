import requests
from StringIO import StringIO as sIO
from PIL import Image as img
import numpy as np
from newt import newt
from time import time

# download the image from a url
#res = requests.get("https://farm8.staticflickr.com/7569/16186587472_2ca92db482_b.jpg")
#res = requests.get("https://scontent-lga1-1.xx.fbcdn.net/hphotos-xft1/v/t1.0-9/11150921_10206708037927992_7306102260647827673_n.jpg?oh=f83d5aabfc14385b956f9bf81e28576c&oe=55FE189B")
#res = requests.get("https://farm4.staticflickr.com/3739/9662657582_0956c7ee4c.jpg")
#res2 = requests.get("http://www.urbancondospaces.com/wp-content/blogs.dir/1/files/2014/12/happy-new-year-2015.jpg")
# open the image using PIL
im = img.open("/Users/kaligamo/things/BME/Grants/Mage Hands/IMG_2530.JPG")
#im2 = img.open(sIO(res2.content)).resize(im.size, img.ANTIALIAS)
#print (im.size, im2.size)
# convert the PIL image to a numpy array and turn it into a newt image
pic = newt(np.array(im, dtype=np.double))

pic.highboost('d 27')
pic.shw()

#pic = np.array(im, dtype=np.double)

#q=np.array([[0.7071, 0.4082, 0.5774],[-0.7071, 0.4082, 0.5774],[0, -0.8165, 0.5774]])
#q2=np.array([[0.7071, 0.7071, 0],[-0.7071, 0.7071, 0],[0, 0, 1]])

#pic.dot(q)
#pic[:,:,2]=0
#pic.dot(q2)
#pic.dot(q.T)

#def shw(pic):
#	im = img.fromarray(pic.astype('uint8'))
#	im.show()
	
#shw(pic)

#pic2 = pic[:,:][:,:,[2, 0, 1]]
#pic[0,0][0]=0
#pic = np.hstack([pic,pic])
