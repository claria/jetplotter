import os
from abc import ABCMeta

import numpy as np
import matplotlib
from matplotlib.colors import Normalize
from matplotlib.colors import LogNorm
import matplotlib.pyplot as plt

from root2np import R2npObject1D, R2npObject2D
from util.viridis import viridis_cmap

plt.register_cmap(cmap=viridis_cmap)

import logging

log = logging.getLogger(__name__)


class BasePlot(object):
    __metaclass__ = ABCMeta

    def __init__(self, **kwargs):

        self.init_matplotlib()

        fig_size = kwargs.pop('fig_size', None)
        if fig_size:
            self.fig = plt.figure(figsize=fig_size)
        else:
            self.fig = plt.figure()

        self.output_path = kwargs.pop('output_path', 'plot.png')
        self.output_prefix = kwargs.pop('output_prefix', 'plots')

    def save_fig(self, close_fig=True):
        """
        Save Fig to File and create directory structure
        if not yet existing.
        """
        # Check if directory exists and create if not
        path = os.path.join(self.output_prefix, self.output_path)
        directory = os.path.dirname(path)

        if directory and not os.path.exists(directory):
            os.makedirs(directory)
            # for ext in self.output_ext:
            # if not m.lower().endswith(('.png', '.jpg', '.jpeg', '.pdf', '.ps'))
            # filename = "{}.{}".format(self.output_path, ext)
        print 'Saved plot to {0}'.format(path)
        self.fig.savefig(path, bbox_inches='tight')

        if close_fig:
            plt.close(self.fig)

    @staticmethod
    def init_matplotlib():
        """
        Initialize matplotlib with rc settings.
        """
        # figure
        matplotlib.rcParams['figure.figsize'] = 10., 10.

        matplotlib.rcParams['lines.linewidth'] = 2
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.serif'] = 'lmodern'
        matplotlib.rcParams['font.sans-serif'] = ['Arial', 'Bitstream Vera Sans', 'stixsans']
        matplotlib.rcParams['font.monospace'] = 'Computer Modern Typewriter'
        matplotlib.rcParams['font.style'] = 'normal'
        matplotlib.rcParams['mathtext.fontset'] = 'stixsans'
        matplotlib.rcParams['font.size'] = 20.
        matplotlib.rcParams['legend.fontsize'] = 14.
        matplotlib.rcParams['text.usetex'] = False
        # matplotlib.rc('text.latex', preamble=r'\usepackage{helvet},\usepackage{sfmath}')
        # matplotlib.rc('text.latex', preamble=r'\usepackage{helvet}')
        # Axes
        matplotlib.rcParams['axes.linewidth'] = 2
        matplotlib.rcParams['axes.labelsize'] = 20
        matplotlib.rcParams['xtick.labelsize'] = 16
        matplotlib.rcParams['xtick.major.size'] = 8
        matplotlib.rcParams['xtick.major.width'] = 1.5
        matplotlib.rcParams['xtick.minor.size'] = 6
        matplotlib.rcParams['xtick.minor.width'] = 1.
        matplotlib.rcParams['ytick.labelsize'] = 16
        matplotlib.rcParams['ytick.major.width'] = 1.5
        matplotlib.rcParams['ytick.major.size'] = 8
        matplotlib.rcParams['ytick.minor.size'] = 6
        matplotlib.rcParams['ytick.minor.width'] = 1.
        matplotlib.rcParams['lines.markersize'] = 8

        # Saving
        matplotlib.rcParams['savefig.bbox'] = 'tight'
        matplotlib.rcParams['savefig.dpi'] = 150
        matplotlib.rcParams['savefig.format'] = 'png'
        matplotlib.rcParams['agg.path.chunksize'] = 20000

        # default color cycle
        matplotlib.rcParams['axes.color_cycle'] = ["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#CCB974", "#64B5CD"]

        matplotlib.rcParams['axes.formatter.limits'] = [-5, 5]
        # legend
        matplotlib.rcParams['legend.numpoints'] = 1
        matplotlib.rcParams['legend.fontsize'] = 19
        matplotlib.rcParams['legend.labelspacing'] = 0.3
        matplotlib.rcParams['legend.frameon'] = False
        # Saving
        matplotlib.rcParams['savefig.bbox'] = 'tight'
        matplotlib.rcParams['savefig.dpi'] = 150
        matplotlib.rcParams['savefig.format'] = 'png'
        matplotlib.rcParams['agg.path.chunksize'] = 20000

        #
        # Helper functions
        #


def add_axis_text(ax, text, loc='top right', **kwargs):
    """
    Possible Positions : top left, top right
    """
    if loc == 'top left':
        kwargs.update({'x': 0.0, 'y': 1.01, 'va': 'bottom',
                       'ha': 'left'})
    elif loc == 'top right':
        kwargs.update({'x': 1.0, 'y': 1.01, 'va': 'bottom',
                       'ha': 'right'})
    elif ',' in loc:
        x, y = map(float, loc.split(','))
        kwargs.update({'x': x, 'y': y, 'va': 'bottom',
                       'ha': 'left'})
    else:
        raise Exception('Unknown loc {0}.'.format(loc))

    ax.text(s=text, transform=ax.transAxes, **kwargs)


