import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_label(rap_bin):
    nice_labels = { 
        'yb0ys0': '_yb0ys0_ ($\\times 10^2$)',
        'yb0ys1': '_yb0ys1_ ($\\times 10^2$)',
        'yb0ys2': '_yb0ys2_ ($\\times 10^1$)',
        'yb1ys0': '_yb1ys0_ ($\\times 10^1$)',
        'yb1ys1': '_yb1ys1_ ($\\times 10^1$)',
        'yb2ys0': '_yb2ys0_ ($\\times 10^0$)',
        }
    return nice_labels[rap_bin]

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    colors = ['_color0_','_color1_','_color2_','_color3_','_color4_','_color5_']
    configs = []

    config = get_base_config()

    config['ana_modules'] = ["Normalize", "ReBinning", 'Multiply']
    config["normalize"] = [(rap_bin, 'width') for rap_bin in rap_bins]
    config["multiply"] = ([('{0}nlo'.format(rap_bin), '{0}_np'.format(rap_bin)) for rap_bin in rap_bins] +
                         [('{0}nlo'.format(rap_bin), '{0}_ewk'.format(rap_bin)) for rap_bin in rap_bins] +
                         [('yb0ys0nlo', 100), ('yb0ys1nlo', 100),('yb0ys2nlo', 10),('yb1ys0nlo', 10),('yb1ys1nlo', 10), ('yb2ys0nlo', 1)] + 
                         [('yb0ys0', 100), ('yb0ys1', 100),('yb0ys2', 10),('yb1ys0', 10),('yb1ys1', 10), ('yb2ys0', 1)]
                         )
    print config['multiply']

    config["data_lims"] = ([(rap_bin, 
                           {'min': '_{0}_xmin_'.format(rap_bin), 'max':'_{0}_xmax_'.format(rap_bin)}) for rap_bin in rap_bins] +
                           [('{0}nlo'.format(rap_bin), 
                           {'min': '_{0}_xmin_'.format(rap_bin), 'max':'_{0}_xmax_'.format(rap_bin)}) for rap_bin in rap_bins]
                           )

    config["combine_legend_entries"] = [(rap_bin, '{0}nlo'.format(rap_bin)) for rap_bin in rap_bins]

    config['plot_order'] = rap_bins

    markers = ['D', 'v', '^', 's', '>', 'o']
    for i, rap_bin in enumerate(rap_bins):
        config['objects']["{0}_np".format(rap_bin)] = {
            "input": "~/dust/dijetana/plot/np_factors.root?{0}/res_np_factor".format(rap_bin)
        } 
        config['objects']["{0}_ewk".format(rap_bin)] = {
            "input": "~/dust/dijetana/ewk/ewk_dijet.root?{0}/ewk_corr".format(rap_bin)
        } 
        config['objects']["{0}".format(rap_bin)] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg".format(rap_bin),
            "color": "none", 
            "label": get_label(rap_bin), 
            "linestyle": "", 
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
        config['objects']["{0}nlo".format(rap_bin)] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_xs".format(rap_bin),
            "step": True, 
            "style": "line",
            'color': colors[i]
        } 

    config['plot_id'] = ['^{0}nlo$'.format(rap_bin) for rap_bin in rap_bins] + ['^{0}$'.format(rap_bin) for rap_bin in rap_bins]
    config['fig_size'] = [10., 10.]
    config['y_log'] = True
    config["y_lims"] = [1E-4, 1E8]
    config["x_log"] = True
    config["x_axis_formatter"] = 'scalar2'
    config["x_lims"] = [120, 2000.]
    config["legend_loc"] = 'upper right'
    config["x_label"] = "_ptavg_"
    config["y_label"] = "$\\frac{d^3\\sigma}{dp_{\\mathrm{T,avg}} dy_b dy*}$ / $\mathrm{pb}\,\mathrm{GeV}^{-1}$"

    config["ax_texts"] = [
                          "_20fb_", 
                          {'s': ur'NLOJET++ (NLO$\otimes$EW$\otimes$NP)' , 'x': 0.54, 'y': 0.68, 'ha': 'left', 'va': 'top'}, 
                          {'s': ur'NNPDF 3.0' , 'x': 0.54, 'y': 0.64, 'ha': 'left', 'va': 'top'}, 
                          {'s': ur'$\mu=p_\mathrm{T,max}e^{{0.3y^{*}}}$', 'x':'0.54','y':'0.60','ha':'left','va':'top'},
                          {'s': ur'anti\u2013$k_\mathrm{t}\,R=0.7$' , 'x': 0.54, 'y': 0.56, 'ha': 'left', 'va': 'top'}, 
                          {'s': ur'CMS' , 'x': 0.05, 'y': 0.95, 'ha': 'left', 'va': 'top', 'size': 40, 'weight': 'bold'}, 
                          {'s': ur'Preliminary' , 'x': 0.055, 'y': 0.875, 'ha': 'left', 'va': 'top', 'size': 18, 'style':'italic'}, 
                          ]

    config["output_path"] = 'ptavg_spectrum_scaled.png'.format(rap_bin)
    configs.append(config)
    return configs


@callbacks.register('after_plot')
def final_plot(**kwargs):
    print 'hallo'

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 18
    kwargs['mpl'].rcParams['font.size'] = 18
