import collections
import logging

import ROOT

from modules.base_module import BaseModule
from util.root_tools import get_tgraphasymm_from_histos

log = logging.getLogger(__name__)


class Remove(BaseModule):
    """Just removes the object."""

    def __init__(self):
        super(Remove, self).__init__()
        self.arg_group.add_argument('--remove', nargs='+', default=[], help='')

    def __call__(self, config):
        for id in config['remove']:
            del config['objects'][id]


class ToTGraph(BaseModule):
    """Converts the object to a TGraphAsymmErrors object."""

    def __init__(self):
        super(ToTGraph, self).__init__()
        self.arg_group.add_argument('--to-tgraph', nargs='+', default=[], help='')

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

class FractionalUncertainty(BaseModule):
    """Converts the object to a TGraphAsymmErrors object."""

    def __init__(self):
        super(FractionalUncertainty, self).__init__()
        self.arg_group.add_argument('--fractional-uncertainty', nargs='+', default=[], help='')

    def __call__(self, config):
        for id in config['fractional_uncertainty']:
            obj = config['objects'][id]['obj']
            if isinstance(obj, ROOT.TH1):
                for i in xrange(1, obj.GetNbinsX() + 1):
                    if obj.GetBinContent(i) != 0.:
                        bc = obj.GetBinError(i) / obj.GetBinContent(i)
                    else:
                        bc = 0.0
                    obj.SetBinContent(i, bc)
                    obj.SetBinError(i, 0.0)
            elif isinstance(obj, ROOT.TGraph):
                for i in xrange(obj.GetN()):
                    tmp_x, tmp_y = ROOT.Double(0), ROOT.Double(0)
                    obj.GetPoint(i, tmp_x, tmp_y)
                    obj.SetPoint(i, tmp_x, tmp_y)
