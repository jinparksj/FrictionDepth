import numpy as np

def processDepthImage(z,missingMask,C):
"""
Args:
    z - Depth in centimeters
    missingMask - Boolean matrix with 1's where there are no values in the depth matrix
    C - Camera matrix
"""

    yDirParam.angleThresh = np.array([45,15])
    yDirParam.iter = np.array([5.5])
    yDirParam.y0 = np.array([[0],[1],[0]])

    normalParam.patchSize = np.array([3,10])

    X, Y, Z = getPointCloudFromZ(z, C, 1)
    pc = np.array([X, Y, Z])

# Compute the normals for this image
N1, b1 = computeNormalIsSquareSupport(z/100, missingMask, normalParam.patchSize[0], 1, C, np.ones(z.size))