import logging

import array
import ROOT

from modules.base_module import BaseModule
from src.lookup_dict import get_lookup_val

log = logging.getLogger(__name__)


class ReBinning(BaseModule):
    def __init__(self):
        super(ReBinning, self).__init__()
        self.arg_group.add_argument('--data-lims', nargs='+', type='str2kvdict',
                                    help='Removes bins not within bin edges. Options are min and max.')

    def __call__(self, config):
        for id, kwargs in config['data_lims']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            obj = config['objects'][id]['obj']
            min_val = float(get_lookup_val('data_lims', kwargs.get('min', None)))
            max_val = float(get_lookup_val('data_lims', kwargs.get('max', None)))
            if isinstance(obj, ROOT.TH1):
                config['objects'][id]['obj'] = rebin_histo(obj, min_val, max_val)
            elif isinstance(obj, ROOT.TGraph):
                config['objects'][id]['obj'] = rebin_tgraph(obj, min_val, max_val)
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
    i=1
    while (i < obj.GetN()):
        X, Y = ROOT.Double(0), ROOT.Double(0)
        obj.GetPoint(i, X, Y)
        if (min_val <= X) and (X <= max_val):
            pass
        else:
            obj.RemovePoint(i)
            i=1
        i+=1
    return obj

