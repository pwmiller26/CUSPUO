
from Colin import *
import sys
import numpy as np
from math import *


x0 = np.array([  1.56926535e+00,  -1.20789690e-01,  -3.05255789e-03,
         9.87920425e+05,   1.91912958e+05,   3.85333237e+02,
        -1.10001068e+04])


orient = np.array([c1(x0[0], x0[1], x0[2]), c2(x0[0], x0[1], x0[2]), c3(x0[0], x0[1], x0[2])])
orient = orient / sqrt(orient[0]**2 + orient[1]**2 + orient[2]**2)  #normalized direction vector
print orient

xpic = []
ypic = []
normlist = []
xold = []
yold = []
zold = []
dil = 50
j = 0
maxj = len(sys.argv[1:])
print maxj
for line in sys.argv[1:]:
    j = j + 1

    #what tile are you looking at?
    file_x = int(line[0:4])*100
    file_y = int(line[4:8])*100

    #roughly speaking in field of view?
    vect = np.array([file_x - x0[3], file_y - x0[4]])
    vect = vect / np.linalg.norm(vect)
    print acos(vect[0]*orient[0] + vect[1]*orient[1])
    if acos(vect[0]*orient[0] + vect[1]*orient[1]) < 0.8 and vect[1] > 0:
    	print j,  maxj
    	dat = np.load(line)
	#print len(dat), dil, len(dat) / dil
    	top = int(len(dat[0]) / dil)
    	for i in range(0, top):
            newi = dil*i
            x = dat[0][newi]
            y = dat[1][newi]
            z = dat[2][newi]
            xnew = pack_col_x(x0, x, y, z)
            ynew = pack_col_y(x0, x, y, z)
            normnew = sqrt((x0[3] - x)**2 + (x0[4] - y)**2 + (x0[5] - z)**2)
           # print xnew, ynew, normnew 
	    if abs(xnew) < 1312 and abs(ynew) < 734 and normnew < 40000:
                xpic.append(xnew)
                ypic.append(ynew)
                normlist.append(normnew)
         	xold.append(x)
		yold.append(y)
		zold.append(z)   
np.save('dildat', np.array([xpic, ypic, normlist, xold, yold, zold])) 



