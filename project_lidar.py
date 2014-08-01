

#This script is meant to be run on compute. Reads in a specified set of numpy array files (.npy)
#Output is 3 .npy files, which are projections of the distance from camera, x and y coordinate
#of each lidar point onto an array of equal size and shape the same as the specified picture
#to run the script, type 'python project_lidar.py [Set of files to be analyzed'
#Thus, to have the script run over a whole data set, 'python project_lidar.py 9*.npy 0*.npy'
#If you want to just project a single file, for example, type 'python project_lidar.py 8831950.npy' 

#Import relevant modules
from Colin import * #this is the module containing the colinearity equation functions
import sys
import numpy as np
from math import *
import multiprocessing as mp


######################################################################
#This section contains important parameters - each of these needs to be specified by the user 

#This variable represents camera parameters. It is a 1 x 7 numpy array of the form
#x0 = [omega, phi, kappa, x, y, z, f], where the first 3 values are the camera oriention angles
#the next 3 are the camera position coordinates ny the NY-Long Island state plane system (same as used by MapPluto and LIDAR)
#and f is the focal length of the camera
x0 = np.array([  1.53593185e+00,  -4.98427146e-01,  -1.90081166e-02,
         9.78512986e+05,   1.96138057e+05,   1.48188764e+03,
        -5.90336764e+03])

#The opimize_camera script I wrote will generate solutions of this form, so generally you can just copy and paste
#what you get out of that to be x0 here


#Name you want to label output files with
#The output files will be called 'name_distgrid.npy', 'name_x.npy', 'name_y.npy'
name = 'WTC'

#1/2 the length and width of the desired image in pixels.
#TO BE CLEAR: Image will be twice the length and twice the width of the values entered here!
pic_size_x = int(0.5*2996)
pic_size_y = int(0.5*1998)
#pic_size_x = 1413
#pic_size_y = 734

#This specifies the angle of the viewing wedge - doesn't need to be exact
#This just tells the program only to read in files whose position tags
#are within this angle of the orientation vector (the direction the camera is pointing)
#I usually just leave it at pi/2, which just excludes files which are behind the camera
view_angle = pi/2

##########################################################################
#make a unit vector giving the direction the camera is pointing
orient = np.array([a3(x0[0], x0[1], x0[2]), b3(x0[0], x0[1], x0[2]), c3(x0[0], x0[1], x0[2])])
orient = np.sign(x0[6])*orient * (sqrt(orient[0]**2 + orient[1]**2 + orient[2]**2)**(-1))
#I should mention that I multiply the orientation vector by the sign of the focal length,
#as sometimes the camera location algorith locates the camera but has it face the opposite direction
#since this is an equally valid solution of the colin equations
#multiplying by the focal length sign ensures that we're always pointing in the proper direction

#determine elements of the rotation matrix - see colinearity equations for details
r = [[0,0,0],[0,0,0],[0,0,0]]
r[0][0] = a1(x0[0], x0[1], x0[2])
r[1][0] = b1(x0[0], x0[1], x0[2]) 
r[2][0] = c1(x0[0], x0[1], x0[2])
r[0][1] = a2(x0[0], x0[1], x0[2])
r[1][1] = b2(x0[0], x0[1], x0[2])
r[2][1] = c2(x0[0], x0[1], x0[2])
r[0][2] = a3(x0[0], x0[1], x0[2])
r[1][2] = b3(x0[0], x0[1], x0[2])
r[2][2] = c3(x0[0], x0[1], x0[2])



#specify the shape of the desired image array
s= (2*pic_size_y, 2*pic_size_x)


#########################################################################
#Next, we define a set of functions that govern most of the program


#These take a point's x, y, z coordinates, and maps them to the corresponding pixel in the generated image
#Details on colinx and coliny, along with the rotation matrix functions above, are in Colin.py
def pixel_x(XA, YA, ZA):
    out = colinx(r, x0, XA, YA, ZA)
    return out.astype(int)


