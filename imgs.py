import requests
from StringIO import StringIO as sIO
from PIL import Image as img
import numpy as np
from newt import newt
from time import time

# download the image from a url
#res = requests.get("https://farm8.staticflickr.com/7569/16186587472_2ca92db482_b.jpg")
res = requests.get("https://scontent-lga1-1.xx.fbcdn.net/hphotos-xft1/v/t1.0-9/11150921_10206708037927992_7306102260647827673_n.jpg?oh=f83d5aabfc14385b956f9bf81e28576c&oe=55FE189B")
#res = requests.get("https://farm4.staticflickr.com/3739/9662657582_0956c7ee4c.jpg")
# open the image using PIL
im = img.open(sIO(res.content))
#im = img.open('C:/Users/Dozey/Py/hmm/static/img/face.jpg')
# convert the PIL image to a numpy array and turn it into a newt image
pic = newt(np.array(im, dtype=np.double))
# do a convolution with a 3x3 disk
pic.srtfilt().shw()


#pic2 = pic[:,:][:,:,[2, 0, 1]]
#pic[0,0][0]=0
#pic = np.hstack([pic,pic])
