import logging

import ROOT

from modules.base_module import BaseModule

log = logging.getLogger(__name__)


class Efficiency(BaseModule):
    def __init__(self):
        super(Efficiency, self).__init__()
        print 'hallo'
        self.arg_group.add_argument('--efficiency', nargs='+', type='str2kvstr',
                                    help='Calculates the efficiency of numerator:denominator and returns a TGraph.')

    def __call__(self, config):
        print config.keys()
        for id, val in config['efficiency']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if val not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(val))

            numerator = config['objects'][id]['obj']
            denominator = config['objects'][val]['obj']
            eff_graph = ROOT.TGraphAsymmErrors(numerator, denominator)

            new_id = 'eff_{0}'.format(id.strip('_'))
            config['objects'].setdefault(new_id, {})
            config['objects'][new_id]['obj'] = eff_graph


def isfloat(value):
    """Return true if value can be converted to float."""
    try:
        float(value)
        return True
    except ValueError:
        return False
