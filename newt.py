from PIL import Image as img
from numpy import array, max, ones, double, arange, meshgrid, sqrt, median, std, where, min, exp, sort, arctan2, abs, sin, cos, log, pi, maximum, minimum, real, imag, mod
from scipy.ndimage.filters import convolve as vconv
from numpy.fft import fft2, ifft2, fftshift, ifftshift

class newt:
	pic = array([0])
	pic = pic

	def __init__(self, pic):
		self.max = max(pic)
		self.pic = pic
		
	def shw(self):
		pic = 255*self.pic/max(self.pic)
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def srt(self):
		pic = 255*self.pic/max(self.pic)
		for color in range(3):
			pic[:,:][:,:,color] = sort(sort(pic[:,:][:,:,color],(color+1)%2),color%2)
		im = img.fromarray(pic.astype('uint8'))
		im.show()
		
	def conv(self,kernel='lap 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):		
			self.pic[:,:][:,:,color] = vconv(self.pic[:,:][:,:,color],\
													kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)
		return self
		
	def highboost(self,kernel='d 17'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			m = median(self.pic[:,:][:,:,color])
			self.pic[:,:][:,:,color] = self.pic[:,:][:,:,color] - vconv(self.pic[:,:][:,:,color],\
													kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)\
													+m
		return self
		
	def varfilt(self,kernel='g 7'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			m = median(self.pic[:,:][:,:,color])
			self.pic[:,:][:,:,color] = vconv(self.pic[:,:][:,:,color]**2, kernel, mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)	- \
													(vconv(self.pic[:,:][:,:,color], kernel, mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0))**2								
		return self
		
	def srtfilt(self):
		
		for color in range(3):
			self.pic[:,:][:,:,color] = sort(sort(self.pic[:,:][:,:,color]),0)
											
		return self
		
	def dhat(self,kernel='d 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			pic = self.pic[:,:][:,:,color]
			m = median(pic)
			st = std(pic)
			pic -= m
			filt = vconv(self.pic[:,:][:,:,color],kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)
			diff = pic - filt
			dex = where(diff == min(diff))
			scl = pic[dex]/filt[dex]
			
			self.pic[:,:][:,:,color] = (pic - scl*filt) >max([st,10])
			
		return self
		
	def dline(self,kernel='g 3'):
		
		kernel = self.kernelmaker(kernel)
		for color in range(3):
			pic = self.pic[:,:][:,:,color]
			m = median(pic)
			st = std(pic)
			pic -= m
			filt = vconv(self.pic[:,:][:,:,color],kernel,mode='constant',cval=0.0)/\
													vconv(ones(self.pic[:,:][:,:,color].shape),kernel,mode='constant',cval=0.0)
			diff = pic - filt
			dex = where(diff == min(diff))
			scl = pic[dex]/filt[dex]
			for step in range(25):
				self.pic[:,:][:,:,color] += (pic - step*scl*filt/25)>max([st,10])
			self.pic[:,:][:,:,color]=self.pic[:,:][:,:,color]>75
		return self
	
	def kernelmaker(self,kernel):	
		type, n = kernel.split(' ')
		n = double(n)
		n = n + 1 - n%2
		if (type=='d'):
			x = arange(-n//2+1,n//2+1,1)
			x, y = meshgrid(x,x)
			kernel = sqrt(x**2+y**2)<=n/2
		elif (type=='g'):
			x = arange(-n//2+1,n//2+1,1)
			x, y = meshgrid(x,x)
			kernel = sqrt(x**2+y**2)
			kernel = exp(-kernel*9/n**2)*(kernel<=n/2)
		elif (type=='lap'):
			kernel = array([[-1., -1., -1.],[-1., 9., -1.],[-1., -1., -1.]])
		return array(kernel, dtype=double)
		
	def phasesym(self, type):

		shp = double(self.pic.shape[:2])
		
		if(mod(shp[0],2)==1):
			xrange= arange(-(shp[0]-1)/2,(shp[0])/2,1)/(shp[0]-1)		
		else:
			xrange= arange(-shp[0]/2,shp[0]/2,1)/shp[0]
			
		if(mod(shp[1],2)==1):
			yrange= arange(-(shp[1]-1)/2,(shp[1])/2,1)/(shp[1]-1)
		else:
			yrange= arange(-shp[1]/2,shp[1]/2,1)/shp[1]
			
		y = xrange.reshape(shp[0],1).repeat(shp[1],axis=1)
		x= yrange.reshape(1,shp[1]).repeat(shp[0],axis=0)
		
		radius = ifftshift(sqrt(x**2 + y**2))
		theta = ifftshift(arctan2(-y,x))

		lp = 1/(1+(radius/0.4)**20)

		radius[0,0]=1
		sinthet= sin(theta)
		costhet= cos(theta)
		if(type=='energy'):
			numo = 3
			nscl = 9
		else:
			numo = 7
			nscl = 5
		
		for color in range(3):		
			f = fft2(self.pic[:,:][:,:,color])
			oreo = double(0*ones(radius.shape))
			to = double(0*ones(radius.shape))
			ts = double(0*ones(radius.shape))
			
			for o in range(numo):
				angl = o*pi/numo
				ds = sinthet*cos(angl) - costhet*sin(angl)
				dc = costhet*cos(angl) + sinthet*sin(angl)
				dthet = abs(arctan2(ds,dc))
				dthet= minimum(dthet*numo/2,pi)	
				spread = (cos(dthet)+1)/2
				
				ethiso = double(0*ones(radius.shape))
				sumthiso = double(0*ones(radius.shape))
				
				for s in range(nscl):
					fo = 1/(3*(2.1**(s)))
					logo = lp*exp((-(log(radius/fo))**2)/(2*log(0.55)**2))
					logo[0,0]=0;
					filt = logo*spread
					eo = ifft2(f*filt)
					sumthiso = sumthiso + abs(eo)
					ethiso = ethiso + abs(real(eo)) - abs(imag(eo))
					if(s==0):
						tau = median(sumthiso[:])/sqrt(log(4))
				
				T = tau*(1-(1/2.1)**nscl)/(1-(1/2.1))
				T = maximum(sqrt(pi/2)*T + 2*sqrt((4-pi)/2)*T, 0.0001)
				ts = ts + sumthiso
				ethiso = ethiso - T
				to = to + ethiso
				
				if(o==0):
					maxe = ethiso
				else:
					change = double(ethiso>maxe)
					oreo = o*change + oreo*(1-change)
					maxe = maximum(maxe,ethiso)

			to = maximum(to,0)
			phasesym = 255*to/(ts+0.00001)
			oreo = oreo*255/numo
			if(type=='energy'):
				self.pic[:,:][:,:,color]=phasesym
			else:
				self.pic[:,:][:,:,color]=oreo
		return self