def autoscale(ax, xmargin=0.0, ymargin=0.0, margin=0.0):
    # User defined autoscale with margins
    x0, x1 = tuple(ax.dataLim.intervalx)
    if margin > 0:
        xmargin = margin
        ymargin = margin
    if xmargin > 0:
        if ax.get_xscale() == 'linear':
            delta = (x1 - x0) * xmargin
            x0 -= delta
            x1 += delta
        else:
            delta = (x1 / x0) ** xmargin
            x0 /= delta
            x1 *= delta
        ax.set_xlim(x0, x1)
    y0, y1 = tuple(ax.dataLim.intervaly)
    if ymargin > 0:
        if ax.get_yscale() == 'linear':
            delta = (y1 - y0) * ymargin
            y0 -= delta
            y1 += delta
        else:
            delta = (y1 / y0) ** ymargin
            y0 /= delta
            y1 *= delta
        ax.set_ylim(y0, y1)


def log_locator_filter(x, pos):
    """
    Add minor tick labels in log plots at 2* and 5*
    """
    s = str(int(x))
    if len(s) == 4:
        return ''
    if s[0] in ('2', '5'):
        return '${0}$'.format(s)
    return ''


def setval(obj, *args, **kwargs):
    """
    Apply Settings in kwargs, while defaults are set
    """
    funcvals = []
    for i in range(0, len(args) - 1, 2):
        funcvals.append((args[i], args[i + 1]))
    funcvals.extend(kwargs.items())
    for s, val in funcvals:
        attr = getattr(obj, s)
        if callable(attr):
            attr(val)
        else:
            setattr(obj, attr, val)


def ensure_latex(inp_str):
    """
    Return string with escaped latex incompatible characters.
    :param inp_str:
    :return:
    """
    chars = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\letteropenbrace{}',
        '}': r'\letterclosebrace{}',
        '~': r'\lettertilde{}',
        '^': r'\letterhat{}',
        '\\': r'\letterbackslash{}',
    }
    return ''.join([chars.get(char, char) for char in inp_str])


def steppify_bin(arr, isx=False):
    """
    Produce stepped array of arr, needed for example for stepped fill_betweens.
    Pass all x bin edges to produce stepped x arr and all y bincontents to produce
    stepped bincontents representation
    steppify_bin([1,2,3], True) 
    -> [1,2,2,3]
    steppify_bin([5,6])
    -> [5,5,6,6]
    """
    if isx:
        newarr = np.array(zip(arr[:-1], arr[1:])).ravel()
    else:
        newarr = np.array(zip(arr, arr)).ravel()
    return newarr


def plot_band(obj=None, step=False, emptybins=True, ax=None, **kwargs):
    """ Produce an errorbar plots with or without connecting lines.

    Args:
        obj: Mplobj representation of a root object.
        ax: Axis to plot on. If not specified current global axis will be used.
        x_err: If True, x errorbars will be plotted.
        yerr: If True, y errorbars will be plotted.
        emptybins: Not Implemented. Supposed to ignore/plot empty bins.
    """
    # Convert root object to mpl readable object
    obj = R2npObject1D(obj)
    # if no axis passed use current global axis
    if ax is None:
        ax = plt.gca()

    x = obj.x
    y = obj.y

    y_errl = obj.yerrl
    y_erru = obj.yerru
    if step:
        x = steppify_bin(obj.xbinedges, isx=True)
        y = steppify_bin(y)
        y_errl = steppify_bin(y_errl)
        y_erru = steppify_bin(y_erru)

    fill_between_kwargs = {k: v for k, v in kwargs.items() if
                           k in ['label', 'facecolor', 'alpha', 'edgecolor', 'zorder']}
    artist = ax.fill_between(x, y - y_errl, y + y_erru, **fill_between_kwargs)
    p = matplotlib.patches.Rectangle((0, 0), 1, 1, **fill_between_kwargs)
    ax.add_patch(p)

    return artist


def plot_histo(obj=None, emptybins=True, ax=None, **kwargs):
    """ Produce an errorbar plots with or without connecting lines.

    Args:
        obj: Mplobj representation of a root object.
        ax: Axis to plot on. If not specified current global axis will be used.
        x_err: If True, x errorbars will be plotted.
        yerr: If True, y errorbars will be plotted.
        emptybins: Not Implemented. Supposed to ignore/plot empty bins.
    """
    # Convert root object to mpl readable object
    obj = R2npObject1D(obj)
    # if no axis passed use current global axis
    if ax is None:
        ax = plt.gca()

    x = obj.x
    y = obj.y

    x = steppify_bin(obj.xbinedges, isx=True)
    y = steppify_bin(y)
    y_0 = np.zeros(y.shape)

    fill_between_kwargs = {k: v for k, v in kwargs.items() if
                           k in ['label', 'facecolor', 'alpha', 'edgecolor', 'zorder']}
    artist = ax.fill_between(x, y, y_0, **fill_between_kwargs)
    p = matplotlib.patches.Rectangle((0, 0), 1, 1, **fill_between_kwargs)
    ax.add_patch(p)

    return artist


