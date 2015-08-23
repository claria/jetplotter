import itertools
import re

import matplotlib
import matplotlib.pyplot as plt

from util.baseplot import BasePlot

BasePlot.init_matplotlib()

from util.baseplot import plot_errorbar, plot_band, plot_line, plot_histo, plot_heatmap, add_axis_text
from modules.base_module import BaseModule

import logging

from src.lookup_dict import get_lookup_val

log = logging.getLogger(__name__)


class PlotModule(BaseModule):
    """Plotting output module for 1d and 2d plots using the matplotlib library. 

       All objects plotted are read from the \'objects\' dict in the configs. You can
       use all the id based settings to manipulate the appearance of the objects and the
       standard arguments to adapt the axis and figure.
    """

    def __init__(self):
        super(PlotModule, self).__init__()
        # Plot object options
        self.arg_group.add_argument('--label', type='str2kvstr', nargs='+', default=['__nolegend__'], action='setting',
                                    help='Legend labels for each plot')
        self.arg_group.add_argument('--color', type='str2kvstr', nargs='+',
                                    default='auto', action='setting',
                                    help='Colors for each plot.')
        self.arg_group.add_argument('--edgecolor', type='str2kvstr', nargs='+',
                                    default='auto', action='setting',
                                    help='Edgecolor for each plot.')
        self.arg_group.add_argument('--cmap', type='str2kvstr', nargs='+',
                                    default='viridis', action='setting',
                                    help='Colormap used for heatmaps.')
        self.arg_group.add_argument('--hatch', type='str2kvstr', nargs='+',
                                    default=None, action='setting',
                                    help='Hatch for each plot')
        self.arg_group.add_argument('--linestyle', type='str2kvstr', nargs='+',
                                    default='', action='setting',
                                    help='Linestyle for each plot')
        self.arg_group.add_argument('--marker', type='str2kvstr', nargs='+',
                                    default='.', action='setting',
                                    help='Marker for errorbars for each plot.')
        self.arg_group.add_argument('--x-err', type='str2kvbool', nargs='+', default=True, action='setting',
                                    help='Show x-errors.')
        self.arg_group.add_argument('--y-err', type='str2kvbool', nargs='+', default=True, action='setting',
                                    help='Show y-errors.')
        self.arg_group.add_argument('--alpha', type='str2kvfloat', nargs='+', default=1.0, action='setting',
                                    help='Alpha value in plot.')
        self.arg_group.add_argument('--capsize', type='str2kvint', nargs='+', default=0, action='setting',
                                    help='Capsize of errorbars in plot.')
        self.arg_group.add_argument('--zorder', type='str2kvfloat', nargs='+', default=1.0, action='setting',
                                    help='Alpha value in plot.')
        self.arg_group.add_argument('--style', default='errorbar', type='str2kvstr', nargs='+', action='setting',
                                    help='Style of the plotted object.')
        self.arg_group.add_argument('--step', type='str2kvbool', nargs='+', default=False, action='setting',
                                    help='Plot the data stepped at the xerr edges.')
        self.arg_group.add_argument('--axis', type='str2kvstr', nargs='+', default='ax', action='setting',
                                    help='Plot the object in the following axis.')

        # Figure options
        self.arg_group.add_argument('--fig-size', type=float, nargs=2, default=None, help='Size of figure.')
        self.arg_group.add_argument('--output-path', default='plot.png', help='Path to output file.')
        self.arg_group.add_argument('--output-prefix', default='plots/', help='Prefix to output paths.')

        # Axis options
        self.arg_group.add_argument('--add-subplot', default=False, type='bool', help='Add subplot with name ax1.')
        self.arg_group.add_argument('--x-lims', nargs=2, default=[None, None], help='X limits of plot.')
        self.arg_group.add_argument('--y-lims', nargs=2, default=[None, None], help='Y limits of plot.')
        self.arg_group.add_argument('--y-subplot-lims', nargs=2, default=[None, None], help='Y limits of subplot.')
        self.arg_group.add_argument('--z-lims', nargs=2, default=[None, None],
                                    help='Z limits of plot (only used in 2d plots).')

        self.arg_group.add_argument('--x-log', default=False, type='bool', help='Use log scale for x-axis.')
        self.arg_group.add_argument('--y-log', default=False, type='bool', help='Use log scale for y-axis.')
        self.arg_group.add_argument('--z-log', default=False, type='bool', help='Use log scale for z-axis.')

        self.arg_group.add_argument('--x-label', default='', help='Label of the x axis.')
        self.arg_group.add_argument('--y-label', default='', help='Label of the y axis.')
        self.arg_group.add_argument('--y-subplot-label', default='', help='Label of the y axis.')
        self.arg_group.add_argument('--z-label', default='', help='Label of the z axis.')

        self.arg_group.add_argument('--show-legend', type='bool', default=True, help='Show a legend.')
        self.arg_group.add_argument('--legend-loc', default='best', help='Legend location.')

        self.arg_group.add_argument('--plot-id', default=r'^(?!_).*',
                                    help='All ids matching are passed to plot-module.'
                                         ' Default matches everything not starting with a underscore.')
        self.arg_group.add_argument('--ax-texts', nargs='+', default=[],
                                    help='Add text to plot. Syntax is \'Text?1.0,1.0\' with loc 1.0,1.0')
        self.arg_group.add_argument('--ax-vlines', nargs='+', default=[],
                                    help='Add vertical lines to plot. Syntax is y_pos?color?lw.')
        self.arg_group.add_argument('--ax-hlines', nargs='+', default=[],
                                    help='Add horizontal lines to plot. Syntax is y_pos?color?lw.')

    def __call__(self, config):
        plot = Plot(**config)
        # plot each object
        id_regex = config.get('plot_id')
        for id, item in config['objects'].iteritems():
            if re.match(id_regex, id):
                log.info('Drawing id {0}'.format(id))
                plot.plot(**item)
        # Save plot
        plot.finish()


