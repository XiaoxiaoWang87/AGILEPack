import numpy as np
import gnumpy as gpu


def rec_to_gpu(rec):
	if rec.dtype.names is not None:
		rec = rec.astype([(k, np.float32) for k in rec.dtype.names])
		return gpu.garray(rec.view((np.float32, len(rec.dtype.names))))
	else:
		# rec = rec.astype(np.float32)
		return gpu.garray(rec.astype(np.float32))

def rec_to_mat(rec):
	if rec.dtype.names is not None:
		rec = rec.astype([(k, np.float64) for k in rec.dtype.names])
		return np.mat(rec.view((np.float64, len(rec.dtype.names))))
	else:
		# rec = rec.astype(np.float64)
		return np.matrix(rec.astype(np.float64))


def scale(arr, scaling):
    for key in scaling['mean'].keys():
        arr[key] = (arr[key] - scaling['mean'][key]) / scaling['sd'][key]
    return arr

def destringify(nrow, ncol, string):
    M = np.zeros(shape=(nrow, ncol))
    data = [float(num) for num in string[(string.find(',') + 1):].split(',')]
    for i in range(0, nrow):
        for j in range(0, ncol):
            M[i, j] = data[i * ncol + j]
    return np.matrix(M)