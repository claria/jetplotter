#!/usr/bin/env python

from src.core import Plotter

import logging
log = logging.getlogger(__name__)

def main():
    """Initializes and runs the core."""
    plotter = Plotter()
    plotter()

if __name__ == '__main__':
    main()
