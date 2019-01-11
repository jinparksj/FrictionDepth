#ITS TEST COMMIT FROM HARRY

import numpy as np
from getHHA import getHHA
from readNPY import readNPY
from fillDepthColorization import fillDepthColorization


# ====================
#   Settings
# ====================
# Data directory
DATA_DIR = 'data/'

# File to load
DATA_NO = 1
DATA_PREFIX = ['lab', 'chair_bed']
DATA_PREFIX = DATA_PREFIX[DATA_NO]

# Display parameters
BOOL_SUBPLOT = True

 # Algorithm and camera parameters
ALPHA = 1 # Denoising parameter
DEPTH_SCALE = 0.0001 # Depth scale used during data recording
FOCAL = 498.0; # Focal length used during data recording
CAM_MATRIX = [[FOCAL, 0, 0], [0, FOCAL, 0], [0, 0, 1]] # Camera matrix

#DONE FOR JIN's PART
#FROM ==============================================
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

# imgDenoisedDepth = fillDepthColorization(imgRgb, imgRawDepth, ALPHA)

#TO ==============================================


#For testing!
imgDenoisedDepth = np.load('data/testdata.npy')

print('working end')
# HHA = getHAA(CAM_MATRIX, imgDenoisedDepth, imgRawDepth)


