import numpy as np
from matplotlib import cm
import matplotlib.pyplot as plt
from math import *

x = np.load('picture_data_dil10_dist40000.npy')
ind = (-x[2]).argsort()
x1 = x[0][ind]
y1 = x[1][ind]
z1 = x[2][ind]

plt.scatter(x1, y1, c=z1, cmap = cm.gist_ncar, marker = '.', s = 2, lw= 0)
plt.colorbar()
plt.show()
