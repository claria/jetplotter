
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
        config['ana_modules'] = ['DataLims', 
                                 'Normalize', 
                                 'Multiply', 'Ratio']

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)})]
        config['ratio_copy'] = [
                                ('ct14nlo_xs','ct14nlo_xs'),
                                ('mmht2014_xs','ct14nlo_xs'),
                                ('nnpdf30_xs','ct14nlo_xs'),
                                ('hw7','ct14nlo_xs'),
                                ('dataunf','ct14nlo_xs'),
                                ]

        config["multiply"] =  [
                                ("ct14nlo_xs", "_np"), 
                                ("mmht2014nlo_xs", "_np"), 
                                ("nnpdf30nlo_xs", "_np"), 
                                ]
        config['normalize'] = [('dataunf', 'width')]

        config['objects']['ratio_ct14nlo_xs_to_ct14nlo_xs'] = {
                'axis' : 'ax',
                'color' : '_color1_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'CT14 (NLO)',
                }
        config['objects']['ratio_mmht2014nlo_xs_to_ct14nlo_xs'] = {
                'axis' : 'ax',
                'color' : '_color2_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'MMHT2014 (NLO)',
                }
        config['objects']['ratio_nnpdf30nlo_xs_to_ct14nlo_xs'] = {
                'axis' : 'ax',
                'color' : '_color3_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'NNPDF30 (NLO)',
                }

        config['objects']['ratio_hw7_to_ct14nlo_xs'] = {
                'axis' : 'ax',
                'color' : '_color0_',
                'style' : 'errorbar',
                'step' : 'True',
                "style": "errorbar", 
                "x_err": True, 
                "y_err": True, 

                }
        config['objects']['ratio_dataunf_to_ct14nlo_xs'] = {
                'axis' : 'ax',
                "alpha": 1.0, 
                "capsize": 0, 
                "cmap": "viridis", 
                "color": "black", 
                "edgecolor": "black", 
                "id": "dataunf", 
                "label": "Data (Unf.)", 
                "linestyle": "", 
                "marker": ".", 
                "step": False, 
                "style": "errorbar", 
                "x_err": True, 
                "y_err": True, 
                "zorder": 1.0
                }


        config['objects']['ct14nlo_xs'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                'color' : '_color1_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'CT14 (NLO)',
                }
        config['objects']['mmht2014nlo_xs'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/MMHT2014_xs'.format(rap_bin),
                'color' : '_color2_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'MMHT2014 (NLO)',
                }
        config['objects']['nnpdf30nlo_xs'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_YBYS_NLO.root?{0}/NNPDF30_xs'.format(rap_bin),
                'color' : '_color3_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'NNPDF30 (NLO)',
                }

        config['objects']['hw7'] = {
                'input' : '/nfs/dust/cms/user/gsieber/HW7/HW7_NLO+PS_2.root?{0}_xs'.format(rap_bin),
                'color' : '_color0_',
                'style' : 'line',
                'yerr' : True,
                'step' : 'True',
                'label' : 'HW7 - NLO+PS',
                }
        config['objects']['_np'] = {
            "input": "~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor".format(rap_bin)
        } 
        config['objects']["dataunf"] = {
            "alpha": 1.0, 
            "axis": "ax", 
            "capsize": 0, 
            "cmap": "viridis", 
            "color": "black", 
            "edgecolor": "black", 
            "id": "dataunf", 
            "input": "~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg".format(rap_bin), 
            "label": "Data (Unf.)", 
            "linestyle": "", 
            "marker": ".", 
            "step": False, 
            "style": "errorbar", 
            "x_err": True, 
            "y_err": True, 
            "zorder": 1.0
        }

        config["y_subplot_lims"] = [0.5, 1.5]
        config["y_lims"] = [1E-5, 1E5]
        config['y_log'] = True
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config["x_log"] =  True
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Cross Section (pb/GeV)"
        config["y_subplot_label"] = "Ratio"
        config["add_subplot"] = True
        config["plot_id"] = ["ratio*"]
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--', 'axis' : 'ax'}
                ]
        config["ax_texts"] = ["_{0}_?_upperleft_".format(rap_bin), 
                              '_8tev_',
                              's=Ratio to $\mu=p_{\mathrm{T,avg}}\cdot e^{(0.3y^*)}$?_bottomleft_?axis=ax'] 

        config["output_path"] = 'nlo_comp_general_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

