#!/usr/bin/env python

import argparse

from settings import AutoGrowListAction, AutoGrowList
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

    args['root_filenames'] = ['~/dust/dijetana/ana/CMSSW_7_2_3/unf_fastNLO.root:ptavg_yb_00_10_ys_00_10/h_genptavg',
                              '~/dust/dijetana/ana/CMSSW_7_2_3/unf_fastNLO.root:ptavg_yb_00_10_ys_00_10/h_recoptavg',
                              'unf_XSNLO.root:h_recoptavg'
                              ]
    args['x_log'] = True
    args['x_lims'] = (50., 3000.)
    args['y_lims'] = (0.5, 1.5)
    args['x_label'] = 'pT_avg'
    args['y_label'] = 'Ratio to Gen'
    args['labels'] = ['Gen (fastNLO)', 'Smeared (fastNLO)', 'Unf. smeared']
    args['output_path'] = 'nloplot.png'
    args['steps'] = AutoGrowList(True)
    args['styles'] = AutoGrowList(['errorbar'])
    args['x_errs'] = AutoGrowList(True)
    args['y_errs'] = AutoGrowList(True)
    args['scale_objs'] = AutoGrowList([1.0, 1.0, 1.0])
    args['ax_texts'] = ['$y_s < 1.0$\n$y_b < 1.0$:0.1,0.8']
    

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
