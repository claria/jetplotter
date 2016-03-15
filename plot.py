#!/usr/bin/env python2
import os
import sys

sys.path.append(os.path.dirname(__file__))
if sys.version_info < (2, 7):
    print 'Need at least python 2.7'
    sys.exit(1)

from src.core import Plotter

def plot(config=None, log_level='info'):
    """Initializes and runs the core."""
    plotter = Plotter()
    plotter(config=config, log_level=log_level)


if __name__ == '__main__':
    plot()
