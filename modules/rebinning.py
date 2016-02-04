import logging

import array
import ROOT

from modules.base_module import BaseModule
from src.lookup_dict import get_lookup_val

log = logging.getLogger(__name__)


class DataLims(BaseModule):
    def __init__(self):
        super(DataLims, self).__init__()
        self.arg_group.add_argument('--data-lims', nargs='+', type='str2kvdict',
                                    help='Removes bins not within bin edges. Options are min and max.')

    def __call__(self, config):
        print config.get('data_lims', [])
        if any(id == 'all' for id, kwargs in config.get('data_lims', [])):
            all_kwargs = [kwargs for id, kwargs in config['data_lims'] if id == 'all'][0] 
            config['data_lims'] = [(id, all_kwargs) for id in config['objects'].keys() if (id != '_default')]
        for id, kwargs in config['data_lims']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if not 'obj' in config['objects'][id]:
                continue
            log.info('Rebinning id {0}'.format(id))
            obj = config['objects'][id]['obj']
            min_val = float(get_lookup_val('data_lims', kwargs.get('min', None)))
            max_val = float(get_lookup_val('data_lims', kwargs.get('max', None)))
            if isinstance(obj, ROOT.TH1):
                config['objects'][id]['obj'] = rebin_histo(obj, min_val, max_val)
            elif isinstance(obj, ROOT.TGraph):
                config['objects'][id]['obj'] = rebin_tgraph(obj, min_val, max_val)

# just for compatibility
class ReBinning(DataLims):
    pass

def rebin_histo(obj, min_val, max_val):
    new_binedges = []
    for i in xrange(obj.GetNbinsX() +1):
        if (min_val <= obj.GetBinLowEdge(i+1)) and (obj.GetBinLowEdge(i+1) <= max_val):
            new_binedges.append(obj.GetBinLowEdge(i+1))

    new_binedges = array.array("d", new_binedges)
    new_obj = obj.Rebin(len(new_binedges) -1, '{0}_reb'.format(obj.GetName()), new_binedges)
    return new_obj

def rebin_tgraph(obj, min_val, max_val):
    print 'rebinning tgraph'
    x_vals = []
    y_vals = []
    x_errs_l = []
    x_errs_h = []
    y_errs_l = []
    y_errs_h = []
    for i in range(0, obj.GetN()):
        X, Y = ROOT.Double(0), ROOT.Double(0)
        obj.GetPoint(i, X, Y)
        if (min_val <= X) and (X <= max_val):
            x_vals.append(X)
            y_vals.append(Y)
            x_errs_l.append(obj.GetErrorXlow(i))
            x_errs_h.append(obj.GetErrorXhigh(i))
            y_errs_l.append(obj.GetErrorYlow(i))
            y_errs_h.append(obj.GetErrorYhigh(i))
    new_obj = ROOT.TGraphAsymmErrors(len(x_vals))
    for i in range(0, new_obj.GetN()):
        new_obj.SetPoint(i, x_vals[i], y_vals[i])
        new_obj.SetPointError(i, x_errs_l[i], x_errs_h[i], y_errs_l[i], y_errs_h[i])
    print x_vals, y_vals
    return new_obj

