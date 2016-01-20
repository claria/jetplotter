#!/usr/bin/env python2
import argparse
import os
import runpy
import sys
import imp

import logging

from util.config_tools import read_config
from plot import plot

from multiprocessing import Pool

log = logging.getLogger(__name__)


def multi_plot():
    """Initializes and runs the core."""
    parser = argparse.ArgumentParser(description='Proces multiple plot configs.')
    parser.add_argument("-l", "--load-config", default=[], nargs='+', 
                        help="Process multiple configs.")
    parser.add_argument("-j", "--jobs", default=6, type=int, help="Number of jobs.")
    parser.add_argument("--no-mp", default=False, action='store_true', help="Do not use multiproccessing, but a simple loop.")
    args = vars(parser.parse_args()) 
    # empty sys args
    sys.argv = sys.argv[:1]

    # Process pool

    configs = []

    for item in args.pop('load_config', []):
            if item.endswith('.json'):
                configs.append(read_config(item))
            elif item.endswith('.py'):
                conf_module = imp.load_source('config', item)
                config = conf_module.get_config()
                if isinstance(config, (list, tuple)):
                    configs += config
                else:
                    configs.append(config)
            else:
                raise ValueError('The file type of {0} is not supported.'.format(item))

    if args['no_mp']:
        for config in configs:
            plot(config)
    else:
        pool = Pool(processes=args['jobs'])
        pool.map(plot, configs)
        pool.close()
        pool.join()


if __name__ == '__main__':
    multi_plot()
