#!/usr/bin/env python

import argparse

from settings import AutoGrowListAction, AutoGrowList
import plotting
import root_input
import ana_modules
import core


def main():

    # Args Parsing
    root_input_parser = root_input.get_parser()
    # plotting_parser = plotting.get_parser()

    parser = core.UserParser(parents=[root_input_parser])
    parser.register('type','bool',plotting.str2bool)
    args = vars(parser.parse_args())
    print 'args', args

    # Input
    data = root_input.read_input(**args)
    print data

if __name__ == '__main__':
    main()
