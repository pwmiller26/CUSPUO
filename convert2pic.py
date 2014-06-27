import numpy as np
from math import *


x = np.load('testdat.npy')


print len(x[0]), len(x[3])

#organize data by distance from camera
ind = (-x[2]).argsort()
xdat =    x[0][ind]
ydat =    x[1][ind]
normdat = x[2][ind]

###these are the LIDAR coords
oldx = x[3][ind]
oldy = x[4][ind]
oldz = x[5][ind]


print 'sort done'

xpix = 2625
ypix = 1468
   
s = (xpix, ypix)
xmax = np.amax(oldx)
ymax = np.amax(oldy)
normmax = np.amax(normdat)

pixelgrid = np.ones(s) * normmax           
ygrid = xmax*np.ones(s)
xgrid = ymax*np.ones(s)

#rescale coordinates to match up with image coordinates
xdat = xdat - min(xdat)
ydat = ydat - min(ydat)

print int(min(xdat)), int(max(xdat))
print int(min(ydat)), int(max(ydat))

print 'begin assigns'
#assign every point to the relevant pixel
for i in range(0, len(xdat)):
    xi = int(xdat[i])
    yi = int(ydat[i])
    normi = normdat[i]
    if xi < len(pixelgrid) and yi < len(pixelgrid[0]) and xi >= 0 and yi >= 0:
	if normi < pixelgrid[xi][yi]:
		pixelgrid[xi][yi] = normi
		xgrid[xi][yi] = xi
		ygrid[xi][yi] = yi
print 'done with assigning'

#try to kill noise by delete every point with void beneath it
#for i in range(0, xpix):
#    for j in range(1, ypix):
#	if pixelgrid[i][j - 1] == normmax:
#		pixelgrid[i][j] = normmax
#		xgrid[i][j] = xmax
#		ygrid[i][j] = ymax

print 'done with noise correction'

#for each point, color the point immediately below the same if that point is farther from camera
for i in range(0, xpix):
    for j in range(1, ypix):
	if pixelgrid[i][ypix - j] < pixelgrid[i][ypix - j -1]:
    	    pixelgrid[i][ypix - j - 1] = pixelgrid[i][ypix - j] 
            xgrid[i][ypix - j - 1]         = xgrid[i][ypix - j]
            ygrid[i][ypix - j - 1]         = ygrid[i][ypix - j]

print 'done with smoothing'
    
pixelgrid = pixelgrid.T
xgrid = xgrid.T
ygrid = ygrid.T
pixelgrid = np.flipud(pixelgrid)
xgrid = np.flipud(xgrid)
ygrid = np.flipud(ygrid)	

np.save('pixgrid', pixelgrid)
np.save('xgrid', xgrid)
np.save('ygrid', ygrid)
