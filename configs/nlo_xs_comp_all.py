
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
        config['ratio_copy'] = [('ct14nlo_xs_ptavg','ct14nlo_xs_ptavgexpys'),
                                ('ct14nlo_xs_ptavgexpys','ct14nlo_xs_ptavgexpys'),
                                ('hw7','ct14nlo_xs_ptavgexpys'),
                                ('dataunf','ct14nlo_xs_ptavgexpys'),
                                # ('ct14nlo_xs_ptmaxexpys','ct14nlo_xs_ptmaxexpys')
                                ]

        config["multiply"] =  [
                                ("ct14nlo_xs_ptavg", "_np"), 
                                ("ct14nlo_xs_ptavgexpys", "_np"), 
                                # ("ct14nlo_xs_ptmaxexpys", "_np"), 
                                ]
        config['normalize'] = [('dataunf', 'width')]

        config['objects']['ratio_ct14nlo_xs_ptavg_to_ct14nlo_xs_ptavgexpys'] = {
                'axis' : 'ax1',
                'color' : '_color0_',
                'style' : 'line',
                'step' : 'True',
                }
        config['objects']['ratio_ct14nlo_xs_ptavgexpys_to_ct14nlo_xs_ptavgexpys'] = {
                'axis' : 'ax1',
                'color' : '_color2_',
                'style' : 'line',
                'step' : 'True',
                }
        # config['objects']['ratio_ct14nlo_xs_ptmaxexpys_to_ct14nlo_xs_ptavgexpys'] = {
        #         'axis' : 'ax1',
        #         'color' : '_color1_',
        #         'style' : 'line',
        #         'step' : 'True',
        #         }
        config['objects']['ratio_hw7_to_ct14nlo_xs_ptavgexpys'] = {
                'axis' : 'ax1',
                'color' : '_color1_',
                'style' : 'errorbar',
                'step' : 'True',
                "style": "errorbar", 
                "x_err": True, 
                "y_err": True, 

                }
        config['objects']['ratio_dataunf_to_ct14nlo_xs_ptavgexpys'] = {
                'axis' : 'ax1',
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


        config['objects']['ct14nlo_xs_ptavg'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_DEF_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                'color' : '_color0_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'CT14 (NLOxNP) - $\mu=p_{\mathrm{T,avg}}$',
                }
        # config['objects']['ct14nlo_xs_ptmaxexpys'] = {
        #         'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
        #         'color' : '_color1_',
        #         'style' : 'line',
        #         'step' : 'True',
        #         'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,max}}\cdot e^{(0.3y^*)}$',
        #         }
        config['objects']['ct14nlo_xs_ptavgexpys'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVGEXPYS_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                'color' : '_color2_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'CT14 (NLOxNP) - $\mu=p_{\mathrm{T,avg}}\cdot e^{(0.3y^*)}$',
                }
        config['objects']['hw7'] = {
                'input' : '/nfs/dust/cms/user/gsieber/HW7/HW7_NLO+PS_2.root?{0}_xs'.format(rap_bin),
                'color' : '_color1_',
                'style' : 'line',
                'yerr' : True,
                'step' : 'True',
                'label' : 'HW7 (NLO+PS matched) - $\mu=p_{\mathrm{T,max}}$',
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
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--', 'axis' : 'ax1'}
                ]
        config["ax_texts"] = ["_{0}_?_upperleft_".format(rap_bin), 
                              '_8tev_',
                              's=Ratio to $\mu=p_{\mathrm{T,avg}}\cdot e^{(0.3y^*)}$?_bottomleft_?axis=ax1'] 

        config["output_path"] = 'nlo_xs_comp_all_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

