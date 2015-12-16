import collections
import logging

import ROOT

from modules.base_module import BaseModule
from util.root_tools import get_tgraphasymm_from_histos

log = logging.getLogger(__name__)


class Project3D(BaseModule):
    """Calls the Project3D function."""

    def __init__(self):
        super(Project3D, self).__init__()
        self.arg_group.add_argument('--project3d', nargs='+', type='str2kvdict', default=[], help='')

    def __call__(self, config):
        for id, kwargs in config['project3d']:
            obj = config['objects'][id]['obj']
            option = kwargs.get('option', 'x')
            xmin = kwargs.get('xmin', None)
            xmax = kwargs.get('xmax', None)
            ymin = kwargs.get('ymin', None)
            ymax = kwargs.get('ymax', None)
            zmin = kwargs.get('zmin', None)
            zmax = kwargs.get('zmax', None)
            if xmin or xmax:
                log.info('Set x range to {0} - {1}'.format(obj.GetXaxis().GetBinLowEdge(xmin),obj.GetXaxis().GetBinLowEdge(xmax)))
                obj.GetXaxis().SetRange(xmin, xmax)
            if ymin or ymax:
                log.info('Set y range to {0} - {1}'.format(obj.GetYaxis().GetBinLowEdge(ymin),obj.GetYaxis().GetBinLowEdge(ymax)))
                obj.GetYaxis().SetRange(ymin, ymax)
            if zmin or zmax:
                log.info('Set z range to {0} - {1}'.format(obj.GetZaxis().GetBinLowEdge(zmin),obj.GetZaxis().GetBinLowEdge(zmax)))
                obj.GetZaxis().SetRange(zmin, zmax)

            newobj = obj.Project3D(option)
            config['objects'][id]['obj'] = newobj

class Profile(BaseModule):
    """Calls the Project3D function."""

    def __init__(self):
        super(Profile, self).__init__()
        self.arg_group.add_argument('--profile-x', nargs='+', type='str2kvdict', default=[], help='')
        self.arg_group.add_argument('--profile-y', nargs='+', type='str2kvdict', default=[], help='')

    def __call__(self, config):
        for id, kwargs in config['profile_x']:
            obj = config['objects'][id]['obj']
            option = kwargs.get('option', '')
            ymin = int(kwargs.get('ymin', 1))
            ymax = int(kwargs.get('ymax', -1))
            if ymin or ymax:
                log.info('Set y range to {0} - {1}'.format(obj.GetYaxis().GetBinLowEdge(ymin),obj.GetYaxis().GetBinLowEdge(ymax)))

            print obj.GetEntries()
            newobj = obj.ProfileX('{0}_pfx'.format(obj.GetName), ymin, ymax, option)
            config['objects'][id]['obj'] = newobj

        for id, kwargs in config['profile_y']:
            obj = config['objects'][id]['obj']
            option = kwargs.get('option', '')
            xmin = kwargs.get('xmin', 1)
            xmax = kwargs.get('xmax', -1)
            if xmin or xmax:
                log.info('Set x range to {0} - {1}'.format(obj.GetXaxis().GetBinLowEdge(xmin),obj.GetXaxis().GetBinLowEdge(xmax)))

            print obj.GetEntries()
            newobj = obj.ProfileY('{0}_pfx'.format(obj.GetName), xmin, xmax, option)
            config['objects'][id]['obj'] = newobj
