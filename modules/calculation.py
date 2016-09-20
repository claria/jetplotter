import logging
import ROOT

from modules.base_module import BaseModule
import numpy as np

log = logging.getLogger(__name__)

class Divide(BaseModule):
    def __init__(self):
        super(Divide, self).__init__()
        self.arg_group.add_argument('--divide', nargs='+', type='str2kvstr', help='')

    def __call__(self, config):
        for id, val in config['divide']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            config['objects'][id]['obj'].Divide(config['objects'][val]['obj'])


class Multiply(BaseModule):
    def __init__(self):
        super(Multiply, self).__init__()
        self.arg_group.add_argument('--multiply', nargs='+', type='str2kvstr', help='')

    def __call__(self, config):
        for id, val in config['multiply']:
            obj = config['objects'][id]['obj']
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if val in config['objects']:
                print 'Multiplying {0} with {1}'.format(id, val)
                config['objects'][id]['obj'] = multiply(config['objects'][id]['obj'], config['objects'][val]['obj'])
            elif isfloat(val):
                # Normalize/Scale by an factor
                if isinstance(obj, ROOT.TH1):
                    # config['objects'][id]['obj'].Multiply(float(val))
                    val = float(val)
                    for i in xrange(1, obj.GetNbinsX() + 1):
                        obj.SetBinContent(i, obj.GetBinContent(i) * val)
                        obj.SetBinError(i, obj.GetBinError(i) * val)
                elif isinstance(obj, ROOT.TGraph):
                    for i in range(obj.GetN()):
                        obj.GetY()[i] *= float(val)
                        obj.GetEYhigh()[i] *= float(val)
                        obj.GetEYlow()[i] *= float(val)
            else:
                raise ValueError('The intended multiplication could not be identified for {0}'.format(val))


class ScaleUnc(BaseModule):
    def __init__(self):
        super(ScaleUnc, self).__init__()
        self.arg_group.add_argument('--scale_unc', nargs='+', type='str2kvstr', help='')

    def __call__(self, config):
        for id, val in config['scale_unc']:
            log.info('Scaling id {0} with value {1}'.format(id, val))
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            obj = config['objects'][id]['obj']
            if isfloat(val):
                # Normalize/Scale by an factor
                if isinstance(obj, ROOT.TH1):
                    raise NotImplementedError('Unc scaling not implemented for TH1')
                elif isinstance(obj, ROOT.TGraph):
                    for i in range(obj.GetN()):
                        obj.GetEYhigh()[i] *= float(val)
                        obj.GetEYlow()[i] *= float(val)
            else:
                raise ValueError('The intended multiplication could not be identified for {0}'.format(val))


def isfloat(value):
    """Return true if value can be converted to float."""
    try:
        float(value)
        return True
    except ValueError:
        return False


def multiply(obj, with_obj):
    obj = obj.Clone('ratio_{0}'.format(obj.GetName()))

    if isinstance(with_obj, ROOT.TH1):
        if isinstance(obj, ROOT.TH1):
            mult_vals = np.zeros(obj.GetNbinsX())
        elif isinstance(obj, ROOT.TGraph):
            mult_vals = np.zeros(obj.GetN())

        for i in xrange(1, with_obj.GetNbinsX() + 1):
            mult_vals[i-1] = with_obj.GetBinContent(i)

    elif isinstance(with_obj, ROOT.TGraph):
        mult_vals = np.zeros(with_obj.GetN())
        for i in xrange(with_obj.GetN()):
            tmp_x, tmp_y = ROOT.Double(0), ROOT.Double(0)
            with_obj.GetPoint(i, tmp_x, tmp_y)
            mult_vals[i] = tmp_y
            # print tmp_x, tmp_y

    if isinstance(obj, ROOT.TH1):
        for i in xrange(1, obj.GetNbinsX() + 1):
            obj.SetBinContent(i, obj.GetBinContent(i) * mult_vals[i-1])
            obj.SetBinError(i, obj.GetBinError(i) * mult_vals[i-1])
    elif isinstance(obj, ROOT.TGraph):
        for i in xrange(obj.GetN()):
            tmp_x, tmp_y = ROOT.Double(0), ROOT.Double(0)
            obj.GetPoint(i, tmp_x, tmp_y)
            obj.SetPoint(i, tmp_x, tmp_y * mult_vals[i])
    else:
        raise TypeError('Invalid types passed: {0} and {1}'.format(type(obj), type(to_obj)))
    return obj

