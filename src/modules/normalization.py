import logging
import numpy as np

from src.modules.base_module import BaseModule
from helpers import ratio_to_obj, isfloat

log = logging.getLogger(__name__)


class Ratio(BaseModule):
    """Calculates ratios of objects. without taking into account any error propagation. If you need an
       proper error propagation use the Divide module.
    """

    def __init__(self):
        super(Ratio, self).__init__()
        self.parser.add_argument('--ratio', nargs='+', default=[], type='str2kvstr',
                                 help='List of id:to_id objects for which the ratio is calculated.')

    def __call__(self, config):
        for id, to in config['ratio']:
            log.debug('Calculating ratio of {0} to {1}'.format(id, to))
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if to not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(to))

            ratio_to_obj(config['objects'][id]['obj'], config['objects'][to]['obj'])


class Normalize(BaseModule):
    """Normalize an obj by binwidth, to unity, to integral of another id or by a float."""

    def __init__(self):
        super(Normalize, self).__init__()
        self.parser.add_argument('--normalize', nargs='+', default=[], type='str2kvstr',
                                 help='Normalize an id to bin widths, unity, to the integral of another object or by a float using width/unity/obj_id or a float.')

    def __call__(self, config):
        for id, val in config['normalize']:
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
                config['objects'][id]['obj'].Scale(1.0 / config['objects'][val]['obj'].Integral())
            elif isfloat(val):
                # Normalize/Scale by an factor
                config['objects'][id]['obj'].Scale(float(val))
            else:
                raise ValueError('There intended normalization could not be identified for {0}'.format(val))


class NormalizeToGen(BaseModule):
    """Normalizes a given TH2 to the sum in a row (y axis), e.g. to the number of true events."""

    def __init__(self):
        super(NormalizeToGen, self).__init__()
        self.parser.add_argument('--normalize-to-gen', nargs='+', default=[], type=str,
                                 help='Id of 2d histograms which will be row-normalized.')

    def __call__(self, config):
        for id in config['normalize_to_gen']:
            if not id in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            obj = config['objects'][id]['obj']

            for y in xrange(1, obj.GetNbinsY() + 1):
                y_sow = np.sum([obj.GetBinContent(x, y) for x in xrange(1, obj.GetNbinsX() + 1)])
                for x in xrange(1, obj.GetNbinsX() + 1):
                    obj.SetBinContent(x, y, obj.GetBinContent(x, y) / y_sow)
                    obj.SetBinError(x, y, obj.GetBinError(x, y) / y_sow)


