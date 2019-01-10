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

# def rgb2gray(rgb):
#     R = rgb[:, :, 0]
#     G = rgb[:, :, 1]
#     B = rgb[:, :, 2]
#     Gray = R * 0.2989 + G * 0.587 + B * 0.114
#     Gray = np.min([np.max([Gray, 0]), 1])
#     Gray =
#
#     return Gray

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
    cols = np.zeros((nPixels * (2*winRad + 1)**2, 1))
    rows = np.zeros((nPixels * (2*winRad + 1)**2, 1))
    vals = np.zeros((nPixels * (2*winRad + 1)**2, 1))
    gvals = np.zeros((1, (2 * winRad + 1) ** 2))

    for j in range(W):
        for i in range(H):
            absImgNdx = absImgNdx + 1

            nWin = 0 #Count the number of points in the current window
            for ii in np.arange(np.max([0, i - winRad]), np.min([i + winRad, H]), 1):
                for jj in np.arange(np.max([0, j - winRad]), np.min([j + winRad, W]), 1):
                    if ii == i and jj == j:
                        continue

                    print(ii, jj)

                    rows[len] = absImgNdx
                    cols[len] = indsM[ii, jj]
                    gvals[nWin] = grayImg[ii, jj]

                    len = len + 1
                    nWin = nWin + 1


            curVal = grayImg[i, j]
            gvals[nWin + 1] = curVal
            c_var = np.mean()




    # return denoisedDepthImg
