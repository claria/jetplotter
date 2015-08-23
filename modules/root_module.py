import ROOT

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

from modules.base_module import BaseModule


class RootModule(BaseModule):
    def __init__(self):
        super(RootModule, self).__init__()
        self.arg_group.add_argument('-i', '--input', nargs='+', type='str2kvstr', action='setting',
                                    help='Path to root file or objects in root files with syntax rootfile:path/to/object.')
        self.arg_group.add_argument('--input_tgraph', nargs='+', type='str2kvstr', action='setting',
                                    help='Path to root file or objects in root files with syntax rootfile:path/to/object.')

    def __call__(self, config):
        for id, item in config['objects'].iteritems():
            if 'input' in item:
                item['obj'] = get_root_object(item['input'])
            elif 'input_tgraph' in item:
                if '&' in item['input_tgraph']:
                    item['obj'] = get_tgraphasymm_from_histos(
                        *[get_root_object(input) for input in item['input_tgraph'].split('&')])
                else:
                    item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input_tgraph']))
            elif 'input_asymmerrgraph' in item:
                item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input']))


def get_root_objects(input, option=None, **kwargs):
    if input is None:
        input = []
    return [get_root_object(filename) for filename in input]


def get_root_object(input, option="READ"):
    if '?' in input:
        input, object_path = input.split('?')
    else:
        raise ValueError('No object path specified.')

    rootfile = get_root_file(input, option=option)
    obj = rootfile.Get(object_path)
    ROOT.SetOwnership(obj, 0)
    if obj == None:
        raise Exception("Requested object {0} not found in rootfile {1}.".format(object_path, input))
    return obj


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
