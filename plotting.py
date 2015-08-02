import argparse
import matplotlib
import matplotlib.pyplot as plt

from baseplot import BasePlot
from baseplot import plot_errorbar, plot_band, add_axis_text

from settings import SettingListAction

from root2mpl import MplObject1D



def get_parser():

    parser = argparse.ArgumentParser(add_help=False)
    # Register new keyword 'bool' for parser
    parser.register('type','bool',str2bool) 
    plotting_group = parser.add_argument_group('Plotting')
    plotting_group.register('type','bool',str2bool) 

    # Plot objects options
    plotting_group.add_argument('--labels', nargs='+', default='__nolegend__', action=SettingListAction, help='Legend labels for each plot')
    plotting_group.add_argument('--colors', nargs='+', default=[], help='Colors for each plot')

    plotting_group.add_argument('--x-errs', type='bool', default=[True], action=SettingListAction, help='Show x-errors.')
    plotting_group.add_argument('--y-errs', type='bool', default=[True], action=SettingListAction, help='Show y-errors.')

    plotting_group.add_argument('--styles', default=['errorbar'], action=SettingListAction,
                                choices=['errorbar', 'band', 'line'], 
                                help='Style of the plotted object.')

    plotting_group.add_argument('--steps', type='bool', default=[False], action=SettingListAction, help='Plot stepped, if possible.')

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
        self.x_lims = [float(v) if not (v is None or v.lower() == 'none') else None for v in self.x_lims ]
        self.y_lims = kwargs.pop('y_lims', (None, None))
        self.y_lims = [float(v) if not (v is None or v.lower() == 'none') else None for v in self.y_lims ]

        self.x_log = kwargs.pop('x_log', False)
        self.y_log = kwargs.pop('y_log', False)

        self.x_label = kwargs.pop('x_label', '')
        self.y_label = kwargs.pop('y_label', '')

        self.show_legend = kwargs.pop('show_legend', True)
        self.legend_loc = kwargs.pop('legend_loc', 'best')

        self.texts = kwargs.pop('ax_texts', [])

        self.labels = kwargs.pop('labels')
        self.colors = kwargs.pop('x_errs')
        self.colors = kwargs.pop('y_errs')
        self.style = kwargs.pop('styles')
        self.steps = kwargs.pop('steps')
        self.idx = 0

    def plot(self, root_obj, style=None, **kwargs):
        mpl_obj = MplObject1D(root_obj)
        idx = kwargs.pop('idx', self.idx)
        style = kwargs.pop('styles')[idx]
        label = kwargs.pop('labels')[idx]
        step = kwargs.pop('steps')[idx]
        xerrs = kwargs.pop('x_errs')[idx]
        yerrs = kwargs.pop('y_errs')[idx]
        if style == 'errorbar':
            plot_errorbar(mpl_obj, ax=self.ax, show_xerr=xerrs, label=label, show_yerr=yerrs, marker='.', linestyle=None, step=True)
        elif style == 'band' :
            plot_band(mpl_obj, ax=self.ax, label=label, step=step)
        else:
            raise ValueError('Style {0} not supported.'.format(style))


    def make_plots(self):

        for i, histo in enumerate(self.histos):
            self.plot(histo)


    def finish(self):

        # Add axis texts
        # TODO refactor into function
        for text in self.texts:
            print text
            text, loc = text.rsplit(':', 1)
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

