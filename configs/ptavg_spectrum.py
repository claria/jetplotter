import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    colors = ['_color0_','_color1_','_color2_','_color3_','_color4_','_color5_']
    configs = []

    config = get_base_config()

    config['ana_modules'] = ["Normalize", "ReBinning", 'Multiply']
    config["normalize"] = [(rap_bin, 'width') for rap_bin in rap_bins]
    config["multiply"] = [('{0}nlo'.format(rap_bin), '{0}_np'.format(rap_bin)) for rap_bin in rap_bins]

    config["data_lims"] = ([(rap_bin, 
                           {'min': '_{0}_xmin_'.format(rap_bin), 'max':'_{0}_xmax_'.format(rap_bin)}) for rap_bin in rap_bins] +
                           [('{0}nlo'.format(rap_bin), 
                           {'min': '_{0}_xmin_'.format(rap_bin), 'max':'_{0}_xmax_'.format(rap_bin)}) for rap_bin in rap_bins]
                           )

    config["combine_legend_entries"] = [(rap_bin, '{0}nlo'.format(rap_bin)) for rap_bin in rap_bins]

    config['plot_order'] = rap_bins

    markers = ['x', '4', '.', '+', '*', '1']
    for i, rap_bin in enumerate(rap_bins):
        config['objects']["{0}_np".format(rap_bin)] = {
            "input": "~/dust/dijetana/plot/np_factors.root?{0}/res_np_factor".format(rap_bin)
        } 
        config['objects']["{0}".format(rap_bin)] = {
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg".format(rap_bin),
            "color": "black", 
            "label": "_{0}_".format(rap_bin), 
            "linestyle": "", 
            "marker": markers[i], 
            "markersize": 10,
            "markeredgewidth": 2,
            "x_err": False, 
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
    config["y_lims"] = [1E-5, 1E6]
    config["x_log"] = True
    config["x_axis_formatter"] = 'scalar2'
    config["x_lims"] = [120, 2000.]
    config["legend_loc"] = 'upper right'
    config["x_label"] = "_ptavg_"
    config["y_label"] = "$\\frac{d^3\\sigma}{dp_{\\mathrm{T,avg}} dy_b dy*}$ / $\mathrm{pb}\,\mathrm{GeV}^{-1}$"

    config["ax_texts"] = [
                          "_20fb_", 
                          {'s': ur'anti\u2013$k_\mathrm{T}\,R=0.7$' , 'x': 0.62, 'y': 0.60, 'ha': 'left', 'va': 'top'}, 
                          {'s': ur'NNPDF 3.0\u2013NLO$\otimes$NP' , 'x': 0.62, 'y': 0.55, 'ha': 'left', 'va': 'top'}, 
                          "s=$\mu=p_\\mathrm{T,max}e^{{0.3y^{*}}}$?x=0.62|y=0.50|ha=left|va=top"
                          ]

    config["output_path"] = 'ptavg_spectrum.png'.format(rap_bin)
    configs.append(config)
    return configs


@callbacks.register('after_plot')
def final_plot(**kwargs):
    print 'hallo'

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    kwargs['mpl'].rcParams['font.size'] = 20
