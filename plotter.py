#!/usr/bin/env python

import argparse

from settings import AutoGrowListAction, AutoGrowList
import plotting
import root_input
import ana_modules
import core
import json
import os


def main():

    # Args Parsing
    root_input_parser = root_input.get_parser()
    plotting_parser = plotting.get_parser()

    modules = ['RatioToObj']
    active_modules = [ana_modules.get_module(name) for name in modules]
    parser = core.UserParser(parents=[root_input_parser, plotting_parser] + [module.parser for module in active_modules])
    parser.add_argument("--log-level", default="info", help="Log level.")
    parser.add_argument("-p", "--print-config", default=False, action="store_true",
                      help="Print out the JSON config before running Artus.")
    parser.add_argument("-l", "--load-config", default=None,
                      help="Print out the JSON config before running Artus.")

    config = vars(parser.parse_args())

    core.print_config(config)
    if config['load_config']:
        file_config = core.read_config(config['load_config'])
        core.update_dict(file_config, config)
        config = file_config
        # config = dict(file_config.items() + config.items())
    core.print_config(config)

    data = config['settings']
    root_input.read_input(data)

    if config['print_config']:
        core.print_config(config)


    core.update_with_default(data)

    for module in active_modules:
        module(data)

    # Plot the root objects
    plot = plotting.get_plot(**config)
    # plot each object
    for id, item in data.iteritems():
        if not 'obj' in item or not item['plot'] or id.startswith('_'):
            continue
        plot.plot(**item)
    # Save plot
    plot.finish()
    # write config
    path = os.path.join(config['output_prefix'], config['output_path']).replace('.png', '.json')
    core.save_config(config, path)




if __name__ == '__main__':
    main()
