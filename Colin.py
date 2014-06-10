from math import *
import numpy as np


def a1(omega, phi, k):
    return cos(phi)*cos(k) 

def b1(omega, phi, k):
    return cos(omega)*sin(k) + sin(omega)*sin(phi)*cos(k)

def c1(omega, phi, k):
    return sin(omega)*sin(k) - cos(omega)*sin(phi)*cos(k)

def a2(omega, phi, k):
    return -1 * cos(phi)*sin(k)

def b2(omega, phi, k):
    return cos(omega)*cos(k) - sin(omega)*sin(phi)*sin(k)

def c2(omega, phi, k):
    return sin(omega)*cos(k) + cos(omega)*sin(phi)*sin(k)

def a3(omega, phi, k):
    return sin(phi)

def b3(omega, phi, k):
    return -1*sin(omega)*cos(phi)

def c3(omega, phi, k):
    return cos(phi)*cos(omega) 

def colinx(A1, B1, C1, A3, B3, C3, XS, YS, ZS, XA, YA, ZA, f):

    return -f * (A1*(XA - XS) + B1*(YA - YS) + C1*(ZA - ZS)) \
           / (A3*(XA-XS) + B3*(YA - YS) + C3*(ZA - ZS))

def coliny(A2, B2, C2, A3, B3, C3, XS, YS, ZS, XA, YA, ZA, f):
    return -f * (A2*(XA - XS) + B2*(YA - YS) + C2*(ZA - ZS)) \
           / (A3*(XA-XS) + B3*(YA - YS) + C3*(ZA - ZS))

def pack_col_x(x, X, Y, Z):
    return -1*colinx(a1(x[0], x[1], x[2]), b1(x[0], x[1], x[2]), c1(x[0], x[1], x[2]), \
                  a3(x[0], x[1], x[2]), b3(x[0], x[1], x[2]), c3(x[0], x[1], x[2]), \
                  x[3], x[4], x[5], X, Y, Z, x[6])

def pack_col_y(x, X, Y, Z):
    return -1*coliny(a2(x[0], x[1], x[2]), b2(x[0], x[1], x[2]), c2(x[0], x[1], x[2]), \
                  a3(x[0], x[1], x[2]), b3(x[0], x[1], x[2]), c3(x[0], x[1], x[2]), \
                  x[3], x[4], x[5], X, Y, Z, x[6])
