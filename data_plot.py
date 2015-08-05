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
    modules = ['NormalizeObj']
    active_modules = [ana_modules.get_module(name) for name in modules]
    # Add parsers of additional modules
    ana_modules_parsers = [module.parser for module in active_modules]
    additional_parsers = [root_input_parser, plotting_parser] + ana_modules_parsers

    parser = argparse.ArgumentParser(parents=additional_parsers)
    parser.register('type','bool',plotting.str2bool)

    args = vars(parser.parse_args())

    args['root_filenames'] = ['~/XSNLO_CT10.root?ptavg_yb_00_10_ys_00_10/xsnlo',
                              '~/XSNLO_NNPDF30.root?ptavg_yb_00_10_ys_00_10/xsnlo',
                              '~/XSNLO_MMHT.root?ptavg_yb_00_10_ys_00_10/xsnlo',
                              'unf_DATA.root?h_ptavg',
                              'np_factors.root?genptavg_yb_00_10_ys_00_10/np_histo',
                              ]
    args['x_log'] = True
    args['figsize'] = 10., 7.
    args['x_lims'] = (50., 3000.)
    args['y_lims'] = (0.5, 1.5)
    args['x_label'] = 'pT_avg'
    args['y_label'] = 'Ratio to NLO'
    args['labels'] = ['NLOxNP (CT10)', 'NLOxNP (NNPDF30)', 'NLOxNP (MMHT)', 'Data (Unf.)', 'np']
    args['output_path'] = 'data.png'
    args['steps'] = AutoGrowList(True)
    args['styles'] = AutoGrowList(['errorbar'])
    args['x_errs'] = AutoGrowList(True)
    args['y_errs'] = AutoGrowList(True)
    args['colors'] = AutoGrowList(['#1f77b4', '#ff7f0e', '#2ca02c', 'black'])
    args['scale_objs'] = AutoGrowList([1.0, 1.0, 1.0,  'width', 1.0])
    args['ax_texts'] = ['$y_s < 1.0$\n$y_b < 1.0$?0.1,0.8']
    

    # Input
    root_objects = root_input.get_root_objects(**args)
    root_objects[0].Multiply(root_objects[4])
    root_objects[1].Multiply(root_objects[4])
    root_objects[2].Multiply(root_objects[4])
    del root_objects[4]
    ana_modules.ratio_to_obj(root_objects[3], root_objects[0], False)
    ana_modules.ratio_to_obj(root_objects[2], root_objects[0], False)
    ana_modules.ratio_to_obj(root_objects[1], root_objects[0], False)
    ana_modules.ratio_to_obj(root_objects[0], root_objects[0], False)


    for module in active_modules:
        module(root_objects, **args)

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
