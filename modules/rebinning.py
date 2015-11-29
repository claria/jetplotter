import logging

import array
import ROOT

from modules.base_module import BaseModule

log = logging.getLogger(__name__)


class ReBinning(BaseModule):
    def __init__(self):
        super(ReBinning, self).__init__()
        self.arg_group.add_argument('--data-lims', nargs='+', type='str2kvdict',
                                    help='Removes bins not within bin edges. Options are min and max.')

    def __call__(self, config):
        print config['data_lims']
        for id, kwargs in config['data_lims']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))

            obj = config['objects'][id]['obj']

            min_val = kwargs.get('min', None)
            max_val = kwargs.get('max', None)

            config['objects'][id]['obj'] = rebin_histo(obj, min_val, max_val)

def rebin_histo(obj, min_val, max_val):
    new_binedges = []
    print min_val, max_val
    for i in xrange(obj.GetNbinsX() +1):
        if (min_val <= obj.GetBinLowEdge(i+1)) and (obj.GetBinLowEdge(i+2) <= max_val):
            new_binedges.append(obj.GetBinLowEdge(i+1))

    new_binedges = array.array("d", new_binedges)
    new_obj = obj.Rebin(len(new_binedges) -1, '{0}_reb'.format(obj.GetName()), new_binedges)
    return new_obj
