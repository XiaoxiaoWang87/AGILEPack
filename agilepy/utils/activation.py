import numpy as np
from numpy.lib import recfunctions

def sigmoid(x):
    '''
    Calculates sigmoid non-linearity 1 / (1 + e^(-x)) for any 'x' such np.exp(x) is defined. 
    '''
    return 1 / (1 + np.exp(-x))

def d_sigmoid(x):
    '''
    Calculates x * (1 - x) element wise.
    '''
    return np.multiply(x, (1 - x))


def softmax(x, axis = 0):
    '''
    Induces a discrete probability distribution over an exponentially weighted 'x'. Defined for any 'x' such that np.exp(x) is valid.
    The softmax is taken in the 'axis' direction.
    '''
    if axis == 0:
        return np.exp(x) / np.exp(x).sum(0).tile((x.shape[0], 1))

    elif axis == 1:
        return np.exp(x) / np.exp(x).sum(axis=1).reshape(x.shape[0], 1)


def identity(x):
    '''
    Placeholder for the identity function.
    '''
    return x

def d_identity(x):
    return 1


derivative = { sigmoid : d_sigmoid,
               identity : d_identity,
               softmax : d_identity }


