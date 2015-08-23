import collections
import logging

import ROOT

from modules.base_module import BaseModule
from modules.root_module import get_tgraphasymm_from_histos

log = logging.getLogger(__name__)


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
