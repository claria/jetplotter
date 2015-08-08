import sys
import inspect
from parser import UserParser
import ROOT


class Module(object):
    def __init__(self):
        self.label = self.__class__.__name__
        self._parser = UserParser(add_help=False)
        self.parser = self._parser.add_argument_group(self.label)

    def __call__(self, **args):
        pass


def get_modules():
    ana_modules = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, Module):
            ana_modules.append(obj())
    return ana_modules


def get_module(name):
    thismodule = sys.modules[__name__]
    cls = getattr(thismodule, name)
    module = cls()
    return module


class RatioToObj(Module):
    def __init__(self):
        super(RatioToObj, self).__init__()
        self.parser.add_argument('--ratio', nargs='+', default=[], type='str2kvstr', help='')

    def __call__(self, config):
        for id, to in config['ratio']:
            print 'calc ratio', id, to
            if id not in config['settings']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['settings']:
                raise ValueError('Requested id {} not found.'.format(to))

            ratio_to_obj(config['settings'][id]['obj'], config['settings'][to]['obj'])


class SimpleRatioToObj(Module):
    def __init__(self):
        super(SimpleRatioToObj, self).__init__()
        self.parser.add_argument('--simpleratio', nargs='+', default=[], type='str2kvstr', help='')

    def __call__(self, config):
        for id, to in config['simpleratio']:
            print 'calc sratio', id, to
            if id not in config['settings']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['settings']:
                raise ValueError('Requested id {} not found.'.format(to))
            to_obj = config['settings'][to]['obj'].Clone('ref')
            for i in xrange(1, to_obj.GetNbinsX() + 1):
                to_obj.SetBinError(i, 0.)
            ratio_to_obj(config['settings'][id]['obj'], to_obj)


class MultiplyObj(Module):

    def __init__(self):
        super(MultiplyObj, self).__init__()
        self.parser.add_argument('--multiply', nargs='+', type='str2kvstr', action='setting', help='')

    def __call__(self, data):
        for id, item in data.items():
            if 'multiply' in item:
                to_id = item['multiply']
                if to_id not in data:
                    raise ValueError('Requested id {} not found.'.format(to_id))
                item['obj'].Multiply(data[to_id]['obj'])


class NormalizeObj(Module):
    def __init__(self):
        super(NormalizeObj, self).__init__()
        self.parser.add_argument('--scale-obj', nargs='+', default=[], type='str2kvstr', help='')

    def __call__(self, config):
        for id, val in config['scale_obj']:
            if not id in config['settings']:
                raise ValueError('Requested id {} not found.'.format(id))
            if val == 'width':
                config['settings'][id]['obj'].Scale(1.0, 'width')
            else:
                config['settings'][id]['obj'].Scale(1.0, float(val))


#
# Helper functions
#

def divide_tgraph(graph1, graph2, error_prop=False):
    assert (graph1.GetN() == graph2.GetN())
    for i in xrange(graph1.GetN()):
        graph1X, graph1Y = ROOT.Double(0), ROOT.Double(0)
        graph1.GetPoint(i, graph1X, graph1Y)
        graph2X, graph2Y = ROOT.Double(0), ROOT.Double(0)
        graph2.GetPoint(i, graph2X, graph2Y)

        graph1.SetPoint(i, graph1X, graph1Y / graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYlow(i, graph1.GetErrorYlow(i) / graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYhigh(i, graph1.GetErrorYhigh(i) / graph2Y if graph2Y != 0. else 0.)


def multiply_tgraph(graph1, graph2, error_prop=False):
    assert (graph1.GetN() == graph2.GetN())
    for i in xrange(graph1.GetN()):
        graph1X, graph1Y = ROOT.Double(0), ROOT.Double(0)
        graph1.GetPoint(i, graph1X, graph1Y)
        graph2X, graph2Y = ROOT.Double(0), ROOT.Double(0)
        graph2.GetPoint(i, graph2X, graph2Y)

        graph1.SetPoint(i, graph1X, graph1Y / graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYlow(i, graph1.GetErrorYlow(i) / graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYhigh(i, graph1.GetErrorYhigh(i) / graph2Y if graph2Y != 0. else 0.)


def normalize_to_obj(obj, ref_obj):
    obj.Scale(ref_obj.Integral() / objIntegral())


def ratio_to_obj(obj, ref_obj, error_prop=True):
    ref_obj = ref_obj.Clone('ref_obj')
    if error_prop is False:
        for i in xrange(1, ref_obj.GetNbinsX() + 1):
            ref_obj.SetBinError(i, 0.)
    obj.Divide(ref_obj)
