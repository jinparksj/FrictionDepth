"""
Preprocesses the kinect depth image using a gray scale version of the RGB image
as a weighting for the smoothing. This code is a slight
adaption of Anat Levin's colorization code:

See: www.cs.huji.ac.il/~yweiss/Colorization/

Args:
    imgRgb - H x W x 3 matrix, the rgb image for the current frame. This must be between 0 and 1.
    imgDepth - H x W matrix, the depth image for the current frame in absolute (meters) space.
    alpha - a penalty value between 0 and 1 for the current depth values.
"""

import numpy as np
from scipy.sparse import csr_matrix, csc_matrix
from scipy.sparse import linalg
from scipy import sparse
from numba import jit


@jit(parallel=True, nogil=True)
def jitforloop(W, H, absImgNdx, winRad, rows, cols, vals, gvals, indsM, grayImg, len):
    for j in range(W):
        for i in range(H):


            nWin = 0 #Count the number of points in the current window
            for ii in np.arange(np.max([0, i - winRad]), np.min([i + winRad, H - 1]) + 1, 1):
                for jj in np.arange(np.max([0, j - winRad]), np.min([j + winRad, W - 1]) + 1, 1):
                    if ii == i and jj == j:
                        continue

                    rows[len] = absImgNdx
                    cols[len] = indsM[ii, jj]
                    gvals[nWin] = grayImg[ii, jj]

                    len = len + 1
                    nWin = nWin + 1


            curVal = grayImg[i, j]
            gvals[nWin] = curVal
            c_var = np.mean((gvals[0:nWin+1] - np.mean(gvals[0:nWin+1])) ** 2)

            csig = c_var * 0.6
            mgv = np.min(((gvals[0:nWin] - curVal)) ** 2)
            if csig < ( -mgv / np.log(0.01)):
                csig = -mgv / np.log(0.01)

            if csig < 0.000002:
                csig = 0.000002

            gvals[0:nWin] = np.exp( -(gvals[0:nWin] - curVal) ** 2 / csig)
            gvals[0:nWin] = gvals[0:nWin] / np.sum(gvals[0:nWin])
            vals[len-nWin:len] = -gvals[0:nWin]

            #Now the self-reference (along the diagonal)

            rows[len] = absImgNdx
            cols[len] = absImgNdx
            vals[len] = 1 #sum(gvals(1:nWin))
            len = len + 1
            absImgNdx = absImgNdx + 1


    return W, H, absImgNdx, winRad, rows, cols, vals, gvals, indsM, grayImg, len



def fillDepthColorization(imgRgb, imgDepth, alpha=1):

    # Check for potential noise in the depth image
    imgIsNoise = np.logical_or(imgDepth == 0, imgDepth == 10)
    maxImgAbsDepth = np.max(imgDepth[~imgIsNoise])
    imgDepth = imgDepth / maxImgAbsDepth #Normalize
    imgDepth = np.clip(imgDepth, None, 1) #Double check normalization

    #assert(ismatrix(imgDepth));
    H = imgDepth.shape[0]
    W = imgDepth.shape[1]

    nPixels = H * W

    indsM = np.arange(0, nPixels, 1).reshape((H, W), order='F')

    knownValMask = ~imgIsNoise

    grayImg = np.ones((imgRgb.shape[0], imgRgb.shape[1])) #NEED TO CHECK!!!!!!!!!!!!!!!!!!

    winRad = 1

    len = 0
    absImgNdx = 0
    cols = np.zeros((nPixels * (2*winRad + 1)**2, ))
    rows = np.zeros((nPixels * (2*winRad + 1)**2, ))
    vals = np.zeros((nPixels * (2*winRad + 1)**2, ))
    gvals = np.zeros(((2 * winRad + 1) ** 2, ))

    #JIT FOR LOOP for Accelerating / NEED TO OPTIMIZE IT
    W, H, absImgNdx, winRad, rows, cols, vals, gvals, indsM, grayImg, len = jitforloop(W, H, absImgNdx, winRad, rows, cols, vals, gvals, indsM, grayImg, len)

    vals = vals[0:len]
    cols = cols[0:len]
    rows = rows[0:len]

    A = csr_matrix((vals, (np.int64(rows), np.int64(cols))), shape = (nPixels, nPixels))

    rows = np.arange(0, knownValMask.size, 1)
    cols = np.arange(0, knownValMask.size, 1)
    vals = knownValMask.flatten(order=1) * alpha
    G = csr_matrix((vals, (np.int64(rows), np.int64(cols))), shape = (nPixels, nPixels))


    new_vals = linalg.spsolve((A + G), (vals * imgDepth.flatten(order=1))).reshape(H, W, order='F')

    denoisedDepthImg = new_vals * maxImgAbsDepth


    return denoisedDepthImg
