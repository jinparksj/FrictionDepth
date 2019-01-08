from readNPYheader import readNPYheader
import numpy as np


def readNPY(filename):
    shape, dataType, fortranOrder, littleEndian, totalHeaderLength, _ = readNPYheader(filename)
    if littleEndian:
        fid = np.load(filename, )




