import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_label(rap_bin):
    nice_labels = { 
        'yb0ys0': '_yb0ys0_',
        'yb0ys1': '_yb0ys1_',
        'yb0ys2': '_yb0ys2_',
        'yb1ys0': '_yb1ys0_',
        'yb1ys1': '_yb1ys1_',
        'yb2ys0': '_yb2ys0_',
        }
    return nice_labels[rap_bin]

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    colors = ['_color0_','_color1_','_color2_','_color3_','_color4_','_color5_']
    configs = []

    config = get_base_config()

    config['ana_modules'] = ["ReBinning"]
    config["normalize"] = [(rap_bin, 'width') for rap_bin in rap_bins]

    config["data_lims"] = [(rap_bin, {'min': '_{0}_xmin_'.format(rap_bin), 'max':'_{0}_xmax_'.format(rap_bin)}) for rap_bin in rap_bins]

    # config["combine_legend_entries"] = [(rap_bin, '{0}nlo'.format(rap_bin)) for rap_bin in rap_bins]

    config['plot_order'] = rap_bins

    markers = ['D', 'v', '^', 's', '>', 'o']
    for i, rap_bin in enumerate(rap_bins):
        # config['objects']["{0}_np".format(rap_bin)] = {
        #     "input": "~/dust/dijetana/plot/np_factors.root?{0}/res_np_factor".format(rap_bin)
        # } 
        config['objects']["{0}".format(rap_bin)] = {
            "input": "~/dust/dijetana/plot/np_factors.root?{0}/res_np_factor".format(rap_bin),
            "color": colors[i],
            "label": get_label(rap_bin), 
            "linestyle": "-", 
            "style" : "line",
            "step" : True,
            "marker": markers[i], 
            "markersize": 8,
            "ecolor" : "black",
            'elinewidth' : 1,
            "markeredgewidth": 2,
            'legend_errorbars': False,
            "x_err": True, 
            "y_err": True, 
            "zorder": 100.0
        } 

    # config['plot_id'] = ['^{0}nlo$'.format(rap_bin) for rap_bin in rap_bins] + ['^{0}$'.format(rap_bin) for rap_bin in rap_bins]
    config['fig_size'] = [10., 10.]
    config['y_log'] = False
    config["y_lims"] = [1.0, 1.15]
    config["x_log"] = True
    config["x_axis_formatter"] = 'scalar2'
    config["x_lims"] = [120, 2000.]
    config["legend_loc"] = 'upper right'
    config["x_label"] = "_ptavg_"
    config["y_label"] = "Relative non-perturbative correction"

    config["ax_texts"] = [
                          "_8tev_", 
                          {'s': ur'CMS' , 'x': 0.05, 'y': 0.95, 'ha': 'left', 'va': 'top', 'size': 40, 'weight': 'bold'}, 
                          {'s': ur'Preliminary' , 'x': 0.055, 'y': 0.875, 'ha': 'left', 'va': 'top', 'size': 18, 'style':'italic'}, 
                          ]

    config["output_path"] = 'np_overview.png'.format(rap_bin)
    configs.append(config)
    return configs


@callbacks.register('after_plot')
def final_plot(**kwargs):
    print 'hallo'

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 18
    kwargs['mpl'].rcParams['font.size'] = 18
