import requests
from StringIO import StringIO as sIO
from PIL import Image as img
import numpy as np
from newt import newt
from time import time

# download the image from a url
#res = requests.get("http://static.squarespace.com/static/524c65ede4b061d170a78660/53124fd0e4b0fff880a511ec/531251c1e4b0fff880a5297f/1362121415000/jetpack-solver-everything.jpg")
res = requests.get("https://fbcdn-sphotos-f-a.akamaihd.net/hphotos-ak-xpf1/t1.0-9/10635727_10105641439402031_4076041239278420979_n.jpg")
#res = requests.get("https://farm4.staticflickr.com/3739/9662657582_0956c7ee4c.jpg")
# open the image using PIL
im = img.open(sIO(res.content))
# convert the PIL image to a numpy array and turn it into a newt image
pic = newt(np.array(im, dtype=np.double))
# do a convolution with a 3x3 disk
pic.highboost('g 17').shw()


#pic2 = pic[:,:][:,:,[2, 0, 1]]
#pic[0,0][0]=0
#pic = np.hstack([pic,pic])
