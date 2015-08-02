import argparse
import sys
import inspect
from settings import SettingListAction

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
        _parser = argparse.ArgumentParser(add_help=False)
        self.parser = _parser.add_argument_group(self.__class__.__name__)

    def get_parser(self):

        return parser_group

    def run(self, **args):
        pass

class RatioToObj(AnaModule):

    def __init__(self):
        super(RatioToObj, self).__init__()
        self.parser.add_argument('--ratio-to', type=int, help='')

    def run(self, root_objects, **args):
        ref_obj = root_objects[0].Clone('ref_obj')
        for obj in root_objects:
            obj.Divide(ref_obj)

class SimpleRatioToFirstObj(AnaModule):
    """Just divide by value, do not take into account errors of ref histo."""

    def __init__(self):
        super(SimpleRatioToFirstObj, self).__init__()
        self.parser.add_argument('--simpleratio-to', type=int, help='')

    def run(self, root_objects, **args):
        ref_obj = root_objects[0].Clone('ref_obj')
        for i in xrange(1, ref_obj.GetNbinsX() + 1):
            ref_obj.SetBinError(i, 0.)
        for obj in root_objects:
            obj.Divide(ref_obj)


class NormalizeObj(AnaModule):

    def __init__(self):
        super(NormalizeObj, self).__init__()
        self.parser.add_argument('--scale-objs',  nargs='+', default=[1.0],
                                       action=SettingListAction,
                                       help='Scale each obj with factor')

    def run(self, root_objects, **args):
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
                                       action=SettingListAction,
                                       help='Scale each obj with factor')

    def run(self, root_objects, **args):
        for i, obj in enumerate(root_objects):
            if args['scale_to'][i] == -1:
                continue
            else:
                obj.Scale(root_objects[args['scale_to'][i]].Integral() / root_objects[i].Integral())



