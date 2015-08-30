import logging

from modules.base_module import BaseModule

log = logging.getLogger(__name__)


class CopyToWeb(BaseModule):
    def __init__(self):
        super(CopyToWeb, self).__init__()
        self.arg_group.add_argument('--www', nargs='+', type='str2kvstr', action='setting', help='')

    def __call__(self, config):
        # what should it do.
        # create folder on target machine for current day.
        # copy plot & json to folder
        # run update_gallery script
        pass
