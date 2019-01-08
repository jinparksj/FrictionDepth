import numpy as np
import os
import sys
import cv2



# def fxn_readNPYheader(filename):
filename = "data/lab_rgb.npy"
fid = np.load(filename)

if (fid.size == -1):
    if len(os.path.dirname(filename)):
        print('Permission Denied: %s' % (filename))
        # return None
    else:
        print('File not found: %s' % (filename))
        # return None

try:
    dtypesPYTHON = ['uint8', ]




