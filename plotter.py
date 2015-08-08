#!/usr/bin/env python

import argparse
import core
import json
import os
import sys

import root_input
import modules
import plotting
from settings import AutoGrowListAction, AutoGrowList
from core import Plotter

def main():

    plotter = Plotter()
    plotter()




if __name__ == '__main__':
    main()
