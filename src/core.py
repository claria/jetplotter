import os
import sys
import logging
import runpy

from module_handler import discover_modules
from util.config_tools import merge, read_config, write_config
from util.setting_parser import SettingParser
import util.callbacks as callbacks

log = logging.getLogger(__name__)


class Plotter(object):
    """ Core module preparing the config and running all modules."""

    def __init__(self):
        # All modules found in modules dir
        self._all_modules = {}
        self._input_modules = []
        self._ana_modules = []
        self._output_modules = []

    def __call__(self):

        # Discover all available modules
        callbacks.trigger('before_module_discovery')
        self._all_modules = discover_modules()

        # Command line args
        cmd_config = self.parse_args()

        # load config from files if requested
        if cmd_config['load_config'] and cmd_config['load_config'].endswith('.json'):
            file_config = read_config(cmd_config['load_config'])
            config = self.build_config(cmd_config=cmd_config, file_config=file_config)
        elif cmd_config['load_config'] and cmd_config['load_config'].endswith('.py'):
            config = cmd_config
            runpy.run_path(cmd_config['load_config'])
        else:
            config = cmd_config

        # trigger after_config_build callback
        callbacks.trigger('after_config_build', config=config)

        # At this point the config is 'complete'
        # While modules may add settings/etc to the config later on, the actual config is feature complete now
        # and can be saved to disk.
        if config.pop('store_json'):
            path = os.path.join(config['output_prefix'], config['output_path']) + '.json'
            write_config(config, path)

        # Construct path in which all the modules are run.
        path = [self._all_modules[name]() for name in
                config['input_modules'] + config['ana_modules'] + config['output_modules']]

        for module in path:
            log.info("Processing {0}...".format(module.label))
            module(config)
            update_with_default(config['objects'])

    def parse_args(self):
        """ Parse arguments. To set log level, load additional module parsers etc. the sys.args[1:] are parsed
            multiple times.
        :return: dict of parsed args
        """
        base_parser = SettingParser(add_help=False)
        base_parser_group = base_parser.add_argument_group(title='Base Parser', description='')
        base_parser_group.add_argument("--log-level", default="info", help="Set the log level.")
        base_parser_group.add_argument("--list-modules", action='store_true', help="List all available modules.")
        # Parse only log level to set it as early as possible
        args = vars(base_parser.parse_known_args()[0])
        # Set log level
        log_level = getattr(logging, args['log_level'].upper(), None)
        if not isinstance(log_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig(format='%(message)s', level=log_level)
        # If module list requested, print it and exit program
        if args['list_modules']:
            for label, module in self._all_modules.iteritems():
                print label
            sys.exit(0)

        base_parser_group.add_argument("--input-modules", nargs='+', default=['RootModule'], help="Input modules .")
        base_parser_group.add_argument("--ana-modules", nargs='+', default=[], help="Analysis modules.")
        base_parser_group.add_argument("--output-modules", nargs='+', default=['PlotModule'], help="Output modules.")
        # Parse also the modules to add their parsers
        args = vars(base_parser.parse_known_args()[0])

        module_parsers = [self._all_modules[name]().parser for name in
                          args['input_modules'] + args['ana_modules'] + args['output_modules']]

        # Additional arguments for complete parser
        base_parser_group.add_argument("-p", "--print-config", default=False, action="store_true",
                                       help="Print out the JSON config before running Artus.")
        base_parser_group.add_argument("-l", "--load-config", default=None,
                                       help="Load a json config from a file.")
        base_parser_group.add_argument("--store-json", type='bool', default=True,
                                       help="Save the config as json file.")

        # Final parser consists of baseparser + active module parsers
        parser = SettingParser(parents=[base_parser] + module_parsers,
                               description='''Plotting tool to read, manipulate and plot root objects.''')

        args = vars(parser.parse_args())
        return args

    def build_config(self, cmd_config, file_config):

        # list of args provided on command line
        provided_args = cmd_config.pop('provided_args')
        merge(file_config, cmd_config, precedence_keys=provided_args)

        config = file_config
        return config

        # def _perform_lookup_replacement(self):
        #     """ Searches for the occurences of keys in the lookup_dict and replaces the values
        #         in the config with the values from the lookup dict.
        #     """
        #     # Perform global replacements:
        #     for k, v in self.config.items():
        #         if isinstance(v, basestring) and k in lookup_dict:
        #             for lk, lv in lookup_dict[k].items():
        #                 # check if string contains any key from lookup dict
        #                 if lk in v:
        #                     self.config[k] = self.config[k].replace(lk, lv)
        #         elif isinstance(v, list) and k in lookup_dict:
        #             for i in xrange(len(v)):
        #                 for lk, lv in lookup_dict[k].items():
        #                     # check if string contains any key from lookup dict
        #                     if lk in v[i]:
        #                         self.config[k][i] = self.config[k][i].replace(lk, lv)
        #     # perform replacement for object dict keys
        #     for id in self.config['objects']:
        #         for k, v in self.config['objects'][id].items():
        #             if isinstance(v, basestring) and k in lookup_dict:
        #                 for lk, lv in lookup_dict[k].items():
        #                     # check if string contains any key from lookup dict
        #                     if lk in v:
        #                         self.config['objects'][id][k] = self.config['objects'][id][k].replace(lk, lv)


def update_with_default(data):
    for id, item in data.iteritems():
        if id == '_default':
            continue
        data[id] = dict(data['_default'].items() + item.items())
