#!/usr/bin/env python2
import argparse
import os
import runpy
import sys
import imp

import logging
import traceback

from util.config_tools import read_config
import signal
from plot import plot

from multiprocessing import Pool

log = logging.getLogger(__name__)

def init_worker():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def run_worker(config, log_level='info'):
    try:
        plot(config, log_level=log_level)
    except Exception as e:
        print 'Caught exception in worker thread (x = %d):' % x
        traceback.print_exc()
        raise e

def multi_plot():
    """Initializes and runs the core."""
    parser = argparse.ArgumentParser(description='Proces multiple plot configs.')
    parser.add_argument("-l", "--load-config", default=[], nargs='+', 
                        help="Process multiple configs.")
    parser.add_argument("-j", "--jobs", default=6, type=int, help="Number of jobs.")
    parser.add_argument("--no-mp", default=False, action='store_true', help="Do not use multiproccessing, but a simple loop.")
    parser.add_argument("--log-level", default='info', help="Set the log level.")
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
            plot(config, log_level=args['log_level'])
    else:
        print 'Initializing {0} worker processes'.format(args['jobs'])
        pool = Pool(processes=args['jobs'], initializer=init_worker)

        try:
            for config in configs:
                pool.apply_async(run_worker, (config,args['log_level']))
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()

if __name__ == '__main__':
    multi_plot()