def get_plot(*args, **kwargs):
    return Plot(*args, **kwargs)


class Plot(BasePlot):
    def __init__(self, histos=None, **kwargs):

        super(Plot, self).__init__(**kwargs)
        if not kwargs['add_subplot']:
            self.ax = self.fig.add_subplot(111)
            self.ax1 = None
        else:
            self.ax = plt.subplot2grid((4, 1), (0, 0), rowspan=3)
            self.ax1 = plt.subplot2grid((4, 1), (3, 0), rowspan=1)
        self.histos = histos

        self.x_lims = kwargs.pop('x_lims', (None, None))
        self.x_lims = [any2float(v) for v in self.x_lims]
        self.y_lims = kwargs.pop('y_lims', (None, None))
        self.y_lims = [any2float(v) for v in self.y_lims]
        self.y_subplot_lims = kwargs.pop('y_subplot_lims', (None, None))
        self.y_subplot_lims = [any2float(v) for v in self.y_subplot_lims]
        self.z_lims = kwargs.pop('z_lims', (None, None))
        self.z_lims = [any2float(v) for v in self.z_lims]

        self.x_log = kwargs.pop('x_log', False)
        self.y_log = kwargs.pop('y_log', False)
        self.z_log = kwargs.pop('z_log', False)

        self.x_label = get_lookup_val('x_label', kwargs.pop('x_label', ''))
        self.y_label = get_lookup_val('y_label', kwargs.pop('y_label', ''))
        self.y_subplot_label = get_lookup_val('y_label', kwargs.pop('y_subplot_label', ''))
        self.z_label = get_lookup_val('z_label', kwargs.pop('z_label', ''))

        self.show_legend = kwargs.pop('show_legend', True)
        self.legend_loc = kwargs.pop('legend_loc', 'best')

        self.texts = kwargs.pop('ax_texts', [])
        self.vlines = kwargs.pop('ax_vlines', [])
        self.hlines = kwargs.pop('ax_hlines', [])

        self.auto_colors = itertools.cycle(matplotlib.rcParams['axes.color_cycle'])

        self.colorbar_mappable = None

    def plot(self, **kwargs):
        style = kwargs.pop('style', 'errorbar')
        kwargs['label'] = get_lookup_val('label', kwargs.get('label'))
        # Plot object on this axis
        axis_name = kwargs.pop('axis', 'ax')
        try:
            ax = getattr(self, axis_name)
        except AttributeError as e:
            log.critical('The axis name {0} does not exist.'.format(axis_name))
            log.critical(e)
            raise

        if kwargs['color'] == 'auto':
            kwargs['color'] = next(self.auto_colors)
        if kwargs['edgecolor'] == 'auto':
            kwargs['edgecolor'] = kwargs['color']

        kwargs['color'] = get_lookup_val('color', kwargs.get('color'))
        # Facecolor is always set using the color argument.
        kwargs['facecolor'] = kwargs['color']

        kwargs['edgecolor'] = get_lookup_val('edgecolor', kwargs.get('edgecolor'))
        if style == 'errorbar':
            artist = plot_errorbar(ax=ax, **kwargs)
        elif style == 'band':
            artist = plot_band(ax=ax, **kwargs)
        elif style == 'histo':
            artist = plot_histo(ax=ax, **kwargs)
        elif style == 'line':
            artist = plot_line(ax=ax, **kwargs)
        elif style == 'heatmap':
            # special case for z scale and lims in heatmaps since they have to be set by the object instead of the axis.
            print kwargs
            kwargs['z_log'] = self.z_log
            kwargs['z_lims'] = self.z_lims
            artist = plot_heatmap(ax=self.ax, **kwargs)
            self.colorbar_mappable = artist
        else:
            raise ValueError('Style {0} not supported.'.format(style))
        return artist

    def make_plots(self):

        for i, histo in enumerate(self.histos):
            self.plot(histo)

    def finish(self):

        # Add colorbar if there is a mappable
        if self.colorbar_mappable:
            cb = self.fig.colorbar(self.colorbar_mappable, ax=self.ax)
            if self.z_label:
                cb.set_label(self.z_label)

        # Add axis texts
        for text in self.texts:
            text = get_lookup_val('ax_texts', text)
            if not '?' in text:
                loc = '0.0,0.0'
            else:
                text, loc = text.rsplit('?', 1)
            add_axis_text(self.ax, text, loc=loc)

        # Add horizontal lines to ax
        for hline in self.hlines:
            ypos, color, lw = hline.split('?')
            self.ax.axhline(y=float(ypos), color=color, lw=lw, zorder=0.99)
        # Add vertical lines to ax
        for vline in self.vlines:
            xpos, color, lw = vline.split('?')
            self.ax.axvline(y=float(ypos), color=color, lw=lw)

        self.ax.set_ylim(ymin=self.y_lims[0], ymax=self.y_lims[1])
        self.ax.set_xlim(xmin=self.x_lims[0], xmax=self.x_lims[1])

        if self.ax1:
            self.ax1.set_ylim(ymin=self.y_subplot_lims[0], ymax=self.y_subplot_lims[1])
        # a specified position of the label can be set via label?centered
        x_pos = self.x_label.rsplit('?', 1)[-1].lower()
        if x_pos == 'center':
            x_pos = {'position': (0.5, 0.0), 'va': 'top', 'ha': 'center'}
            self.x_label = self.x_label.rsplit('?', 1)[0]
        else:
            x_pos = {'position': (1.0, 0.0), 'va': 'top', 'ha': 'right'}
        if self.ax1:
            self.ax1.set_xlabel(self.x_label, **x_pos)
        else:
            self.ax.set_xlabel(self.x_label, **x_pos)

        y_pos = self.y_label.rsplit('?', 1)[-1].lower()
        if y_pos == 'center':
            y_pos = {'position': (0.0, 0.5), 'va': 'center', 'ha': 'right'}
            self.y_label = self.y_label.rsplit('?', 1)[0]
        else:
            y_pos = {'position': (0.0, 1.0), 'va': 'top', 'ha': 'right'}
        self.ax.set_ylabel(self.y_label, **y_pos)

        if self.ax1:
            self.ax1.set_ylabel(self.y_subplot_label)

        self.ax.set_xscale('log' if self.x_log else 'linear')
        if self.y_log:
            self.ax.set_yscale('log', nonposy='clip')
        else:
            self.ax.set_yscale('linear')

        if self.show_legend:
            handles, labels = self.ax.get_legend_handles_labels()
            if any(labels):
                self.ax.legend(handles, labels, loc=self.legend_loc)
            else:
                pass
                log.debug('Omit legend since all labels are empty.')

        if self.ax1:
            # self.ax.get_xaxis().set_ticks([])
            plt.setp(self.ax.get_xticklabels(), visible=False)
            self.ax1.set_xscale(self.ax.get_xscale())
            self.ax1.set_xlim(self.ax.get_xlim())
            plt.subplots_adjust(hspace=0.15)

        self.save_fig()
        plt.close(self.fig)


def str2bool(v):
    """ Parse string content to bool."""
    return v.lower() in ("yes", "true", "t", "1")


def any2float(v):
    """Return float if parseable, else None."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None
