import argparse
import sys
import inspect
import core
import copy
from settings import AutoGrowListAction

def get_modules():
    ana_modules = []
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj) and issubclass(obj, AnaModule):
            ana_modules.append(obj())
    return ana_modules

def get_module(name):
    thismodule = sys.modules[__name__]
    cls = getattr(thismodule, name)
    module = cls()
    return module

class AnaModule(object):

    def __init__(self):
        _parser = core.UserParser(add_help=False)
        self.parser = _parser.add_argument_group(self.__class__.__name__)

    def get_parser(self):
        return parser_group

    def __call__(self, **args):
        pass

class RatioToObj(AnaModule):

    def __init__(self):
        super(RatioToObj, self).__init__()
        self.parser.add_argument('--ratio', nargs='+', type='str2kvstr', action='setting', help='')

    def __call__(self, data):
        for id, item in data.items():
            if 'ratio' in item:
                to_id = item['ratio']
                if not to_id in data:
                    raise ValueError('Requested id {} not found.'.format(to_id))
                ratio_container = copy.deepcopy(item)
                if not 'ratio_{0}'.format(id) in data: 
                    data['ratio_{0}'.format(id)] ={}
                data['ratio_{0}'.format(id)] = dict(ratio_container.items() + data['ratio_{0}'.format(id)].items())
                ratio_to_obj(ratio_container['obj'], data[to_id]['obj'])

class MultiplyObj(AnaModule):

    def __init__(self):
        super(RatioToObj, self).__init__()
        self.parser.add_argument('--multiply', nargs='+', type='str2kvstr', action='setting', help='')

    def __call__(self, data):
        for id, item in data.items():
            if 'multiply' in item:
                to_id = item['multiply']
                if not to_id in data:
                    raise ValueError('Requested id {} not found.'.format(to_id))
                item['obj'].Multiply(data[to_id]['obj'])




class SimpleRatioToObj(AnaModule):
    """Just divide by value, do not take into account errors of ref histo."""

    def __init__(self):
        super(SimpleRatioToFirstObj, self).__init__()
        self.parser.add_argument('--simpleratio-to', type=int, help='')

    def __call__(self, root_objects, **args):
        if not root_objects:
            return
        ref_obj = root_objects[0].Clone('ref_obj')
        for i in xrange(1, ref_obj.GetNbinsX() + 1):
            ref_obj.SetBinError(i, 0.)
        for obj in root_objects:
            obj.Divide(ref_obj)


class NormalizeObj(AnaModule):

    def __init__(self):
        super(NormalizeObj, self).__init__()
        self.parser.add_argument('--scale-objs',  nargs='+', default=[1.0],
                                       action=AutoGrowListAction,
                                       help='Scale each obj with factor')

    def __call__(self, root_objects, **args):
        for i, obj in enumerate(root_objects):
            if args['scale_objs'][i] == 'width':
                print "Scale", obj.GetName(), "with ", args['scale_objs'][i]
                obj.Scale(1.0, args['scale_objs'][i])
            else:
                print "Scale", obj.GetName(), "with ", args['scale_objs'][i]
                obj.Scale(float(args['scale_objs'][i]))

class NormalizeToObj(AnaModule):

    def __init__(self):
        super(NormalizeToObj, self).__init__()
        self.parser.add_argument('--scale-to',  nargs='+', default=[1.0],
                                       action=AutoGrowListAction,
                                       help='Scale each obj with factor')

    def __call__(self, root_objects, **args):
        for i, obj in enumerate(root_objects):
            if args['scale_to'][i] == -1:
                continue
            else:
                obj.Scale(root_objects[args['scale_to'][i]].Integral() / root_objects[i].Integral())


#
# Helper functions
#

def divide_tgraph(graph1, graph2, error_prop=False):
    assert(graph1.GetN() == graph2.GetN())
    for i in xrange(graph1.GetN()):
        graph1X, graph1Y = ROOT.Double(0), ROOT.Double(0)
        graph1.GetPoint(i, graph1X, graph1Y)
        graph2X, graph2Y = ROOT.Double(0), ROOT.Double(0)
        graph2.GetPoint(i, graph2X, graph2Y)

        graph1.SetPoint(i, graph1X, graph1Y/graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYlow(i, graph1.GetErrorYlow(i)/graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYhigh(i, graph1.GetErrorYhigh(i)/graph2Y if graph2Y != 0. else 0.)

def multiply_tgraph(graph1, graph2, error_prop=False):
    assert(graph1.GetN() == graph2.GetN())
    for i in xrange(graph1.GetN()):
        graph1X, graph1Y = ROOT.Double(0), ROOT.Double(0)
        graph1.GetPoint(i, graph1X, graph1Y)
        graph2X, graph2Y = ROOT.Double(0), ROOT.Double(0)
        graph2.GetPoint(i, graph2X, graph2Y)

        graph1.SetPoint(i, graph1X, graph1Y/graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYlow(i, graph1.GetErrorYlow(i)/graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYhigh(i, graph1.GetErrorYhigh(i)/graph2Y if graph2Y != 0. else 0.)


def normalize_to_obj(obj, ref_obj):
    obj.Scale(ref_obj.Integral() / objIntegral())

def ratio_to_obj(obj, ref_obj, error_prop=True):
    ref_obj = ref_obj.Clone('ref_obj')
    if error_prop is False:
        for i in xrange(1, ref_obj.GetNbinsX() + 1):
            ref_obj.SetBinError(i, 0.)
    obj.Divide(ref_obj)

