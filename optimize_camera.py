from scipy.optimize import minimize, anneal
from math import *
import numpy as np
from random import *
from Colin import *

############################
#Actual positions of Empire State Building, Chrysler, and that fire station
Xe = 988229
Ye = 211952
Ze = 1507

Xc = 991078
Yc = 213111
Zc = 1118

Xf = 988819
Yf = 197822
Zf = 39

Xm = 990541
Ym = 213810
Zm = 859

##############################
#Photo locations
originx = 2624 / 2
originy = 1467 / 2

Xt_e = 145 - originx
Yt_e = originy - 103 

Xt_c = 1609 - originx
Yt_c = originy - 344 

Xt_f = 1645 - originx
Yt_f = originy - 1354

Xt_m = 1294 - originx
Yt_m = originy - 473
##############################



def fullfunc(x):
    return  (pack_col_x(x, Xe, Ye, Ze) - Xt_e)**2 \
           +(pack_col_x(x, Xc, Yc, Zc) - Xt_c)**2 \
           +(pack_col_x(x, Xf, Yf, Zf) - Xt_f)**2 \
           +(pack_col_x(x, Xm, Ym, Zm) - Xt_m)**2 \
           +(pack_col_y(x, Xe, Ye, Ze) - Yt_e)**2 \
           +(pack_col_y(x, Xc, Yc, Zc) - Yt_c)**2 \
           +(pack_col_y(x, Xf, Yf, Zf) - Yt_f)**2 \
           +(pack_col_y(x, Xm, Ym, Zm) - Yt_m)**2


x0 = np.array([  1.56438037e+00,  -1.23837300e-01,  -6.41605361e-04,
         9.87577881e+05,   1.89663330e+05,   5.08956767e+02,
        -1.22777347e+04]) 

def random_start():
    return x0 + np.array([gauss(0, 0.2), gauss(0, 0.2), gauss(0, 0.2), gauss(0, 1000), gauss(0, 1000), gauss(0, 10), gauss(0, 2000)])

def run():
    x0 = random_start()
#bnds = ((0, 2*pi), (0, 2*pi), (0, 2*pi), (0, 1100000), (0, 200000), (0, 600), (0, 100000))
    lo = np.array([0, 0, 0, 980000, 189000, 0, 0])
    up = np.array([2*pi, 2*pi,2*pi,  990000, 200000, 1000, 10000])
    #res = anneal(fullfunc, x0, full_output=True, disp=True, upper = up, lower = lo)
    bnds = ((0, 2*pi), (0, 2*pi), (0, 2*pi), (980000, 990000), (180000, 200000), (100, 1000), (0, None))
    res = minimize(fullfunc, x0, method = 'Nelder-Mead', options={'maxfev': 10000, 'maxiter': 10000})
    return res
#x = MCMC(packaged_func, x0, 100000)

def ensemble(k):
    min_score = 100000000000000
    coords = 0
    for i in range(0, k):
        res = run()
        if res.fun < min_score and res.x[4] < 199000:
            min_score = res.fun
            coords = res.x
    return [min_score, coords]




