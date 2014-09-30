from PIL import Image as img
import numpy as np
from scipy.ndimage.filters import convolve as vconv

siz = 200
pic = np.random.randint(-1, 2, size=(siz, siz))
temp = np.zeros(pic.shape);
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
			temp[row, col] =  np.double(temp[row, col] > 0) - np.double(temp[row, col] < 0)

	value = np.sum(pic[:]-temp[:])
	
	for row in range(pic.shape[0]):
		for col in range(pic.shape[1]):
			pic[row, col] = temp[row, col]

pic = np.random.randint(-1, 2, size=(siz, siz, 3))

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

#255.0000  255.0000  255.0000
#255.0000  133.5714  156.3393
#12.1429  255.0000  163.9286
#z = np.zeros(pic.shape)
#red = np.dstack((pic,z,z))

#pic = np.array(im, dtype=np.double)
#pic = 255*pic/max(pic)
im = img.fromarray(pic.astype('uint8'))
im = im.resize((200, 200)) 
im.show()