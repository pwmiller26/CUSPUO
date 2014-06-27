import arcpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from math import *


arcpy.env.workspace = "C:/Users/pwm267/Desktop/Manhattan"
arcpy.env.overwriteOutput = True


x = np.load('xgrid.npy')
y = np.load('ygrid.npy')
pixelgrid = np.load('pixgrid.npy')
bblgrid = -1*np.ones(x.shape)
unitdat = -1*np.ones(x.shape)
valdat =  -1*np.ones(x.shape)
rows = arcpy.SearchCursor("intersect_dat.shp")
for row in rows:
    #print row.posx, row.posy
    bblgrid[row.posx][row.posy] = row.BBL
    unitdat[row.posx][row.posy] = row.UnitsTotal
    valdat[row.posx][row.posy]  = row.AssessTot
    
print 'done with rows'

for i in range(1, len(pixelgrid) - 1):
    for j in range(1, len(pixelgrid[0]) - 1):
        if bblgrid[i][j - 1] == bblgrid[i][j + 1] and bblgrid[i][j] != bblgrid[i][j+1]:
            bblgrid[i][j] = bblgrid[i][j-1]
            unitdat[i][j] = unitdat[i][j-1]
            valdat[i][j]  = valdat[i][j-1]
            pixelgrid[i][j] = 0.5*(pixelgrid[i][j-1] + pixelgrid[i][j+1])
            

for i in range(1, len(pixelgrid) - 1):
    for j in range(1, len(pixelgrid[0]) - 1):
        if abs(pixelgrid[i][j - 1] - pixelgrid[i][j + 1]) < 500 and abs(pixelgrid[i][j] - pixelgrid[i][j+1])>500:
            bblgrid[i][j] = bblgrid[i][j-1]
            unitdat[i][j] = unitdat[i][j-1]
            valdat[i][j]  = valdat[i][j-1]
            pixelgrid[i][j] = 0.5*(pixelgrid[i][j-1] + pixelgrid[i][j+1])

#creates pixel array outlines which displaces edges of objects based on
#bbl
outline = np.zeros(pixelgrid.shape)
for i in range(0, len(pixelgrid) - 1):
    for j in range(0, len(pixelgrid[0]) - 1):
        if bblgrid[i][j]!= bblgrid[i + 1][j]:
            outline[i][j] = 1
            outline[i+1][j] = 1
            #outline[i+1][j] = 1
        elif bblgrid[i][j] != bblgrid[i][j+1]:
            outline[i][j] = 1
            outline[i][j+1] = 1




outline = np.ma.masked_where(outline != 1, outline)
