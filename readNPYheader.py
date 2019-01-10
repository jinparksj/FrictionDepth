import numpy as np
import re

def readNPYheader(filename):
    with open(filename, 'rb') as f:
        try:
            dtypesPYTHON = np.array(['uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'single',
                                     'double', 'logical'])
            dtypesNPY = np.array(['u1', 'u2', 'u4', 'u8', 'i1', 'i2', 'i4', 'i8', 'f4', 'f8', 'b1'])
            farray = np.fromfile(f, count=6 * 1, dtype='uint8')
            magicString = farray.reshape((6,))

            if not np.all(magicString == np.array([147, 78, 85, 77, 80, 89])):
                print('readNPY:NotNUMPYFile, Error: This file does not appear to be NUMPY format based on the header.')
                raise AssertionError()

            majorVersion = np.fromfile(f, count=1 * 1, dtype='uint8')
            majorVersion = majorVersion.reshape((1,))

            minorVersion = np.fromfile(f, count=1 * 1, dtype='uint8')
            minorVersion = minorVersion.reshape((1,))

            npyVersion = [majorVersion[0], minorVersion[0]]

            headerLength = np.fromfile(f, count=1 * 1, dtype='uint16')
            headerLength = headerLength.reshape((1,))[0]

            totalHeaderLength = 10 + headerLength

            arrayFormat = np.fromfile(f, count=headerLength * 1, dtype='S64')
            arrayFormat = str(arrayFormat.reshape((headerLength, 1))[0])
            # to interpret the array format infor, we make some faily strict assumptions about its format

            r_descr = re.compile(r"descr....(.\w+)")
            descr = r_descr.search(arrayFormat)
            dtNPY = descr.group(1)

            littleEndian = not ('>' in dtNPY)

            for i in range(len(dtypesNPY)):
                if dtNPY[1:] == dtypesNPY[i]:
                    dataType = dtypesPYTHON[i]

            r_fortran = re.compile(r"fortran_order...(\w+)")
            fortran = r_fortran.search(arrayFormat)
            fortran_sub = fortran.group(1)

            fortranOrder = (fortran_sub == True)

            if 'rgb' in filename:
                r_shape = re.compile(r"shape....(\d+)..(\d+)..(\d+)")
                shape = r_shape.search(arrayFormat)
                arrayShape = np.uint(shape.group(1, 2, 3))
            elif 'depth' in filename:
                r_shape = re.compile(r"shape....(\d+)..(\d+)")
                shape = r_shape.search(arrayFormat)
                arrayShape = np.uint(shape.group(1, 2))

            return arrayShape, dataType, fortranOrder, littleEndian, totalHeaderLength, npyVersion

        except:
            f.close()
            print('error')
            return None



