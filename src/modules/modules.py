import copy
import sys
import inspect
import math
import numpy as np
import collections

from ..parser import UserParser
import ROOT

class Module(object):

    def __init__(self):
        self.label = self.__class__.__name__
        self._parser = UserParser(add_help=False)
        self.parser = self._parser.add_argument_group(self.label)

    def __call__(self, **args):
        raise NotImplementedError()


def get_module(name):
    """Returns instance of module of with class name 'name'."""
    thismodule = sys.modules[__name__]
    cls = getattr(thismodule, name)
    module = cls()
    return module


class RatioToObj(Module):
    def __init__(self):
        super(RatioToObj, self).__init__()
        self.parser.add_argument('--ratio', nargs='+', default=[], type='str2kvstr', help='List of id:to_id objects for which the ratio is calculated.')

    def __call__(self, config):
        for id, to in config['ratio']:
            print 'Calculating ratio', id, to
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(to))

            ratio_to_obj(config['objects'][id]['obj'], config['objects'][to]['obj'])

class ToTGraph(Module):
    def __init__(self):
        super(ToTGraph, self).__init__()
        self.parser.add_argument('--to-tgraph', nargs='+', default=[], help='')

    def __call__(self, config):
        for id in config['to_tgraph']:
            if isinstance(config['objects'][id]['obj'], collections.Iterable):
                if len(config['objects'][id]['obj']) == 1:
                    config['objects'][id]['obj'] = ROOT.TGraphAsymmErrors(config['objects'][id]['obj'])
                elif len(config['objects'][id]['obj']) == 3:
                    config['objects'][id]['obj'] = get_tgraphasymm_from_histos(*config['objects'][id]['obj'])
                else:
                    raise ValueError('unsupported conversion requested.')
            else:
                config['objects'][id]['obj'] = ROOT.TGraphAsymmErrors(config['objects'][id]['obj'])


class SimpleRatioToObj(Module):
    def __init__(self):
        super(SimpleRatioToObj, self).__init__()
        self.parser.add_argument('--simpleratio', nargs='+', default=[], type='str2kvstr', help='List of id:to_id objects for which the ratio is calculated.')

    def __call__(self, config):
        for id, to in config['simpleratio']:
            print 'calc sratio', id, to
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(to))
            to_obj = config['objects'][to]['obj'].Clone('ref')
            config['objects'][id]['obj'] = ratio_to_obj(config['objects'][id]['obj'], to_obj, error_prop=False)


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
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if val == 'width':
                config['objects'][id]['obj'].Scale(1.0, 'width')
            else:
                config['objects'][id]['obj'].Scale(1.0, float(val))


class FitObj(Module):
    """ Calls the fit function on an object.

        The function to be fitted is passed via a dict str, e.g.
        --fit-obj id:'{"fcn":"[0] + [1]/x**[2]", "fcn_0":[1.0, 1.0, 1.0]}'
    """
    def __init__(self):
        super(FitObj, self).__init__()
        self.parser.add_argument('--fit-obj', nargs='+', default=[], type='str2kvdict', help='')

    def __call__(self, config):
        for id, settings in config['fit_obj']:
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            fcn_name = 'fit_{0}'.format(id)
            fcn = ROOT.TF1(fcn_name, settings['fcn'])

            if 'fcn_0' in settings:
                fcn.SetParameters(*settings['fcn_0'])
            options = settings.get('options', '')

            xmin, xmax = config['objects'][id]['obj'].GetXaxis().GetXmin(), config['objects'][id]['obj'].GetXaxis().GetXmax()
            # Do the fit
            config['objects'][id]['obj'].Fit(fcn_name, options)
            vfitter = ROOT.TVirtualFitter.GetFitter()
            fcn.SetNpx(1000)
            fcn.SetRange(xmin, xmax)
            errorgraph = get_tgrapherrors(fcn, vfitter)
            #TODO fix this shit
            # config['objects']['fit_{0}'.format(id)] = copy.deepcopy(config['objects'][id])
            new_obj_name = 'fit_{0}'.format(id)
            config['objects'].setdefault(new_obj_name, {})['obj'] = errorgraph