def pixel_y(XA, YA, ZA):
    out = coliny(r, x0, XA, YA, ZA)
    return out.astype(int)


#This gives the distance between a given (x,y,z) and the camera position - nothing too fancy
def distance(x, y, z):
    return 1.*((x - x0[3])**2 + (y - x0[4])**2 + (z - x0[5])**2)**0.5


#returns TRUE if the angle between the ray from the camera to a point (x,y,z)
#and the camera orientation vector is less than the view angle
#In other words, this checks to see if a given point is within the vision cone
def orientation_angle(x, y, z):
    vec = np.array([x - x0[3], y - x0[4], z - x0[5]])
    vec = vec / distance(x, y, z)
    dot = vec[0]*orient[0] + vec[1]*orient[1] + vec[2]*orient[2]
    return np.arccos(dot) < view_angle
        


#check to make sure point is in image - that is, if it gets mapped to a pixel
#within the specified x and y sizes of the image
def onscreen(x, y):
    return (x< 2*pic_size_x)*(x > 0)*(y > 0)*(y < 2*pic_size_y)

#This is the big function - it takes a file, and gives you the desired projection
#The input is a string, the name of a .npy file containing lidar data
def project(filename):  
    dat = np.load(filename) #load up the Lidar file

    #define 3 numpy arrays to store our projections
    distgrid = np.ones(s)*(100000.)  #this stores distance to camera
    xgrid =  -1.*np.ones(s) #this will store the lidar x coordinate of that pixel
    ygrid = -1.*np.ones(s)  #this will store the lidar y coordinate of that pixel

    #first, in a vectorized fashion check to see which points are in the vision cone
    vis = orientation_angle(dat[0], dat[1], dat[2])
    if (vis == 0).all(): 
        return [distgrid, xgrid, ygrid] #if nothing is visible just return the blank arrays

    #create a vector containing the pixel_x and pixel_y coordinate of each point
    x = pic_size_x - pixel_x( dat[0], dat[1], dat[2])
    y = pic_size_y + pixel_y(dat[0], dat[1], dat[2])

    #now check to see which points are actually on the image we want
    #note that we basically have two checks on visibility - one checking to see if
    #we match pixel bounaries, and the other checking the angle
    #while the pixel boundary check is stronger, it can give false positives as
    #the colin equations will map points directly behind the camera onto the image
    vis = vis*onscreen(x, y)
    if (vis == 0).all():
        #again, if nothing is onscreen return the blank arrays
        return [distgrid, xgrid, ygrid]
    
    #calculate the distance of each point to the camera
    n = distance(dat[0], dat[1], dat[2])

    #now, add each point to the arrays, as long as it is visibile (vis[i] == 1)
    #and it is closer to the camera than the current value stored in the corresponding pixel
    #of the distance array
    for i in range(0, len(n)):
        if vis[i] == 1 and n[i] < distgrid[y[i]][x[i]]:
            distgrid[y[i]][x[i]] = n[i]
            xgrid[y[i]][x[i]] = dat[0][i]
            ygrid[y[i]][x[i]] = dat[1][i]   

    print filename
    return [distgrid, xgrid, ygrid]  #return an array of our three arrays


## ###########################################################################
#This is an experimental function that should allow us to parallelize the BBL finding
#process, dramatically speading up the entire procedure. Didn't have time to test it out or debug
#since we never got geopandas installed on compute. The basic idea, though, is that we match buildings
#to BBLs on a LIDAR tile basis. That is, for each lidar npy file, we first use project above to create our
#mock images. Then we takes those arrays, and the filename of the file, and plug them into this function.
#Load up MapPluto,
#then select out all buildings that are within or intersect with the Lidar tile
#then, for each point in the projection arrays, compute the relevant BBL


