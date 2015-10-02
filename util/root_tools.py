import ROOT

import root2np


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
        graph.SetPointEYlow(i, central_histo.GetBinContent(i + 1) - low_histo.GetBinContent(i + 1))
        graph.SetPointEYhigh(i, hi_histo.GetBinContent(i + 1) - central_histo.GetBinContent(i + 1))
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
