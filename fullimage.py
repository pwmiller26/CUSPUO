import matplotlib.pyplot as plt
from matplotlib import cm
import pylab
from Colin import *
import sys
import numpy as np
from math import *


x0 = np.array([  1.55823490e+00,  -1.28163955e-01,   5.87465422e-03,
         9.86981556e+05,   1.85785006e+05,   7.11002180e+02,
        -1.44841397e+04]) 

xpic = []
ypic = []
normlist = []
dil = 1000
i = 0
print len(sys.argv[1:])
for line in sys.argv[1:]:
    i = i + 1
    if i % 1  == 0:
    	print line
    	dat = np.load(line)
	print len(dat), dil, len(dat) / dil
    	top = int(len(dat[0]) / dil)
    	for i in range(0, top):
            newi = dil*i
            x = dat[0][newi]
            y = dat[1][newi]
            z = dat[2][newi]
            xnew = pack_col_x(x0, x, y, z)
            ynew = pack_col_y(x0, x, y, z)
            normnew = sqrt((x0[3] - x)**2 + (x0[4] - y)**2 + (x0[5] - z)**2)
            if abs(xnew) < 1312 and abs(ynew) < 734:
                xpic.append(xnew)
                ypic.append(ynew)
                normlist.append(normnew)
            


plt.scatter(xpic, ypic, c=normlist, vmin = min(normlist), vmax = max(normlist), cmap = cm.prism, marker = '.', s = 0.1, lw = 0 )
plt.colorbar()
plt.axis([-1312, 1312, -734, 734])
plt.show()
plt.savefig('full.png')

np.save('picture_data', [xpic, ypic, normlist])

