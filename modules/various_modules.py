import collections
import logging
import copy

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

class Copy(BaseModule):
    def __init__(self):
        super(Copy, self).__init__()
        self.arg_group.add_argument('--copy-id', nargs='+', type='str2kvstr', help='')

    def __call__(self, config):
        for id, new_id in config['copy_id']:
            config['objects'].setdefault(new_id, {})['obj'] = copy.deepcopy(config['objects'][id]['obj'])


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

class MinusOne(BaseModule):
    """Just subtracts 1 from histo or graph."""

    def __init__(self):
        super(MinusOne, self).__init__()
        self.arg_group.add_argument('--minusone', nargs='+', default=[], help='')

    def __call__(self, config):
        for id in config['minusone']:
            obj = config['objects'][id]['obj']
            if isinstance(obj, ROOT.TH1):
                for i in xrange(1, obj.GetNbinsX() + 1):
                    if obj.GetBinContent(i) != 0.:
                        bc = obj.GetBinContent(i) -1.
                    else:
                        bc = 0.0
                    obj.SetBinContent(i, bc)
            elif isinstance(obj, ROOT.TGraph):
                for i in xrange(obj.GetN()):
                    tmp_x, tmp_y = ROOT.Double(0), ROOT.Double(0)
                    obj.GetPoint(i, tmp_x, tmp_y)
                    obj.SetPoint(i, tmp_x, tmp_y-1)

class QuadraticSum(BaseModule):
    """Just subtracts 1 from histo or graph."""

    def __init__(self):
        super(QuadraticSum, self).__init__()
        self.arg_group.add_argument('--quadratic_sum', nargs='+', default=[], help='')

    def __call__(self, config):
        for item in config['quadratic_sum']:
            new_id = item[0]
            new_obj = ROOT.TGraphAsymmErrors(config['objects'][item[1][0]]['obj'])

            yerr_l = np.zeros((new_obj.GetN(),))
            yerr_u = np.zeros((new_obj.GetN(),))

            for sum_id in item[1]:
                if isinstance(obj, ROOT.TGraph):
                    for i in xrange(obj.GetN()):
                        yerr_l += obj.GetErrorYlow(i)**2
                        yerr_u += obj.GetErrorYhigh(i)**2
                else:
                    raise NotImplementedError

            yerr_l = np.sqrt(yerr_l)
            yerr_u = np.sqrt(yerr_u)

            for i in xrange(obj.GetN()):
                new_obj.SetPointEYhigh(yerr_u[i])
                new_obj.SetPointEYlow(yerr_l[i])

            config['objects'].setdefault('new_id', {})['obj'] = new_obj
