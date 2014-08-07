from layers.Layer import Layer
from utils.activation import *
from numpy.lib import recfunctions
import yaml
from utils.gputils import rec_to_mat

class NeuralNetwork(object):
    """docstring for NeuralNetwork"""
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.arch = []
        self.data = []
        self.has_branches = False
        self.has_inputs = False
        self.has_targets = False
        self.has_scaling = False
        self.has_outputs = False
        self.has_binning = False
        self.branches = None
        self.inputs = None
        self.binning = None
        self.outputs = None
        self.architecture = None
        self.X = None
        self.Y = None

    def add_layer(self, layer):
        if layer.__class__ == Layer:
            arch.append(layer)
        else:
            raise TypeError("Can only add opjects of class 'Layer' to a NeuralNetwork.")


    def set_inputs(self, input_list):
        if input_list.__class__ is not list:
            raise TypeError('Input list must be of type list.')
        if False in (cl.__class__ == str for cl in input_list):
            raise TypeError('Found non-string member of input list')
        self.inputs = input_list
        self.has_inputs = True

    def add_input(self, input_name):
        if input_name.__class__ is not str:
            raise TypeError('Input name must be a string')
        self.inputs.extend(input_name)
        self.has_inputs = True

    def set_outputs(self, output_list):
        if output_list.__class__ is not list:
            raise TypeError('output list must be of type list.')
        if False in (cl.__class__ == str for cl in output_list):
            raise TypeError('Found non-string member of output list')
        self.outputs = output_list
        self.has_targets = True

    def add_output(self, output_name):
        if output_name.__class__ is not str:
            raise TypeError('output name must be a string')
        self.outputs.extend(output_name)
        self.has_targets = True

    def predict(self, recarray):
        if self.has_scaling:
            z = rec_to_mat(_scale(recarray[self.inputs], self.scaling)).T
        else:
            z = rec_to_mat(recarray[self.inputs]).T
        for layer in self.arch:
            z = layer.forward(z)
        if self.has_targets:
            dtypes_out = [(name + '_predicted', '<f8') for name in self.outputs]
            return np.core.records.fromarrays(z, dtype = dtypes_out)[0]
        return z.T

    def load(self, filename):
        '''   
        '''
        self.has_branches = False
        self.has_inputs = False
        self.has_targets = False
        self.has_scaling = False
        self.has_outputs = False
        self.has_binning = False
        self.branches = None
        self.inputs = None
        self.binning = None
        self.outputs = None
        self.architecture = None
        with open(filename, 'r') as f:
            y = yaml.load(f.read())
        if y.has_key('branches'):
            self.branches = y['branches'].keys()
            self.has_branches = True

        if y['network'].has_key('input_order'):
            self.inputs = y['network']['input_order']
            self.has_inputs = True

        if y['network'].has_key('scaling'):
            self.scaling = y['network']['scaling']
            self.has_scaling = True

        if y.has_key('binning'):
            self.binning = y['binning']
            self.has_binning = True

        if y['network'].has_key('target_order'):
            self.outputs = y['network']['target_order']
            self.has_targets = True

        self.arch = [Layer.from_tuple(_layer_from_yaml(y['network'][idx])) for idx in y['network']['layer_access']]

    # def correct(self, data, targets, epochs = 15):
    #     for i in range(0,epochs * data.shape[0]):
    #         sel = np.random.randint(0,data.shape[0],1)
    #         error = predict(arch, data[sel, :].T) - targets[sel, :].T
    #         for layer in arch[::-1]:
    #             error = layer.back_prop(error)
    #             layer.update()

    #         sys.stdout.write('\rTraining {}% complete.'.format(np.int((float(i) / (epochs * data.shape[0])) * 100)))




def _scale(arr, scaling): 
    arr = arr.astype([(k, np.float64) for k in arr.dtype.names])
    for key in scaling['mean'].keys():
        # arr[key] = (arr[key].copy() - scaling['mean'][key]) / scaling['sd'][key]
        arr[key] -= scaling['mean'][key]
        arr[key] /= scaling['sd'][key]
    return arr

def _destringify(nrow, ncol, string):
    M = np.zeros(shape=(nrow, ncol))
    data = [float(num) for num in string[(string.find(',') + 1):].split(',')]
    for i in range(0, nrow):
        for j in range(0, ncol):
            M[i, j] = data[i * ncol + j]

    return np.matrix(M)

def _layer_from_yaml(d):
    W = _destringify(d['outputs'], d['inputs'], d['weights'])
    b = _destringify(d['outputs'], 1, d['bias'])

    if d['activation'] == 'sigmoid':
        f = sigmoid
    elif d['activation'] == 'linear':
        f = identity
    elif d['activation'] == 'softmax':
        f = softmax
    else:
        raise LookupError("activation function type \'{}\' not yet supported.".format(d['activation']))
    return [W, b, f]














