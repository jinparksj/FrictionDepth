import numpy as np

def getYDir(N, yDirParam):
    # function y = getYDir(N, yDirParam)

    # Input:
    #   N:          normal field
    #   yDirParam:  parameters
    #               struct('y0', [0 1 0]', 'angleThresh', [45 15], 'iter', [5 5])

    # Output:
    #   y:          Gravity direction

    y = yDirParam.y0

    for i in range(yDirParam.angleThresh.shape[0])
        y = getYDirHelper(N, y, yDirParam.angleThresh[i], yDirParam.iter[i])

    return y

def getYDirHelper(N, y0, thresh, iter):
    # function yDir = getYDirHelper(N, y0, thresh, iter)

    # Input:
    #   N: HxWx3 matrix with normal at each pixel
    #   y0: the initial gravity direction
    #   thresh: in degrees the threshold for mapping to parallel to gravity and perpendicular to gravity
    #   iter: number of iterations to perform

    # Output:
    #   yDir: the direction of gravity vector as inferred

    nn =