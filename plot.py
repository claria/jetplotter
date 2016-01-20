#!/usr/bin/env python2
import os
import sys

sys.path.append(os.path.dirname(__file__))
if sys.version_info < (2, 7):
    print 'Need at least python 2.7'
    sys.exit(1)

import logging

from src.core import Plotter

log = logging.getLogger(__name__)


def plot(config=None):
    """Initializes and runs the core."""
    plotter = Plotter()
    plotter(config=config)


if __name__ == '__main__':
    plot()