def BBL(filename, dat):
    x = dat[0]
    y = dat[1]
    dist = dat[2]
    file_y = int(line[4:8])*100

    file_x = int(line[0:4])
    if file_x < 1000:
        file_x = file_x + 1000

    bblgrid = np.zeros(dat[0].shape)
    manhattan = GeoDataFrame.from_file('Manhattan/MNMapPLUTO.shp')

    #crop the tile you're looking at according to tile dimensions
    tile_square = Polygon([(file_x, file_y), (file_x + 4000, file_y ), (file_x + 4000, file_y + 4000), (file_x, file_y + 4000)])
    select = manhattan.intersects(tile_square)

    manhattan = manhattan[select]
    xmax = len(x)
    ymax = len(x[0])
    for i in range(0, xmax):
        print i, xmax
        for j in range(0, ymax):
            if x[i][j] != -1:
                xi = x[i][j]
                yi = y[i][j]
                shape = (Point(xi, yi))
                intersect = man_cut.contains(shape)
                if any(intersect == True):
                    building = man_cut[intersect]
                    bblgrid[i][j] = int(building.BBL)


    return bblgrid


#So, this function will merge together two arrays of arrays of the form output by project,
#such that the final array will match at each pixel whichever of the original arrays is closer at that pixel
def merge(final, new):
    
    out = [0, 0, 0]
    replace = np.greater(final[0], new[0])
    out[0] = final[0]*np.logical_not(replace) + new[0]*replace
    out[1] = final[1]*np.logical_not(replace) + new[1]*replace
    out[2] = final[2]*np.logical_not(replace) + new[2]*replace
    return out

#Sets up the parallel operation of the code
def project_parallel(file_list):
    pool = mp.Pool()
    pic_slices = pool.map(project, file_list)
    pool.close()
    pool.join()
    return pic_slices
##############################################################################
#This section details the main script

#first, we define an array containing three numpy arrays of the desired shape and size
final_grids = [np.ones(s)*(10**8), -1*np.ones(s), -1*np.ones(s)]
file_list = [] #this stores the total set of viewable filenames
maxj = len(sys.argv[1:])  #total number of files to read
print 'Total files: ' + str(maxj)

#begin a for loop which runs over the set of input files, reading data from each
for line in sys.argv[1:]:

    #the names of the lidar files contain the x and y coordinates of their southwest point
    #we use this to rule out files obviously outside of the field of view
    file_y = int(line[4:8])*100
    file_x = int(line[0:4])
    if file_x < 1000:
        file_x = file_x + 1000 #files whose x values start with 0 actually begin 10
    file_x = file_x*100

    #vect is a unit vector from the camera to this coordinates point
    vect = np.array([file_x - x0[3], file_y - x0[4]])
    distance_to_cam = np.linalg.norm(vect)
    vect = vect / distance_to_cam
    #if the camera angle smaller than 0.8 rad, read the datafile 
    if acos(vect[0]*orient[0] + vect[1]*orient[1]) < 1.5 or distance_to_cam < 5000:
        file_list.append(line)

print 'done with selecting files'
#parallel computation of each file's projection
projected_tiles = project_parallel(file_list) #this starts the process by which all selected files will be analyzed in parallel
for tile in projected_tiles:
        #merge together all of our outputs into a single file
        final_grids = merge(final_grids, tile)

###cascade to fill holes by covering a given point if there is a closer point above it
for i in range(0, len(final_grids[0])-1):
    for j in range(0, len(final_grids[0][0])):
        if final_grids[0][i][j] < final_grids[0][i + 1][j]:
            final_grids[0][i+1][j] = final_grids[0][i][j]
            final_grids[1][i+1][j] = final_grids[1][i][j]
            final_grids[2][i+1][j] = final_grids[2][i][j]

#save data 
np.save(name + '_distgrid', final_grids[0])
np.save(name + '_xgrid', final_grids[1])
np.save(name + '_ygrid', final_grids[2])