def plot_line(obj=None, step=False, emptybins=True, ax=None, **kwargs):
    """ Produce an errorbar plots with or without connecting lines.

    Args:
        obj: Mplobj representation of a root object.
        ax: Axis to plot on. If not specified current global axis will be used.
        x_err: If True, x errorbars will be plotted.
        yerr: If True, y errorbars will be plotted.
        emptybins: Not Implemented. Supposed to ignore/plot empty bins.
    """
    # Convert root object to mpl readable object
    obj = R2npObject1D(obj)

    if not kwargs['linestyle']:
        kwargs['linestyle'] = '-'

    # if no axis passed use current global axis
    if ax is None:
        ax = plt.gca()

    x = obj.x
    y = obj.y

    if step:
        x = steppify_bin(obj.xbinedges, isx=True)
        y = steppify_bin(y)

    line_kwargs = {k: v for k, v in kwargs.items() if
                   k in ['alpha', 'color', 'linestyle', 'step', 'label', 'zorder', 'linewidth', 'linestyle']}
    artist = ax.plot(x, y, **line_kwargs)

    return artist


def plot_errorbar(obj=None, step=False, x_err=True, y_err=True, emptybins=True, ax=None, **kwargs):
    """ Produce an errorbar plots with or without connecting lines.

    Args:
        obj: Mplobj representation of a root objogram.
        ax: Axis to plot on. If not specified current global axis will be used.
        x_err: If True, x errorbars will be plotted.
        yerr: If True, y errorbars will be plotted.
        emptybins: Not Implemented. Supposed to ignore/plot empty bins.
    """
    # Convert root object to mpl readable object
    obj = R2npObject1D(obj)

    # if no axis passed use current global axis
    if ax is None:
        ax = plt.gca()

    x = obj.x
    y = obj.y

    if x_err:
        x_err = np.array((obj.xerrl, obj.xerru))
    else:
        x_err = None
    if y_err:
        y_err = np.array((obj.yerrl, obj.yerru))
    else:
        y_err = None

    # linestyle = kwargs.pop('linestyle', '')
    # color = kwargs.pop('color', next(ax._get_lines.color_cycle))
    # capsize = kwargs.pop('capsize', 0)
    # Due to a bug in matplotlib v1.1 errorbar does not always respect linestyle when fmt is passed.
    # Workaround by plotting line and errorbars separately.
    # http://stackoverflow.com/a/18499120/3243729

    errorbar_kwargs = {k: v for k, v in kwargs.items() if
                       k in ['label', 'marker', 'capsize', 'marker', 'fmt', 'alpha', 'color', 'zorder']}
    errorbar_kwargs['fmt'] = ''
    errorbar_kwargs['linestyle'] = ''
    artist = ax.errorbar(x, y, xerr=x_err, yerr=y_err, **errorbar_kwargs)

    if kwargs['linestyle']:
        if step:
            x = steppify_bin(obj.xbinedges, isx=True)
            y = steppify_bin(y)
        plot_kwargs = {k: v for k, v in kwargs.items() if
                       k in ['label', 'alpha', 'color', 'linestyle', 'step', 'zorder']}
        ax.plot(x, y, **plot_kwargs)
    return artist


def plot_heatmap(obj, ax=None, z_log=False, z_lims=(None, None), cmap='viridis', **kwargs):
    """One dimensional heatmap plot.
    Args:
        obj: 1D Root object to be plotted
        ax: Axis to plot on. If not specified current global axis will be used.
        z_log: If True, z axis will be logarithmic.
        z_lims: (Lower, Upper) limits of z axis
        cmap: Colormap
    """
    # Convert root object to mpl readable object
    obj = R2npObject2D(obj)
    cmap = matplotlib.cm.get_cmap(cmap)

    # if no axis passed use current global axis
    if ax is None:
        ax = plt.gca()

    # Set z axis limits
    vmin, vmax = z_lims
    if (vmin, vmax) == (None,) * 2:
        if z_log:
            vmin, vmax = np.min(obj.z[np.nonzero(obj.z)]), np.amax(obj.z)
        else:
            vmin, vmax = np.amin(obj.z), np.amax(obj.z)
    norm = (LogNorm if z_log else Normalize)(vmin=vmin, vmax=vmax)

    artist = ax.pcolormesh(obj.xbinedges, obj.ybinedges, obj.z, cmap=cmap, norm=norm)
    return artist
