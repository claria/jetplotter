#!/usr/bin/env python
import os
import sys
# sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from src.core import Plotter

import logging
log = logging.getLogger(__name__)

def main():
    """Initializes and runs the core."""
    plotter = Plotter()
    plotter()

if __name__ == '__main__':
    main()
