import numpy as np
from processDepthImage import processDepthImage

def getHHA(C, D, RD):
    # CAM_MATRIX, imgDenoisedDepth, imgRawDepth

    # GETHHA Given a camera matrix, depth, and raw depth, get an "image" with HHA encoding.
    # Args:
    # C - Camera matrix
    # D - HxW Denoised depth matrix in meters
    # RD - HxW Raw depth matrix in meters

    D = np.double(D)/1000 # Convert to millimeters
    missingMask = (RD == 0) # Indicate areas in the raw depth with no values

    pc, N, yDir, h, pcRot, NRot = processDepthImage(D*100, missingMask, C)
    #N: 480 by 848 by 3, ydir = 3 by 1 -> 1 by 1 by 3??? 3 by 1 by 1
    angl = np.rad2deg(np.arccos(np.minimum(1, np.maximum(-1, np.sum( np.dot(N, yDir.reshape((3, 1, 1))), axis=2)))))

    pc[:, :, 2] = np.maximum(pc[:, :, 2], 100)
    rowSize = pc.shape[0]
    colSize = pc.shape[1]
    I = np.zeros((rowSize, colSize, 3))
    I[:, :, 0] = 31000 / pc[:, :, 2]
    I[:, :, 1] = h
    I[:, :, 2] = (angl + 128 - 90)
    HHA = np.uint8(I)

    return HHA























