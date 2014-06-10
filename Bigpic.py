import numpy as np
from math import *
from Colin import *
import os
from liblas import file


x0 = np.array([  1.56438037e+00,  -1.23837300e-01,  -6.41605361e-04,
         9.87577881e+05,   1.89663330e+05,   5.08956767e+02,
        -1.22777347e+04]) 

orient = np.array([c1(x0[0], x0[1], x0[2]), c2(x0[0], x0[1], x0[2]), c3(x0[0], x0[1], x0[2])])


orient = orient / sqrt(orient[0]**2 + orient[1]**2 + orient[2]**2)  #normalized direction vector

#determine if given las file is in wedge

x_list = []
y_list = []
norm_list = []

direct = '/home/cusp/pwm267/las/'
#filelist = os.listdir('/projects/cusp/10019/0/LAS_Classified_All_Returns')

filelist = os.listdir(direct)

for filename in filelist:
    #figurout basic coordinate of picture
    file_x = int(filename[0:3])*1000
    file_y = int(filename[4:7])*1000
    vect = np.array([file_x - x0[3], file_y - x0[4]])
    vect = vect / np.linalg.norm(vect)
    #check to make sure in wedge
    if acos(vect[0]*orient[0] + vect[1]*orient[1]) and vect[1] > 0:
        f = file.File(direct + filename, mode = 'r')
        i = 0
        for p in f:
            i += 1
            if i % 10000:
                print p.x, p.y, p.z
                x_list.append(pack_col_x(x0, p.x, p.y, p.z))
                y_list.append(pack_col_y(x0, p.x, p.y, p.z))
                norm_list.append((p.x - x0[3])**2 + (p.y - x0[4])**2 + (p.z - x0[5])**2)

    
out = open('picdat.txt', 'w')

for j in range(0, len(x_list)):
    out.write(str(x_list[j]) + "\n")
    out.write(str(y_list[j]) + "\n")
    out.write(str(norm_list[j]) + "\n")

out.close()



