import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

import argparse
import core
from core import SettingAction


def get_parser():

    parser = core.UserParser(add_help=False)
    root_input = parser.add_argument_group('Root Input')
    root_input.add_argument('-i', '--input',  nargs='+', type='str2kvstr', action='setting', help='Path to root file or objects in root files with syntax rootfile:path/to/object.')
    root_input.add_argument('--object-paths', nargs='+', help='Path to root objects.')

    return parser

def read_input(**kwargs):
    root_objects = get_root_objects(**kwargs)
    data = []

    for i, object in enumerate(root_objects):
        obj = {}
        obj['id'] = 'id_{0}'.format(i)
        obj['obj'] = object
        data.append(obj)
    return data

def get_root_objects(input, object_paths=None, option=None, **kwargs):
    if input is None:
        input = []
    if not object_paths:
        object_paths = len(input) * [None]
    return [get_root_object(filename, object_path) for filename, object_path in zip(input, object_paths)]

def get_root_object(root_filename, object_path=None, option="READ"):

    if ':' in root_filename and not object_path:
        root_filename, object_path = root_filename.split('?')

    rootfile = get_root_file(root_filename, option=option)
    obj = rootfile.Get(object_path)
    ROOT.SetOwnership(obj, 0)
    if obj == None:
        raise Exception("Requested object {0} not found in rootfile {1}.".format(object_path, root_filename))
    return obj


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
