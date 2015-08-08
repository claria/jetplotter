import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import argparse
import core
from parser import SettingAction
from modules import Module


class RootModule(Module):

    def __init__(self):
        super(RootModule, self).__init__()
        self.parser.add_argument('-i', '--input',  nargs='+', type='str2kvstr', action='setting', help='Path to root file or objects in root files with syntax rootfile:path/to/object.')
        self.parser.add_argument('--input_graph',  nargs='+', type='str2kvstr', action='setting', help='Path to root file or objects in root files with syntax rootfile:path/to/object.')
        self.parser.add_argument('--object-paths', nargs='+', help='Path to root objects.')

    def __call__(self, config):
        for id, item in config['settings'].iteritems():
            if 'input' in item:
                item['obj'] = get_root_object(item['input'])
            elif 'input_graph' in item:
                item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input_graph']))
            elif 'input_asymmerrgraph' in item:
                item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input']))


def get_root_objects(input, object_paths=None, option=None, **kwargs):
    if input is None:
        input = []
    if not object_paths:
        object_paths = len(input) * [None]
    return [get_root_object(filename, object_path) for filename, object_path in zip(input, object_paths)]

def get_root_object(root_filename, object_path=None, option="READ"):

    if '?' in root_filename and not object_path:
        root_filename, object_path = root_filename.split('?')

    rootfile = get_root_file(root_filename, option=option)
    obj = rootfile.Get(object_path)
    ROOT.SetOwnership(obj, 0)
    if obj == None:
        raise Exception("Requested object {0} not found in rootfile {1}.".format(object_path, root_filename))
    return obj


def get_tgraphasymm_err(central_histo, err_low_histo, err_hi_histo):
    graph = ROOT.TGraphAsymmErrors(central_histo)
    for i in xrange(graph.GetN()):
        graph.SetPointEYlow(i, err_low_histo.GetBinContent(i+1))
        graph.SetPointEYhigh(i, err_hi_histo.GetBinContent(i+1))
    return graph

def get_tgraphasymm(central_histo, low_histo, hi_histo):
    graph = ROOT.TGraphAsymmErrors(central_histo)
    for i in xrange(graph.GetN()):
        graph.SetPointEYlow(i, central_histo.GetBinContent(i+1) - low_histo.GetBinContent(i+1))
        graph.SetPointEYhigh(i, hi_histo.GetBinContent(i+1) - central_histo.GetBinContent(i+1))
    return graph


def get_root_file(root_filename, option="READ"):
    rootfile = ROOT.TFile(root_filename, option)
    ROOT.SetOwnership(rootfile, 0)
    return rootfile


def normalize_to(histo, factor=1.0):
    histo.Sumw2()
    histo.Scale(1.0 / histo.Integral())


def normalize_to_histo(histo, ref_histo):
    histo.Sumw2()
    histo.Scale(ref_histo.Integral() / histo.Integral())


def normalize_to_binwidth(histo):
    histo.Sumw2()
    histo.Scale(1.0, "width")
