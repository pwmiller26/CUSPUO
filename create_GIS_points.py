import arcpy
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from math import *


arcpy.env.workspace = "C:/Users/pwm267/Desktop/Manhattan/"
arcpy.env.overwriteOutput = True
featureClass = "MNMapPLUTO.shp"
#arcpy.MakeFeatureLayer_management('MNMapPLUTO.shp', 'citylayer')
x = np.load('xgrid.npy')
y = np.load('ygrid.npy')
pixelgrid = np.load('pixgrid.npy')

print 'loaded'

xmax = len(x)
ymax = len(x[0])

arcpy.CreateFeatureclass_management(arcpy.env.workspace, 'data.shp', "POINT") 
arcpy.AddField_management('data.shp', 'posx', 'LONG')
arcpy.AddField_management('data.shp', 'posy', 'LONG')
arcpy.AddField_management('data.shp', 'cam_dist', 'LONG')

array = []
rows = arcpy.InsertCursor('data.shp')
id = 1
for i in range(0, xmax):
    for j in range(0, ymax):
        row = rows.newRow()
        row.posx = i
        row.posy = j
        row.cam_dist = pixelgrid[i][j]
        row.Shape = arcpy.Point(x[i][j], y[i][j])
        rows.insertRow(row)
        id += 1
    print i, xmax

del row
del rows
arcpy.Intersect_analysis(['citylayer', 'data.shp'], 'intersect_dat')
