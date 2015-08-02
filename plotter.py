#!/usr/bin/env python

import argparse

from settings import SettingListAction, SettingList
import plotting
import root_input
import ana_modules


def main():

    # Args Parsing
    root_input_parser = root_input.get_parser()
    plotting_parser = plotting.get_parser()
    # Additional modules
    modules = ['NormalizeObj', 'SimpleRatioToFirstObj']
    active_modules = [ana_modules.get_module(name) for name in modules]
    # Add parsers of additional modules
    ana_modules_parsers = [module.parser for module in active_modules]
    additional_parsers = [root_input_parser, plotting_parser] + ana_modules_parsers

    parser = argparse.ArgumentParser(parents=additional_parsers)
    parser.register('type','bool',plotting.str2bool)

    args = vars(parser.parse_args())
    # Input
    root_objects = root_input.get_root_objects(**args)

    for module in active_modules:
        module.run(root_objects, **args)

    # Plot the root objects
    plot = plotting.get_plot(**args)
    # plot each object
    for i, object in enumerate(root_objects):
        args['idx'] = i
        plot.plot(object, **args)
    # Save plot
    plot.finish()

if __name__ == '__main__':
    main()
