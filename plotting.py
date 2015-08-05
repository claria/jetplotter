import argparse
import matplotlib
import matplotlib.pyplot as plt

from baseplot import BasePlot
from baseplot import plot_errorbar, plot_band, add_axis_text

from settings import AutoGrowListAction, AutoGrowList

from root2mpl import MplObject1D



def get_parser():

    parser = argparse.ArgumentParser(add_help=False)
    # Register new keyword 'bool' for parser
    parser.register('type','bool',str2bool) 
    plotting_group = parser.add_argument_group('Plotting')
    plotting_group.register('type','bool',str2bool) 

    # Plot objects options
    plotting_group.add_argument('--labels', nargs='+', default=AutoGrowList(['__nolegend__']), action=AutoGrowListAction, help='Legend labels for each plot')
    plotting_group.add_argument('--colors', nargs='+', default=AutoGrowList(matplotlib.rcParams['axes.color_cycle']), help='Colors for each plot')

    plotting_group.add_argument('--x-errs', type='bool', default=AutoGrowList([True]), action=AutoGrowListAction, help='Show x-errors.')
    plotting_group.add_argument('--y-errs', type='bool', default=AutoGrowList([True]), action=AutoGrowListAction, help='Show y-errors.')

    plotting_group.add_argument('--styles', default=AutoGrowList(['errorbar']), 
                                action=AutoGrowListAction,
                                choices=['errorbar', 'band', 'line'], 
                                help='Style of the plotted object.')

    plotting_group.add_argument('--steps', type='bool', default=AutoGrowList([False]), action=AutoGrowListAction, help='Plot stepped, if possible.')

    # Axis options
    plotting_group.add_argument('--x-lims', nargs=2, default=[None, None], help='X limits of plot.')
    plotting_group.add_argument('--y-lims', nargs=2, default=[None, None], help='Y limits of plot.')

    plotting_group.add_argument('--x-log', action='store_true', help='Show x-errors.')
    plotting_group.add_argument('--y-log', action='store_true', help='Show y-errors.')

    plotting_group.add_argument('--x-label', default='', help='xlabel')
    plotting_group.add_argument('--y-label', default='', help='ylabel')

    plotting_group.add_argument('--show-legend', type='bool', default=True, help='Show a legend.')
    plotting_group.add_argument('--legend-loc', default='best', help='Legend location.')

    plotting_group.add_argument('--ax-texts', nargs='+', default=[], help='Add text to plot. Syntax is \'Text:1.0,1.0\' with loc 1.0,1.0')

    plotting_group.add_argument('--output-path', default='plot.png', help='Path to output file.')
    plotting_group.add_argument('--output-prefix', default='plots/', help='Prefix to output paths.')

    # plotting_group.add_argument('--autoscale', 'store_false', default=True, help='Autoscale plot to datalims')

    return parser


def get_plot(*args, **kwargs):
    return Plot(*args, **kwargs)


class Plot(BasePlot):

    def __init__(self, histos=None,  *args, **kwargs):

        super(Plot, self).__init__(*args, **kwargs)
        self.ax = self.fig.add_subplot(111)
        self.histos = histos

        self.x_lims = kwargs.pop('x_lims', (None, None))
        self.x_lims = [any2float(v) for v in self.x_lims ]
        self.y_lims = kwargs.pop('y_lims', (None, None))
        self.y_lims = [any2float(v) for v in self.y_lims ]

        self.x_log = kwargs.pop('x_log', False)
        self.y_log = kwargs.pop('y_log', False)

        self.x_label = kwargs.pop('x_label', '')
        self.y_label = kwargs.pop('y_label', '')

        self.show_legend = kwargs.pop('show_legend', True)
        self.legend_loc = kwargs.pop('legend_loc', 'best')

        self.texts = kwargs.pop('ax_texts', [])

        self.labels = kwargs.pop('labels')
        self.colors = kwargs.pop('colors')
        self.x_errs = kwargs.pop('x_errs')
        self.y_errs = kwargs.pop('y_errs')
        self.style = kwargs.pop('styles')
        self.steps = kwargs.pop('steps')
        self.idx = 0

    def plot(self, **kwargs):
        print kwargs
        mpl_obj = MplObject1D(kwargs.pop('obj'))
        style = kwargs.pop('styles')
        label = kwargs.pop('labels')
        step = kwargs.pop('steps')
        xerrs = kwargs.pop('x_errs')
        yerrs = kwargs.pop('y_errs')
        color = kwargs.pop('colors')
        if style == 'errorbar':
            plot_errorbar(mpl_obj, ax=self.ax, show_xerr=xerrs, color=color, label=label, show_yerr=yerrs, marker='.', linestyle=None, step=True)
        elif style == 'band' :
            plot_band(mpl_obj, ax=self.ax, label=label, step=step, color=color)
        else:
            raise ValueError('Style {0} not supported.'.format(style))


    def make_plots(self):

        for i, histo in enumerate(self.histos):
            self.plot(histo)


    def finish(self):

        # Add axis texts
        # TODO refactor into function
        for text in self.texts:
            text, loc = text.rsplit('?', 1)
            add_axis_text(self.ax, text, loc=loc)

        self.ax.set_ylim(ymin=self.y_lims[0], ymax=self.y_lims[1])
        self.ax.set_xlim(xmin=self.x_lims[0], xmax=self.x_lims[1])

        self.ax.set_xlabel(self.x_label, position=(1., 0.), va='top', ha='right')
        self.ax.set_ylabel(self.y_label)

        self.ax.set_xscale('log' if self.x_log else 'linear')
        self.ax.set_yscale('log' if self.y_log else 'linear')

        if self.show_legend:
            self.ax.legend(loc=self.legend_loc)

        self.save_fig()
        plt.close(self.fig)


def str2bool(v):
    """ Parse string content to bool."""
    return v.lower() in ("yes", "true", "t", "1")


def any2float(v):
    """Return float if parseable, else None."""
    try:
        return float(v)
    except TypeError:
        return None
