import logging

from modules.base_module import BaseModule

log = logging.getLogger(__name__)


class Multiply(BaseModule):
    def __init__(self):
        super(Multiply, self).__init__()
        self.arg_group.add_argument('--multiply', nargs='+', type='str2kvstr', action='setting', help='')

    def __call__(self, config):
        for id, val in config['multiply']:
            if id not in config['objects']:
                raise ValueError('Requested id {} not found.'.format(id))
            if val in config['objects']:
                # Normalize to another object
                config['objects'][id]['obj'].Multiply(config['objects'][val]['obj'])
            elif isfloat(val):
                # Normalize/Scale by an factor
                config['objects'][id]['obj'].Multiply(float(val))
            else:
                raise ValueError('The intended multiplication could not be identified for {0}'.format(val))


def isfloat(value):
    """Return true if value can be converted to float."""
    try:
        float(value)
        return True
    except ValueError:
        return False
