import numpy as np

def processDepthImage(z, missingMask, C):
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
    N1, b1 = computeNormalIsSquareSupport(z/100, missingMask, normalParam.patchSize[0], 1, C, np.ones(z.shape))
    N2, b2 = computeNormalIsSquareSupport(z/100, missingMask, normalParam.patchSize[1], 1, C, np.ones(z.shape))

    N = N1

    # Compute the direction of gravity
    yDir = getYDir(N2, yDirParam)
    y0 = np.transpose(np.array([0, 1, 0]))
    R = getRMatrix(y0, yDir)
    NRot = rotatePC(N, np.transpose(R))
    pcRot = rotatePC(pc, np.transpose(R))
    h = -pcRot[:, :, 1]
    yMin = np.percentile(h, 0, interpolation='midpoint')
    if yMin > -90:
        yMin = -130
    h = h - yMin

    return pc, N, yDir, h, pcRot, NRot
