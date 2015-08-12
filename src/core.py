import copy
import os
import sys
import json
import collections

from modules.root_module import RootModule
from modules.plot_module import PlotModule
from parser import UserParser
from modules.modules import get_module
from lookup_dict import lookup_dict


class Plotter(object):
    """ Core module preparing the config and running all modules."""
    def __init__(self):
        self.config = {}
        self._input_modules = [RootModule()]
        self._ana_modules = []
        self._output_modules = [PlotModule()]

    def __call__(self):
        self._init_parser()
        self._prepare_config()
        self.path = self._input_modules + self._ana_modules + self._output_modules

        self._perform_lookup_replacement()

        if self.config['print_config']:
            print_config(self.config)

        for module in self.path:
            print "Processing {0}...".format(module.label)
            module(self.config)

        # write config
        path = os.path.join(self.config['output_prefix'], self.config['output_path']).replace('.png', '.json')
        save_config(self.config, path)

    def _init_parser(self, parents=[]):
        self.parser = UserParser(add_help=False)
        self.parser.add_argument("--ana-modules", nargs='+', default=[], help="Analysis modules.")
        args = vars(self.parser.parse_known_args()[0])
        self._ana_modules += [get_module(name) for name in args['ana_modules']]
        add_parsers = [module._parser for module in self._input_modules + self._ana_modules + self._output_modules]
        self.parser = UserParser(parents=add_parsers)
        # self.parser.add_argument("--input-modules", nargs='+', default=[], help="Analysis modules.")
        self.parser.add_argument("--ana-modules", nargs='+', default=[], help="Analysis modules.")
        # self.parser.add_argument("--output-modules", nargs='+', default=[], help="Analysis modules.")
        self.parser.add_argument("-p", "--print-config", default=False, action="store_true",
                                 help="Print out the JSON config before running Artus.")
        self.parser.add_argument("-l", "--load-config", default=None,
                                 help="Print out the JSON config before running Artus.")

    def _prepare_config(self):
        """Get config from parser and supplied json file and merges the configs.
           Then it updates missing keys in the id objects using the values of
           the _default object.
        """
        config = vars(self.parser.parse_args())
        if config['load_config']:
            file_config = read_config(config['load_config'])
            update_settings(file_config, config)
            config = file_config
        self.config = config

        self._ana_modules = [get_module(name) for name in config['ana_modules']]
        update_with_default(self.config['objects'])

    def _perform_lookup_replacement(self):
        """ Searches for the occurences of keys in the lookup_dict and replaces the values
            in the config with the values from the lookup dict.
        """
        # Perform global replacements:
        for k in self.config.keys():
            if k in lookup_dict and self.config[k] in lookup_dict[k]:
                self.config[k] = lookup_dict[k][v]
        # perform replacement for object dict keys
        for id in self.config['objects']:
            for k in self.config['objects'].keys():
                if k in lookup_dict and self.config['objects']['id'][k] in lookup_dict[k]:
                    self.config['objects'][id][k] = lookup_dict[k][v]


class SimpleJsonEncoder(json.JSONEncoder):
    """JSON Encoder which replaces not serializiable objects like root objects with null."""
    def default(self, obj):
        if not isinstance(obj, (dict, list, tuple, str, unicode, int, long, float, bool)):
            return 'null'
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


def save_config(config, path, indent=4):
    """Save json config to file."""
    # Remove non serializiable objects from dict.
    out_config = copy.deepcopy(config)

    for id in out_config['objects'].keys():
        if 'obj' in out_config['objects'][id]:
            out_config['objects'][id].pop('obj')

    # Check that output directory exists
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    # Write config.
    with open(path, "w") as f:
        json.dump(out_config, f, skipkeys=True, indent=indent, sort_keys=True)

    # log.debug("Config written to \"{0}\"".format(path))
    print "Config written to \"{0}\"".format(path)
    return path


def read_config(path):
    """Read json config from file."""
    with open(path) as json_file:
        try:
            config = json.load(json_file)
        except ValueError:
            # log.critical('Failed to parse json file {0}'.format(config_name))
            print 'Failed to parse json file {0}'.format(path)
            sys.exit(1)
    return config


def update_settings(d, u, provided_args=None):
    """ Update dict d with entries of dict u, but only if key of u not in d."""
    print provided_args
    if provided_args is None:
        provided_args = []
    provided_args += u.get('provided_args', [])
    for k, v in u.iteritems():
        if isinstance(v, collections.Mapping):
            r = update_settings(d.get(k, {}), v, provided_args)
            d[k] = r
        else:
            if k in provided_args or k not in d:
                d[k] = u[k]
            else:
                pass
    return d


def print_config(config):
    print json.dumps(config, sort_keys=True, cls=SimpleJsonEncoder, indent=4)


def walk_json():
    pass


def update_with_default(data):
    for id, item in data.iteritems():
        if id == '_default':
            continue
        data[id] = dict(data['_default'].items() + item.items())
