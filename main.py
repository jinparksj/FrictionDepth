#ITS TEST COMMIT FROM HARRY

import numpy as np
# from getHHA import getHHA
from readNPY import readNPY
from fillDepthColorization import fillDepthColorization


DATA_DIR = 'data/'

DEPTH_SCALE = 0.0001 #Depth Scale used during data recording
ALPHA = 1 #Denoising parameter

#load RGB
filename = 'data/chair_bed_rgb.npy'
imgBgr = readNPY(filename)

imgRgb = np.zeros_like(imgBgr)
imgRgb[:, :, 0] = imgBgr[:, :, 2]
imgRgb[:, :, 1] = imgBgr[:, :, 1]
imgRgb[:, :, 2] = imgBgr[:, :, 0]
imgRgb = np.double(imgRgb)

#Load depth
filename_depth = 'data/chair_bed_depth.npy'
imgRawDepth = readNPY(filename_depth)
imgRawDepth = np.double(imgRawDepth)
imgRawDepth = imgRawDepth * DEPTH_SCALE

#Create HHA

imgDenoisedDepth = fillDepthColorization(imgRgb, imgRawDepth, ALPHA)