class ResolutionAna(Module):
    """ Calls the fit function on an object.

    """
    def __init__(self):
        super(ResolutionAna, self).__init__()
        self.parser.add_argument('--resolution', nargs='+', default=[],  help='')

    def __call__(self, config):
        for id in config['resolution']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            gen_bins = config['objects'][id]['obj'].GetNbinsY()
            resolution_graph = ROOT.TGraphErrors(gen_bins)
            for i in xrange(1, gen_bins + 1):
                # Get slice of 2d histogram
                pt_bin_obj = config['objects'][id]['obj'].ProjectionX("{0}_slice_{1}".format(id, i), i, i)
                # Continue if histogram if empty
                if pt_bin_obj.GetEntries() < 1:
                    continue
                # If fit fails continue instead of failing
                id_slice = '_{0}_slice_{1}'.format(id.strip('_'), i)
                res = pt_bin_obj.Fit("gaus", "SQ")
                fcn = pt_bin_obj.GetFunction("gaus")
                if res.Get() == None or res.Status() != 0:
                    continue
                xmin, xmax = pt_bin_obj.GetXaxis().GetXmin(), pt_bin_obj.GetXaxis().GetXmax()
                vfitter = ROOT.TVirtualFitter.GetFitter()
                fcn.SetNpx(1000)
                fcn.SetRange(xmin, xmax)
                error_graph = get_tgrapherrors(fcn, vfitter)

                # Omit bin with too large errors > 5%
                if (fcn.GetParError(2)/fcn.GetParameter(2)) > 0.05:
                    continue
                # Uncomment to save also individual gauss fits to dict
                # config['objects'].setdefault(id_slice, {})
                # config['objects'][id_slice]['obj'] = pt_bin_obj
                # config['objects'].setdefault('{0}_fit'.format(id_slice), {})
                # config['objects']['{0}_fit'.format(id_slice)]['obj'] = error_graph
                resolution_graph.SetPoint(i, config['objects'][id]['obj'].GetYaxis().GetBinCenter(i), fcn.GetParameter(2))
                resolution_graph.SetPointError(i, config['objects'][id]['obj'].GetYaxis().GetBinWidth(i)/2., fcn.GetParError(2))
            # Store TGraph and fit TGraph
            id_res = 'resolution_{0}'.format(id.strip('_'))
            config['objects'].setdefault(id_res, {})
            config['objects'][id_res]['obj'] = resolution_graph

            res_fcn = ROOT.TF1("res_fcn", "sqrt(([0]/x)**2 + (([1]**2)/x) + [2]**2)")
            res_fcn.SetParameters(6., 0.5, 0.01)
            res_fcn.SetRange(0., 999999.)
            print 'Fitting id {0}'.format(id_res)
            res = resolution_graph.Fit("res_fcn", "RS", "")
            # graph.Write()
            if res.Get() == None or res.Status() != 0:
                continue
            xmin, xmax = resolution_graph.GetXaxis().GetXmin(), resolution_graph.GetXaxis().GetXmax()
            vfitter = ROOT.TVirtualFitter.GetFitter()
            res_fcn.SetNpx(1000)
            res_fcn.SetRange(xmin, xmax)
            res_error_graph = get_tgrapherrors(res_fcn, vfitter)

            config['objects'].setdefault('{0}_fit'.format(id_res), {})['obj'] = res_error_graph




def get_tgrapherrors(fcn, vfitter):
    # no thinking involved. just copied from the data analysis c macro.
    npoints = 1000
    graph = ROOT.TGraphErrors(npoints)

    x_values = np.linspace(fcn.GetXmin(), fcn.GetXmax(), npoints)
    for i in xrange(0, len(x_values)):
        graph.SetPoint(i, x_values[i], 0)

    vfitter.GetConfidenceIntervals(graph, 0.683);

    return graph
    #npoints = 1000
    #x_values = np.linspace(fcn.GetXmin(), fcn.GetXmax(), npoints)

    #vfitter = ROOT.TVirtualFitter.GetFitter()
    #graph = ROOT.TGraphErrors(npoints)
    ## npar = vfitter.GetNumberTotalParameters()

    #x = array.array('d', x_values)
    #y = array.array('d', [0.]*len(x_values))
    #vfitter.GetConfidenceIntervals(len(x_values), 1, 1, x, y, 0.683)

    #for i in xrange(0, len(x)):
    #    g.SetPoint(i, x[i], fcn.Eval(point))
    #    g.SetPointError(i, 0, math.sqrt(pointerror))

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


def normalize_to_obj(obj, to_obj):
    obj.Scale(to_obj.Integral() / objIntegral())


def ratio_to_obj(obj, to_obj, error_prop=True):
    if isinstance(obj, ROOT.TH1) and isinstance(to_obj, ROOT.TH1):
        to_obj = to_obj.Clone('to_obj')
        if error_prop is False:
            for i in xrange(1, to_obj.GetNbinsX() + 1):
                to_obj.SetBinError(i, 0.)
        obj.Divide(to_obj)
    elif isinstance(obj, ROOT.TGraph) and isinstance(to_obj, ROOT.TGraph):
        divide_tgraph(obj, to_obj, error_prop=False)
    elif isinstance(obj, ROOT.TH1) and isinstance(to_obj, ROOT.TGraph):
        obj = ROOT.TGraphAsymmErrors(obj)
        divide_tgraph(obj, to_obj, error_prop=False)
    else:
        raise TypeError('Invalid types passed: {0} and {1}'.format(type(obj), type(to_obj)))
    return obj
