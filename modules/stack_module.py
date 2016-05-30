import logging

import numpy as np
import ROOT

from modules.base_module import BaseModule
from modules.helpers import divide_tgraph, isfloat

log = logging.getLogger(__name__)


class Stack(BaseModule):

    def __init__(self):
        super(Stack, self).__init__()
        self.arg_group.add_argument('--stack', nargs='+', default=[], type=str,
                                    help='Stacks all the nicks.')

    def __call__(self, config):
        for i, id in reversed(list(enumerate(config['stack']))):
            for j in range(i):
                config['objects'][id]['obj'] = add(config['objects'][id]['obj'], config['objects'][config['stack'][j]]['obj'])
            config['objects'][id]['zorder'] = 1.5  - 0.01*i

class Add(BaseModule):

    def __init__(self):
        super(Add, self).__init__()
        self.arg_group.add_argument('--add', nargs='+', default=[], type='str2kvstr',
                help='Sums of all the nicks and creates new object. syntax is newnick:nick1,nick2,nick3')

    def __call__(self, config):
        for id, id_list in config['add']:
            id_list = id_list.split(',')
            newobj = config['objects'][id_list[0]]['obj'].Clone()
            for sum_id in id_list[1:]:
                newobj.Add(config['objects'][sum_id]['obj'])
            config['objects'].setdefault(id, {})['obj'] = newobj


def add(histo1, histo2):
    histo1.Add(histo2)
    return histo1


