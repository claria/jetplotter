import logging

import numpy as np
import ROOT

from modules.base_module import BaseModule
from modules.helpers import divide_tgraph, isfloat

log = logging.getLogger(__name__)


class Ratio(BaseModule):
    """Calculates ratios of objects. without taking into account any error propagation. If you need an
       proper error propagation use the Divide module.
    """

    def __init__(self):
        super(Ratio, self).__init__()
        self.arg_group.add_argument('--ratio', nargs='+', default=[], type='str2kvstr',
                                    help='Calculates the ratio of id:val for each entry '
                                         'and puts the result in the id setting.')
        self.arg_group.add_argument('--ratio-copy', nargs='+', default=[], type='str2kvstr',
                                    help='Calculates the ratio of id:val for each entry '
                                         'and creates a new item ratio_id for the ratio.')

    def __call__(self, config):
        for id, to in config['ratio']:
            log.debug('Calculating ratio of {0} to {1}'.format(id, to))
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(to))
            obj = config['objects'][id]['obj']
            to_obj = config['objects'][to]['obj']
            config['objects'][id]['obj'] = calc_ratio(obj, to_obj)
        for id, to in config.get('ratio_copy', []):
            log.debug('Calculating ratio of {0} to {1}'.format(id, to))
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(to))
            obj = config['objects'][id]['obj']
            to_obj = config['objects'][to]['obj']
            new_id = 'ratio_{0}'.format(id)
            config['objects'].setdefault(new_id, {})
            config['objects'][new_id]['obj'] = calc_ratio(obj, to_obj)


def calc_ratio(obj, to_obj):
    obj = obj.Clone('ratio_{0}'.format(obj.GetName()))
    if isinstance(obj, ROOT.TH1) and isinstance(to_obj, ROOT.TH1):
        if not (obj.GetNbinsX() == to_obj.GetNbinsX()):
            raise ValueError('The two histograms have different numbers of bins.')
        for i in xrange(1, obj.GetNbinsX() + 1):
            try:
                obj.SetBinContent(i, obj.GetBinContent(i) / to_obj.GetBinContent(i))
                obj.SetBinError(i, obj.GetBinError(i) / to_obj.GetBinContent(i))
            except ZeroDivisionError:
                obj.SetBinContent(i, 0.)
                obj.SetBinError(i, 0.)
    elif isinstance(obj, ROOT.TGraph) and isinstance(to_obj, ROOT.TGraph):
        divide_tgraph(obj, to_obj, error_prop=False)
    elif isinstance(obj, ROOT.TH1) and isinstance(to_obj, ROOT.TGraph):
        obj = ROOT.TGraphAsymmErrors(obj)
        divide_tgraph(obj, to_obj, error_prop=False)
    else:
        raise TypeError('Invalid types passed: {0} and {1}'.format(type(obj), type(to_obj)))
    return obj


class Normalize(BaseModule):
    """Normalize an obj by binwidth, to unity, to integral of another id or by a float."""

    def __init__(self):
        super(Normalize, self).__init__()
        self.arg_group.add_argument('--normalize', nargs='+', default=[], type='str2kvstr',
                                    help='Normalize an id to bin widths, unity, to the integral of another '
                                         'object or by a float using width/unity/obj_id or a float.')

    def __call__(self, config):
        for id, val in config['normalize']:
            log.debug('Normalizing id {0} using {1}.'.format(id, val))
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if val == 'width':
                # Normalize to bin width
                config['objects'][id]['obj'].Scale(1.0, 'width')
            elif val == 'unity':
                # Normalize to Unity
                config['objects'][id]['obj'].Scale(1.0 / config['objects'][id]['obj'].Integral())
            elif val in config['objects']:
                # Normalize to another object
                config['objects'][id]['obj'].Scale(
                    config['objects'][val]['obj'].Integral() / config['objects'][id]['obj'].Integral())
            elif isfloat(val):
                # Normalize/Scale by an factor
                config['objects'][id]['obj'].Scale(float(val))
            else:
                raise ValueError('There intended normalization could not be identified for {0}'.format(val))


class NormalizeToRow(BaseModule):
    """Normalizes a given TH2 to the sum in a row (y axis), e.g. to the number of true events for a response matrix."""

    def __init__(self):
        super(NormalizeToRow, self).__init__()
        self.arg_group.add_argument('--normalize-to-row', nargs='+', default=[], type=str,
                                    help='Id of 2d histograms which will be row-normalized.')

    def __call__(self, config):
        for id in config['normalize_to_row']:
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            obj = config['objects'][id]['obj']

            for y in xrange(1, obj.GetNbinsY() + 1):
                y_sow = np.sum([obj.GetBinContent(x, y) for x in xrange(1, obj.GetNbinsX() + 1)])
                for x in xrange(1, obj.GetNbinsX() + 1):
                    obj.SetBinContent(x, y, obj.GetBinContent(x, y) / y_sow)
                    obj.SetBinError(x, y, obj.GetBinError(x, y) / y_sow)
