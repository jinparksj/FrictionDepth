from readNPYheader import readNPYheader
import numpy as np

def readNPY(filename):
    shape, dataType, fortranOrder, littleEndian, totalHeaderLength, _ = readNPYheader(filename)
    #NEED TO DEBUG for Little Endian
    with open(filename, 'rb') as f:
        try:
            if littleEndian:#little endian
                header = np.fromfile(f, count=totalHeaderLength * 1, dtype='<u1')
                header = header.reshape((totalHeaderLength,))
            else: #big endian
                header = np.fromfile(f, count=totalHeaderLength * 1, dtype='>u1')
                header = header.reshape((totalHeaderLength,))

            data_count = np.prod(shape)
            data = np.fromfile(f, count=data_count, dtype=dataType)
            data = data.reshape((data_count, ))

            if (len(shape) > 1 and not fortranOrder):
                if 'rgb' in filename:
                    data = data.reshape((shape[2], shape[1], shape[0]))
                    data = np.transpose(data, (len(shape) -1, 1, 0))
                elif 'depth' in filename:
                    data = data.reshape((shape[1], shape[0]))
                    data = np.transpose(data, (len(shape) -1, 0))
            elif len(shape) > 1:
                data = data.reshape(shape)

            return data

        except:
            f.close()
            print('error')
            return None
















