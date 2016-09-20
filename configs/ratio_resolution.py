import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    configs = []
    config = get_base_config()
    config['ana_modules'] = ['Ratio']

    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    config['ratio'] = []
    config['plot_id'] = []
    colors = {
            'yb0ys0': '_color0_',
            'yb0ys1': '_color1_',
            'yb0ys2': '_color2_',
            'yb1ys0': '_color3_',
            'yb1ys1': '_color4_',
            'yb2ys0': '_color5_',
            }

    for rap_bin in rap_bins:
        config["ratio"].append(["res_smeared2_{0}".format(rap_bin), "res_smeared_{0}".format(rap_bin)])
        config['plot_id'].append('res_smeared2_{0}'.format(rap_bin))

        config['objects']["res_smeared2_{0}".format(rap_bin)] = {
            "input": "~/dust/dijetana/plot/plots/resolution_ptavg_smeared2_crystalball.root?resolution_{0}_fit".format(rap_bin), 
            "label": "Resolution Smeared/Scaled _{0}_".format(rap_bin), 
            "step": True, 
            "style": "line", 
            'color': colors[rap_bin],
        }
        config['objects']["res_smeared_{0}".format(rap_bin)] = {
            "input": "~/dust/dijetana/plot/plots/resolution_ptavg_smeared_crystalball.root?resolution_{0}_fit".format(rap_bin), 
            "step": True, 
            "style": "line", 
        }

    config["y_lims"] = ["0.5", "1.5"]
    config["x_lims"] = [30., 2000.]
    config["x_log"] =  True
    config["legend_loc"] = 'upper right'
    config["x_label"] = "$p_\\mathrm{T,avg}$ (GeV)"
    config["y_label"] = "Ratio?_center_"
    config["ax_hlines"] = [
            {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
            ]
    config["ax_texts"] = [
                          # '_{0}_?_upperleft_'.format(rap_bin), 
                          '_20fb_'] 

    config["output_path"] = 'ratio_resolution.png'
    configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 14
    kwargs['mpl'].rcParams['lines.linewidth'] = 4
    # kwargs['mpl'].rcParams['font.size'] = 20
