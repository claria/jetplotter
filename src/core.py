import copy
import os
import sys
import json
import collections
import logging

from module_handler import get_all_modules
from user_parser import UserParser
# from modules.various_modules import get_module
from lookup_dict import lookup_dict


# logging.basicConfig(format='%(message)s', level='INFO')
log = logging.getLogger(__name__)


class Plotter(object):
    """ Core module preparing the config and running all modules."""

    def __init__(self):
        self.config = {}
        # All modules found in modules dir
        self._all_modules = {}
        self._input_modules = []
        self._ana_modules = []
        self._output_modules = []

    def __call__(self):

        self._init_parser()
        self._prepare_config()


        self.path = self._input_modules + self._ana_modules + self._output_modules

        # self._perform_lookup_replacement()

        if self.config['print_config']:
            print_config(self.config)

        for module in self.path:
            log.info("Processing {0}...".format(module.label()))
            module(self.config)
            update_with_default(self.config['objects'])

        # write config
        path = os.path.join(self.config['output_prefix'], self.config['output_path']).replace('.png', '.json')
        save_config(self.config, path)

    def _init_parser(self, parents=[]):
        # TODO replace mutable parents arg
        # Defines the base parser, which will be pre-parsed using known args to find additional modules 
        # with possibly additional parsers
        base_parser = UserParser(add_help=False)
        base_parser_group = base_parser.add_argument_group(title='Base Parser', description='')
        base_parser_group.add_argument("--input-modules", nargs='+', default=['RootModule'], help="Input modules .")
        base_parser_group.add_argument("--ana-modules", nargs='+', default=[], help="Analysis modules.")
        base_parser_group.add_argument("--output-modules", nargs='+', default=['PlotModule'], help="Output modules.")
        base_parser_group.add_argument("--list-modules", action='store_true', help="List all available modules.")
        base_parser_group.add_argument("--log-level", default="info", help="Set the log level.")
        args = vars(base_parser.parse_known_args()[0])

        log_level = getattr(logging, args['log_level'].upper(), None)
        if not isinstance(log_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig(format='%(message)s', level=log_level)

        # Find all available modules in modules directory.
        self._all_modules = get_all_modules()
        # Initialize additional modules specified on command line
        self._input_modules = [self._all_modules[name]() for name in args['input_modules']]
        self._ana_modules += [self._all_modules[name]() for name in args['ana_modules']]
        self._output_modules += [self._all_modules[name]() for name in args['output_modules']]
        add_parsers = [module._parser for module in self._input_modules + self._ana_modules + self._output_modules]
        add_parsers.append(base_parser)
        self.parser = UserParser(parents=add_parsers, 
                                 description='''Plotting tool to read, manipulate and plot root objects.''')
        self.parser.add_argument("-p", "--print-config", default=False, action="store_true",
                                 help="Print out the JSON config before running Artus.")
        self.parser.add_argument("-l", "--load-config", default=None,
                                 help="Load a json config from a file.")

    def _prepare_config(self, merge_parser_args=True):
        """Get config from parser and supplied json file and merges the configs.
           Then it updates missing keys in the id objects using the values of
           the _default object.
        """
        config = vars(self.parser.parse_args())
        if config['list_modules']:
            for label, module in self._all_modules.iteritems():
                print label
            sys.exit(0)

        if config['load_config']:
            file_config = read_config(config['load_config'])
            if merge_parser_args:
                update_settings(file_config, config)
            config = file_config
        self.config = config

        self._ana_modules = [self._all_modules[name]() for name in config['ana_modules']]
        update_with_default(self.config['objects'])

    def _perform_lookup_replacement(self):
        """ Searches for the occurences of keys in the lookup_dict and replaces the values
            in the config with the values from the lookup dict.
        """
        # Perform global replacements:
        for k, v in self.config.items():
            if isinstance(v, basestring) and k in lookup_dict:
                for lk, lv in lookup_dict[k].items():
                    # check if string contains any key from lookup dict
                    if lk in v:
                        self.config[k] = self.config[k].replace(lk, lv)
            elif isinstance(v, list) and k in lookup_dict:
                for i in xrange(len(v)):
                    for lk, lv in lookup_dict[k].items():
                        # check if string contains any key from lookup dict
                        if lk in v[i]:
                            self.config[k][i] = self.config[k][i].replace(lk, lv)
        # perform replacement for object dict keys
        for id in self.config['objects']:
            for k, v in self.config['objects'][id].items():
                if isinstance(v, basestring) and k in lookup_dict:
                    for lk, lv in lookup_dict[k].items():
                        # check if string contains any key from lookup dict
                        if lk in v:
                            self.config['objects'][id][k] = self.config['objects'][id][k].replace(lk, lv)


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
            config = json.load(json_file, object_pairs_hook=collections.OrderedDict)
        except ValueError as err:
            # log.critical('Failed to parse json file {0}'.format(config_name))
            print 'Failed to parse json file {0}'.format(path)
            print err
            sys.exit(1)
    return config


def update_settings(d, u, provided_args=None):
    """ Update dict d with entries of dict u, but only if key of u not in d."""
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


def walk_dic(node, func):
    """Walks a dic containing dicts, lists or str and calls func(key, val) on each str leaf."""
    seq_iter = node.keys() if isinstance(node, dict) else xrange(len(node))
    for k in seq_iter:
        print 'walk', k
        if isinstance(node[k], basestring):
            node[k] = func(k=k, v=node[k])
        elif isinstance(node[k], dict) or isinstance(node[k], list):
            walk_dic(node[k], func)


def update_with_default(data):
    for id, item in data.iteritems():
        if id == '_default':
            continue
        data[id] = dict(data['_default'].items() + item.items())
