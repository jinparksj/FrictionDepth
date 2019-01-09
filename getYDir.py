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

    for i in range(yDirParam.angleThresh.shape[0]):
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

    nn = np.transpose(N,(2,0,1))
    nn = nn.reshape((3,nn.size/3))
    nn = nn[:,(~np.isnan(nn[1,:]))]

    # Set it up as a optimization problem

    yDir = y0;
    # Let us do hard assignments
    for i in range(iter):
        sim0 = np.dot(np.transpose(yDir),nn)
        indF = abs(sim0) > np.rad2deg(np.arccos(thresh))
        indW = abs(sim0) < np.rad2deg(np.arcsin(thresh))

        NF = nn[:,indF]
        NW = nn[:,indW]
        A = np.dot(NW,np.transpose(NW)) - np.dot(NF,np.transpose(NF))
        b = np.zeros((3,1))
        c = NF.shape[1]

        V,D = np.linalg.eig(A)
        gr = min(np.diag(D))
        ind = np.argmin(np.diag(D))
        newYDir = V[:,ind]
        yDir = newYDir*np.sign(np.dot(np.transpose(yDir),newYDir))

    return yDir