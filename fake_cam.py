from optimize_camera import *
from scipy import *
import matplotlib.pyplot as plt
import pylab
from Colin import *


    #grab some data
f1 = open('ESBtop.txt', 'r')
x1 = []
y1 = []
z1 = []

i = 0
for line in f1:
    if i % 3 == 0:
        x1.append(float(line[0:-2]))
    elif i % 3 == 1:
        y1.append(float(line[0:-2]))
    else:
        z1.append(float(line[0:-2]))
    i += 1

f2 = open('chrytop.txt', 'r')
x2 = []
y2 = []
z2 = []

i = 0
for line in f2:
    if i % 3 == 0:
        x2.append(float(line[0:-2]))
    elif i % 3 == 1:
        y2.append(float(line[0:-2]))
    else:
        z2.append(float(line[0:-2]))
    i += 1

f3 = open('riverside.txt', 'r')
x3 = []
y3 = []
z3 = []

i = 0
for line in f3:
    if i % 3 == 0:
        x3.append(float(line[0:-2]))
    elif i % 3 == 1:
        y3.append(float(line[0:-2]))
    else:
        z3.append(float(line[0:-2]))
    i += 1

##omega = pi/4#resx[0]
##phi = 0#resx[1]
##k = 0#resx[2]
##x = 987421#resx[3]
##y = 191943#resx[4]
##z = 400# resx[5]
##f = 8000# resx[6]

#res = ensemble(200)
#resx = res[1]
resx = np.array([  1.55823490e+00,  -1.28163955e-01,   5.87465422e-03,
         9.86981556e+05,   1.85785006e+05,   7.11002180e+02,
        -1.44841397e+04]) 


xpic = []
ypic = []
fullx = x1  + x2 + x3
fully = y1 + y2 + y3
fullz = z1 + z2 + z3
for i in range(0, len(fullx)):
    Xe = fullx[i]
    Ye = fully[i]
    Ze = fullz[i]
    if i % 10 == 0:
        xpic.append(pack_col_x(resx, Xe, Ye, Ze))
        ypic.append(pack_col_y(resx, Xe, Ye, Ze))

plt.scatter(xpic, ypic, marker = '.', s = 0.1)
plt.show()

