import numpy as np
ok
def getRMatrix(yi,yf):
    # function R = getRMatrix(yi,yf)
    # Generates a rotation matrix that
    #   if yf is a scalar, rotates about axis yi by yf degrees
    #   if yf is an axis, rotates yi to yf in the direction given by yi x yf

    if np.isscalar(yf):
        ax = yi/np.linalg.norm(yi)
        phi = yf
    else:
        yi = yi/np.linalg.norm(yi)
        yf = yf/np.linalg.norm(yf)
        ax = np.cross(yi,yf)
        ax = ax/np.linalg.norm(ax)
        # Find angle of rotation
        # phi = acosd(abs(yi'*yf)) we dont need to take absolute value here
        phi = np.rad2deg(np.arccos(np.dot(np.transpose(yi)*yf)))

    if abs(phi) > 0.1:
        # ax = np.cross(yi,yf)
        # ax = ax/np.linalg.norm(ax)
        phi = phi*(np.pi/180)
        S_hat = np.array([[0,-ax[2],ax[1]],[ax[2],0,-ax[0]],[-ax[1],ax[0],0]])
        R = np.eye(3) + sin(phi)*S_hat + (1-cos(phi))*(S_hat^2)
    else:
        R = np.eye(3)

    return R