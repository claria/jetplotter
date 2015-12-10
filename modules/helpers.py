import ROOT
import numpy as np


def divide_tgraph(graph1, graph2, error_prop=False):
    assert (graph1.GetN() == graph2.GetN())
    for i in xrange(graph1.GetN()):
        graph1X, graph1Y = ROOT.Double(0), ROOT.Double(0)
        graph1.GetPoint(i, graph1X, graph1Y)
        graph2X, graph2Y = ROOT.Double(0), ROOT.Double(0)
        graph2.GetPoint(i, graph2X, graph2Y)

        graph1.SetPoint(i, graph1X, graph1Y / graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYlow(i, np.abs(graph1.GetErrorYlow(i) / graph2Y) if graph2Y != 0. else 0.)
        graph1.SetPointEYhigh(i, np.abs(graph1.GetErrorYhigh(i) / graph2Y) if graph2Y != 0. else 0.)


def multiply_tgraph(graph1, graph2, error_prop=False):
    assert (graph1.GetN() == graph2.GetN())
    for i in xrange(graph1.GetN()):
        graph1X, graph1Y = ROOT.Double(0), ROOT.Double(0)
        graph1.GetPoint(i, graph1X, graph1Y)
        graph2X, graph2Y = ROOT.Double(0), ROOT.Double(0)
        graph2.GetPoint(i, graph2X, graph2Y)

        graph1.SetPoint(i, graph1X, graph1Y * graph2Y if graph2Y != 0. else 0.)
        graph1.SetPointEYlow(i, np.abs(graph1.GetErrorYlow(i) * graph2Y) if graph2Y != 0. else 0.)
        graph1.SetPointEYhigh(i, np.abs(graph1.GetErrorYhigh(i) * graph2Y) if graph2Y != 0. else 0.)


def get_tgrapherrors(fcn, vfitter, cl=0.683):
    """Returns a TGraph with a confidence interval representing the confidence intervals."""
    # no thinking involved. just copied from the data analysis c macro.
    npoints = 1000
    graph = ROOT.TGraphErrors(npoints)

    x_values = np.linspace(fcn.GetXmin(), fcn.GetXmax(), npoints)
    for i in xrange(0, len(x_values)):
        graph.SetPoint(i, x_values[i], 0)

    vfitter.GetConfidenceIntervals(graph, cl);
    return graph


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


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
