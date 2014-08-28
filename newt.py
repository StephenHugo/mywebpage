from PIL import Image as img
import numpy as np
from scipy.ndimage.filters import convolve as vconv

class newt:
	orig = np.array([0])
	pic = orig

	def __init__(self, pic):
		self.orig = pic
		self.pic = pic
		
	def shw(self):
		pic = 255*self.pic/np.max(self.pic)
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def neg(self):
		pic = -255*self.pic/np.max(self.pic)
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def conv(self,kernel='d 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):		
			self.pic[:,:][:,:,color] = vconv(self.orig[:,:][:,:,color],\
													kernel,mode='constant',cval=0.0)/\
													vconv(np.ones(self.orig[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)
		return self
		
	def dhat(self,kernel='d 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			m = np.mean(self.orig[:,:][:,:,color])
			self.pic[:,:][:,:,color] = self.pic[:,:][:,:,color] - vconv(self.orig[:,:][:,:,color],\
													kernel,mode='constant',cval=0.0)/\
													vconv(np.ones(self.orig[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)\
													+m
		return self
	
	def kernelmaker(self,kernel):	
		type, n = kernel.split(' ')
		n = np.double(n)
		n = n + 1 - n%2
		if (type=='d'):
			x = np.arange(-n//2+1,n//2+1,1)
			x, y = np.meshgrid(x,x)
			kernel = np.sqrt(x**2+y**2)<=n/2
		elif (type=='lap'):
			kernel = np.array([[-1., -1., -1.],[-1., 9., -1.],[-1., -1., -1.]])
		return np.array(kernel, dtype=np.double)
		
		
		
		