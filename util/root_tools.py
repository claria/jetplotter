import ROOT
import numpy as np
import root2np


def build_root_object(center, low=None, up=None, err_low=None, err_up=None):
    
    obj_central = get_root_object(center)
    if low:
        obj_low = get_root_object(low)
    if up:
        obj_up = get_root_object(up)
    if err_low:
        obj_err_low = get_root_object(err_low)
    if err_up:
        obj_err_up = get_root_object(err_up)

    # convert everything into tgraph
    out_obj = ROOT.TGraphAsymmErrors(obj_central)

    if low and high:
        low_graph = ROOT.TGraphAsymmErrors(obj_low)
        up_graph = ROOT.TGraphAsymmErrors(obj_up)
        assert(low_graph.GetN() == up_graph.GetN() == out_obj.GetN())
        for i in xrange(out_obj.GetN()):
            central_x, central_y = ROOT.Double(0), ROOT.Double(0)
            out_obj.GetPoint(i, central_x, central_y)
            up_x, up_y = ROOT.Double(0), ROOT.Double(0)
            up_graph.GetPoint(i, central_x, central_y)
            low_x, low_y = ROOT.Double(0), ROOT.Double(0)
            low_graph.GetPoint(i, central_x, central_y)

            xerrl_i = out_obj.GetErrorXlow(i)
            xerru_i = out_obj.GetErrorXhigh(i)
            yerrl_i = up_y - central_y if (up_y - central_y > 0.) else 0.0
            yerru_i = central_y -low_y if (central_y - low_y > 0.) else 0.0
            graph.SetPointError(i, xerrl_i, xerru_i, yerrl_i, yerru_i)
    elif err_low and err_up:
        pass
    else:
        print 'error'
    return out_obj



def get_root_objects(input, option=None, **kwargs):
    if input is None:
        input = []
    return [get_root_object(filename) for filename in input]


def get_root_object(input, option="READ"):
    if '?' in input:
        input, object_path = input.split('?')
    else:
        raise ValueError('No object path specified. Syntax: File.root?path/to/histo')

    rootfile = get_root_file(input, option=option)
    obj = rootfile.Get(object_path)
    ROOT.SetOwnership(obj, 0)
    if obj == None:
        raise Exception("Requested object {0} not found in rootfile {1}.".format(object_path, input))
    return obj


def get_np_object(root_object_path):
    root_object = get_root_object(root_object_path)
    np_object = root2np.R2npObject1D(root_object)

    return np_object



def get_tgraphasymm_err(central_histo, err_low_histo, err_hi_histo):
    graph = ROOT.TGraphAsymmErrors(central_histo)
    for i in xrange(graph.GetN()):
        graph.SetPointEYlow(i, err_low_histo.GetBinContent(i + 1))
        graph.SetPointEYhigh(i, err_hi_histo.GetBinContent(i + 1))
    return graph


def get_tgraphasymm_from_histos(central_histo, low_histo, hi_histo):
    graph = ROOT.TGraphAsymmErrors(central_histo)
    for i in xrange(graph.GetN()):
        graph.SetPointEYlow(i, np.abs(central_histo.GetBinContent(i + 1) - low_histo.GetBinContent(i + 1)))
        graph.SetPointEYhigh(i, np.abs(hi_histo.GetBinContent(i + 1) - central_histo.GetBinContent(i + 1)))
    return graph

def build_tgraph_from_lists(x, y, xerrl=None, xerru=None, yerrl=None, yerru=None):
    """ Builds a TGraphErrors from python lists containing the data."""
    graph = ROOT.TGraphAsymmErrors(len(x))
    for i in xrange(graph.GetN()):
        graph.SetPoint(i, x[i], y[i])
        xerrl_i = xerrl[i] if xerrl is not None else 0.
        xerru_i = xerru[i] if xerru is not None else 0.
        yerrl_i = yerrl[i] if yerrl is not None else 0.
        yerru_i = yerru[i] if yerru is not None else 0.
        graph.SetPointError(i, xerrl_i, xerru_i, yerrl_i, yerru_i)
    return graph


def get_root_file(root_filename, option="READ"):
    rootfile = ROOT.TFile(root_filename, option)
    ROOT.SetOwnership(rootfile, 0)
    return rootfile


def normalize_to(histo, factor=1.0):
    histo.Sumw2()
    histo.Scale(factor / histo.Integral())


def normalize_to_histo(histo, ref_histo):
    histo.Sumw2()
    histo.Scale(ref_histo.Integral() / histo.Integral())


def normalize_to_binwidth(histo):
    histo.Sumw2()
    histo.Scale(1.0, "width")
