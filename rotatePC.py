import numpy as np

def rotatePC(pc,R):
    # function tmp = rotatePC(pc,R)

    if R == np.eye(3):
        tmp = pc
    else:
        pc = np.transpose(pc,(2,0,1))
        tmp = pc.reshape((3, pc.size/3))
        tmp = np.dot(R,tmp)
        tmp = tmp.reshape(np.array(pc.shape))
        tmp = np.transpose(tmp,(1,2,0))
        pc = tmp

    return tmp