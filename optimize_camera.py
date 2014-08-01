from scipy.optimize import minimize
from math import *
import numpy as np
from random import *
from Colin_old import *
#So this program is a bit of a mess, since truth be told the greater part of the battle is identifying fiducial points
#generally speaking, you'll have to modify the script anytime you want to find a new camera position,
#to accomodate new fiducials
#The basic procedure, though, is to type in the xyz coordinates of your fiducials below, and then the corresponding pixel coordinates
#modify the fullfunc function as needed to account for however many fiducials you have
#then set x0 below to be your best starting guess for the camera parameters
#once all this is set, run the modules, and call ensemble(100, x0)
#I find 100 is generally a sufficient number of iterations for the ensemble function to converge on a good fit
#you can use more or less as needed though


##############################
### I store here the physical x, y, z coordinates of the fiducial points
#generally I just grab these out lidar, by playing around with the display_lidar script....
Xe = 988229
Ye = 211952
Ze = 1309
##
Xc = 991078
Yc = 213111
Zc = 1118
##

Xw = 985021
Yw = 205694
Zw = 98

Xg = 983044
Yg = 209528
Zg = 313

Xi = 987490
Yi = 206730
Zi = 546



##Xf = 988819
##Yf = 197822
##Zf = 39
##
##Xm = 990541
##Ym = 213810
##Zm = 859
##
##X6 = 988002
##Y6 = 198215
##Z6 = 250
##
################################
### originx and originy are the coordinates of the center of the image in the coordinate system where 0, 0 is the upper left corner of the image
originx = 2996 / 2
originy = 1998 / 2


#Each of these is the x and y pixel coordinate for the given fiducial points
#the numbers are the pixel values I got from the coordinate system where (0,0) is the upper left corner pixel
#To make the calculation easier, I change to the coordinate system where the origin is in the center of the image
Xt_e = 1825 - originx
Yt_e = originy - 869 
##
Xt_c = 2303 - originx
Yt_c = originy - 920 
##
Xt_w = 2075 - originx
Yt_w = originy - 1535

Xt_g = 471 - originx
Yt_g = originy - 1305

Xt_i = 2732 - originx
Yt_i = originy - 1198
################################

#This calculates the goodness of fit. the array x that is input is
# a numpy array of the from (omega, phi, kappa, x, y, z, f), where the
#first 3 values are orientation angles, the next 3 are position coordinates,
#and f is the focal length
#for each (x,y,z) of the fiducial we use the imput parameters to calculate
#the corresponding pixel X and Y
#the script then returns the sum of the squares of the differences between our
#projections and the measured values
def fullfunc(x):
    #note that the pack_col_x/y functions can be found in the module called Colin_old.py
    return  (pack_col_x(x, Xe, Ye, Ze) - Xt_e)**2 \
           +(pack_col_x(x, Xc, Yc, Zc) - Xt_c)**2 \
           +(pack_col_x(x, Xw, Yw, Zw) - Xt_w)**2 \
           +(pack_col_x(x, Xg, Yg, Zg) - Xt_g)**2 \
           +(pack_col_x(x, Xi, Yi, Zi) - Xt_i)**2 \
           +(pack_col_y(x, Xe, Ye, Ze) - Yt_e)**2 \
           +(pack_col_y(x, Xc, Yc, Zc) - Yt_c)**2 \
           +(pack_col_y(x, Xw, Yw, Zw) - Yt_w)**2 \
           +(pack_col_y(x, Xg, Yg, Zg) - Yt_g)**2 \
           +(pack_col_y(x, Xi, Yi, Zi) - Yt_i)**2 

#UO - This is the currect best position I have for the Urban Observatory position
##x0 = np.array([  1.56926535e+00, -1.20789690e-01,  -3.05255789e-03,
##         9.87920425e+05,   1.91912958e+05,   3.85333237e+02,
##        -1.10001068e+04]) 


#To actually go about finding a new position, you first have to list a starting guess x0 like the one below
x0 = np.array([  1.53593185e+00,  -4.98427146e-01,  -1.90081166e-02,
         9.78512986e+05,   1.96138057e+05,   1.48188764e+03,
        -5.90336764e+03])

#takes a camera position and perturbs it in a gaussian fashion
def random_start(x):
    return x + np.array([gauss(0, 0.2), gauss(0, 0.2), gauss(0, 0.2), gauss(0, 100), gauss(0, 100), gauss(0, 10), gauss(0, 2000)])


#Imput a camera position
#first position is randomized slightly - want to avoid local minima if possible
#then figure out the orientation that minimizes fullfunc - best fit for fiducials
def run(x):
    start = random_start(x)
    res = minimize(fullfunc, start, method = 'Nelder-Mead', options={'maxfev': 10000, 'maxiter': 10000})
    return res

#repeats the run script k times, starting with x as your initial camera position
#each time you complete run(), check to see if new position is better than the old posiiton
#if so, use the new position for subsequent calls of run
#output the final fullfunc score, and the coordinates that generated it
def ensemble(k, x):
    min_score = 100000000000000
    coords = x
    for i in range(0, k):
        res = run(coords)
        if res.fun < min_score and res.x[4] < 199000:
            min_score = res.fun
            coords = res.x
    return [min_score, coords]




