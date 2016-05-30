import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_config():
    rap_bins = ['yb0ys0','yb0ys1','yb0ys2','yb1ys0','yb1ys1','yb2ys0']
    configs = []
    for rap_bin in rap_bins:
        config = get_base_config()
        config['ana_modules'] = [
                                'Add', 
                                'Ratio', 
                                'Stack'
                                ]

        config['ratio'] = [
                    ("sub0", "_sum"), 
                    ("sub1", "_sum"), 
                    ("sub2", "_sum"), 
                    ("sub3", "_sum"), 
                    ("sub4", "_sum"), 
                    ("sub5", "_sum"), 
                    ("sub6", "_sum"), 
                    ]
        config['add'] = [
                    ("_sum", "sub0,sub1,sub2,sub3,sub4,sub5,sub6"), 
                    ]
        config['stack'] = ['sub0', 'sub5', 'sub6', 'sub2','sub1', 'sub3', 'sub4']
        config['plot_order'] = ['sub0', 'sub5', 'sub6', 'sub1', 'sub2', 'sub3', 'sub4']

        config['objects']['sub0'] = {
            "input": "~/nsubstest.root?{0}_sub0/NNPDF30_xs".format(rap_bin), 
            "label": u"\u2460 gg$\\rightarrow$jets", 
            "color": "_colorpair0b_",
            "style": "histo", 
            "y_err": False, 
            }
        config['objects']['sub1'] = {
            "input": "~/nsubstest.root?{0}_sub1/NNPDF30_xs".format(rap_bin), 
            "label": u"\u2463 $\\mathrm{q}_\\mathrm{i}\\mathrm{q}_\mathrm{j} \\rightarrow\\mathrm{jets}$", 
            "style": "histo", 
            "color": "_colorpair4b_",
            "y_err": False, 
            }
        config['objects']['sub2'] = {
            "input": "~/nsubstest.root?{0}_sub2/NNPDF30_xs".format(rap_bin), 
            "label": u"\u2464 $\\mathrm{q}_\\mathrm{i}\\mathrm{q}_\mathrm{i} \\rightarrow\\mathrm{jets}$", 
            "style": "histo", 
            "color": "_colorpair4a_",
            "y_err": False,
            }
        config['objects']['sub3'] = {
            "input": "~/nsubstest.root?{0}_sub3/NNPDF30_xs".format(rap_bin), 
            "label": u"\u2465 $\\mathrm{q}_\\mathrm{i}\\overline{\\mathrm{q}}_\mathrm{i} \\rightarrow\\mathrm{jets}$", 
            "color": "_colorpair2a_",
            "style": "histo", 
            "y_err": False, 
            }
        config['objects']['sub4'] = {
            "input": "~/nsubstest.root?{0}_sub4/NNPDF30_xs".format(rap_bin), 
            "label": u"\u2466 $\\mathrm{q}_\\mathrm{i}\\overline{\\mathrm{q}}_\mathrm{j} \\rightarrow\\mathrm{jets}$", 
            "color": "_colorpair2b_",
            "style": "histo", 
            "y_err": False, 
            }
        config['objects']['sub5'] = {
            "input": "~/nsubstest.root?{0}_sub5/NNPDF30_xs".format(rap_bin), 
            "label": u"\u2461 gq$\\rightarrow$jets ($x_g < x_q$)", 
            "color": "_colorpair1a_",
            "style": "histo", 
            "y_err": False, 
            }
        config['objects']['sub6'] = {
            "input": "~/nsubstest.root?{0}_sub6/NNPDF30_xs".format(rap_bin), 
            "label": u"\u2462 gq$\\rightarrow$jets ($x_g > x_q$)", 
            "color": "_colorpair1b_",
            "style": "histo", 
            "y_err": False, 
            }


        config["y_lims"] = ["0.0", "1.0"]
        config['legend_loc'] = 'lower left outside'
        config['legend_bbox_anchor'] = (-0.021,1.0)
        config['legend_ncol'] = 3
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Subprocess fraction"
        config["ax_texts"] = ["_{0}_?_bottomleft_".format(rap_bin)] 

        config["output_path"] = 'subprocesses_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    # kwargs['mpl'].rcParams['font.size'] = 20
