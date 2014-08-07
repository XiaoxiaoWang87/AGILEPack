"""
Building block for multi layered 
acyclic computation graphs.
"""

from gnumpy import dot as gdot
from gnumpy import zeros as gzeros
import gnumpy as gpu
import numpy as np
import sys
from ..utils.activation import *


class Layer(object):
    '''
    Layer class which will hold W, b, and activation function. Provides
    a base for more intricate network building blocks. A layer represents
    a connected, acyclic, bipartite graph.

    A layer is a mapping from a N dimensional space to a M dimensional
    space. 

    Attrbutes
    ---------

    W: an M x N numpy.matrix

    b: an M x 1 numpy.matrix

    Methods
    -------

    load(self, filename): 
        loads a neural network

    predict(self, data): 
        when passed a {record, structured} array, provides predictions.

    apply_binning(self, data):
        Applies the binning specified in the network file loaded to 'data',
        and returns a record array with the appropriate fields appended.
    '''
    def __init__(self, shape, activ, dropout = None, parameters = None, **kwargs):
        super(Layer, self).__init__()
        self.activ = activ
        if parameters is not None:
            self.parameters = parameters
        else:
            self.parameters = {'learning' : 0.0003, 'momentum' : 0.8, 'regularizer' : 0}
        
        self.W = np.matrix(np.random.randn(shape[1], shape[0]) * 0.1)
        self._prev_W = np.matrix(np.zeros((shape[1], shape[0])))
        self.b = np.matrix(np.random.randn(shape[1], 1) * 0.1)
        self._prev_b = np.matrix(np.zeros((shape[1], 1)))

    @classmethod
    def from_tuple(cls, par):
        _tmp = cls(par[0].shape[::-1], par[2])
        _tmp.W, _tmp.b = par[0], par[1]
        return _tmp

    def forward(self, data):
        return self.activ(np.dot(self.W, data) + self.b)

    def forward_prop(self, data):
        self.data = data
        self.activations = self.activ(np.dot(self.W, data) + self.b)
        return self.activations

    def back_prop(self, grad): # need grad.transpose()
        self.delta = np.multiply(grad, derivative[self.activ](self.activations))
        self.delta_W = np.dot(self.delta, self.data.transpose())
        self.delta_b = self.delta
        del self.data
        del self.activations
        return np.dot(self.W.transpose(), self.delta)

    def update(self):
        self._prev_W = self.parameters['momentum'] * self._prev_W - self.parameters['learning'] * (self.delta_W + self.parameters['regularizer'] * self.W)
        self._prev_b = self.parameters['momentum'] * self._prev_b - self.parameters['learning'] * (self.delta_b)
        self.W += self._prev_W
        self.b += self._prev_b

        



# for i in xrange(0,200):
#     predicted = layer.forward_prop(inputs); _ = layer.back_prop(predicted - targets); layer.update()

# layer1 = Layer((5, 3), activ = sigmoid, parameters={'learning' : 0.01, 'momentum' : 0.7, 'regularizer' : 0.0000001})
# layer2 = Layer((3, 1), activ = identity, parameters={'learning' : 0.01, 'momentum' : 0.7, 'regularizer' : 0.0000001})


# arch = [layer1, layer2]




# layer1 = Layer((5, 6), activ = sigmoid, parameters={'learning' : 0.01, 'momentum' : 0.7, 'regularizer' : 0.0000001})
# layer2 = Layer((6, 3), activ = sigmoid, parameters={'learning' : 0.01, 'momentum' : 0.7, 'regularizer' : 0.0000001})
# layer3 = Layer((3, 1), activ = identity, parameters={'learning' : 0.01, 'momentum' : 0.7, 'regularizer' : 0.0000001})


# arch = [layer1, layer2, layer3]


# def predict(arch, data): #data should be transposed
#     for layer in arch:
#         data = layer.forward_prop(data)
#     return data


# def correct(arch, data, targets, epochs = 15):
#     for i in range(0,epochs * data.shape[0]):
#         sel = np.random.randint(0,data.shape[0],1)
#         error = predict(arch, data[sel, :].T) - targets[sel, :].T
#         for layer in arch[::-1]:
#             error = layer.back_prop(error)
#             layer.update()

#         sys.stdout.write('\rTraining {}% complete.'.format(np.int((float(i) / (epochs * data.shape[0])) * 100)))
#     return arch

# for i in xrange(1,100):
#     sel = np.random.randint(0,X.shape[0],2)
#     arch = correct(arch, X[sel, :].transpose(), Y[sel].transpose())



# def train(arch, data, targets, epochs):
#     pass



# for i in xrange(1,3000):
#     sel = np.random.randint(0,4,2)
#     d = layer2.back_prop(layer2.forward_prop(layer1.forward_prop(X[sel, :].transpose())) - y[sel].transpose())
#     _ = layer1.back_prop(d)
#     layer1.update()
#     layer2.update()


# for i in xrange(1,100):
#     for x in xrange(0,2):
#         d = layer2.back_prop((layer2.forward_prop(layer1.forward_prop(inputs[x:x+2, :])) - targets[x:x+2, :]).transpose())
#         _ = layer1.back_prop(d)
#         layer1.update()
#         layer2.update()
    



            



#             