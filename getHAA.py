import numpy as np
from processDepthImage import processDepthImage


def fxn_getHAA(C, D, RD):
    # CAM_MATRIX, imgDenoisedDepth, imgRawDepth
    D = np.double(D)/1000 # Convert to millimeters
    missingMask = (RD == 0) # Indicate areas in the raw depth with no values

    pc, N, yDir, h, pcRot, NRot = processDepthImage(D*100, missingMask, C)
    angl = np.arcsin(np.rad2deg())
