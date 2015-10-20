import os
import sys
import logging
import runpy

from module_handler import discover_modules
from util.config_tools import merge, read_config, write_config, ConfigDict
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

        # Prepare configs from parsed args and provided input configs/python files
        config = self.build_config()

        # Triggered after config built
        callbacks.trigger('after_config', config=config)

        # At this point the config is 'complete'
        # While modules may add settings/etc to the config later on, the actual config is feature complete now
        # and can be saved to disk.
        if config.pop('store_json'):
            path = os.path.splitext(os.path.join(config['output_prefix'], config['output_path']))[0]
            write_config(config, path + '.json')

        # Run all modules
        for module in [self._all_modules[name]() for name in config['input_modules']]:
            log.info("Processing {0}...".format(module.label))
            callbacks.trigger('before_module_{0}'.format(module), config=config)
            module(config)
            callbacks.trigger('after_module_{0}'.format(module), config=config)
            update_with_default(config['objects'])

        # Triggered after all input modules processed.
        callbacks.trigger('after_input_modules', config=config)

        for module in [self._all_modules[name]() for name in config['ana_modules']]:
            log.info("Processing {0}...".format(module.label))
            callbacks.trigger('before_module_{0}'.format(module), config=config)
            module(config)
            callbacks.trigger('after_module_{0}'.format(module), config=config)
            update_with_default(config['objects'])

        # Triggered after all ana modules processed.
        callbacks.trigger('after_ana_modules', config=config)
        for module in [self._all_modules[name]() for name in config['output_modules']]:
            log.info("Processing {0}...".format(module.label))
            callbacks.trigger('before_module_{0}'.format(module), config=config)
            module(config)
            callbacks.trigger('after_module_{0}'.format(module), config=config)
            update_with_default(config['objects'])

        # Triggered after all output modules processed.
        callbacks.trigger('after_ana_modules', config=config)

    def build_config(self):
        """ Parse arguments. To set log level, load additional module parsers etc. the sys.args[1:] are parsed
            multiple times.
        :return: dict of parsed args
        """
        base_parser = SettingParser(add_help=False)
        base_parser_group = base_parser.add_argument_group(title='Base Parser', description='')
        base_parser_group.add_argument("--log-level", default="info", help="Set the log level.")
        base_parser_group.add_argument("--list-modules", action='store_true', help="List all available modules.")
        base_parser_group.add_argument("-l", "--load-config", default=[], nargs='+',
                                       help="Load json configs, with decreasing precedence,  or a python scripts from file.")

        # Parse only log level to set it as early as possible
        args = vars(base_parser.parse_known_args()[0])
        # Set log level
        log_level = getattr(logging, args['log_level'].upper(), None)
        if not isinstance(log_level, int):
            raise ValueError('Invalid log level: %s' % log_level)
        logging.basicConfig(format='%(message)s', level=log_level)

        # Discover all available modules
        self._all_modules = discover_modules()

        # If module list requested, print it and exit program
        if args['list_modules']:
            for label, module in self._all_modules.iteritems():
                print label
            sys.exit(0)

        # Load configs/python scripts from files if requested
        file_config = ConfigDict()
        for item in args.pop('load_config', []):
            if item.endswith('.json'):
                merge(file_config, read_config(item))
            elif item.endswith('.py'):
                runpy.run_path(item)
            else:
                raise ValueError('The file type of {0} is not supported.'.format(item))

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
        base_parser_group.add_argument("--store-json", type='bool', default=True,
                                       help="Save the config as json file.")
        base_parser_group.add_argument("--merge-args", nargs='+', default=[],
                                       help=("If json file configs and command line configs are provided the settings are "
                                       "merged for the provided args. Works only for list arguments."))

        # Final parser consists of baseparser + active module parsers
        parser = SettingParser(parents=[base_parser] + module_parsers,
                               description='''Plotting tool to read, manipulate and plot root objects.''')

        # Triggers before actual parameters are parsed.
        callbacks.trigger('before_parsing', config=file_config)

        # Final parsing of parameters
        args = vars(parser.parse_args())

        # If a config was loaded, merge it with the args
        if file_config:
            provided_args = args.pop('provided_args')
            merge_args = args.pop('merge_args')
            merge(file_config, args, precedence_keys=provided_args, merge_keys=merge_args)
            config = file_config
        else:
            config = args

        # ConfigDict is just a simple wrapper around a dict with some helper functions.
        return ConfigDict(config)

def update_with_default(data):
    """
    Updates all objects with values from '_default' object.
    """
    for id, item in data.iteritems():
        if id == '_default':
            continue
        data[id] = dict(data['_default'].items() + item.items())
