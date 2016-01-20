
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
        config['ana_modules'] = ['Ratio', 'DataLims']

        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)})]
        config['ratio_copy'] = [('ct14nlo_xs_ptavg','ct14nlo_xs_ptmaxexpys'),
                                ('ct14nlo_xs_ptavgexpys','ct14nlo_xs_ptmaxexpys'),
                                ('ct14nlo_xs_ptmaxexpys','ct14nlo_xs_ptmaxexpys')]
        config['objects']['ratio_ct14nlo_xs_ptavg_to_ct14nlo_xs_ptmaxexpys'] = {
                'axis' : 'ax1',
                'color' : '_color0_',
                'style' : 'line',
                'step' : 'True',
                }
        config['objects']['ratio_ct14nlo_xs_ptavgexpys_to_ct14nlo_xs_ptmaxexpys'] = {
                'axis' : 'ax1',
                'color' : '_color2_',
                'style' : 'line',
                'step' : 'True',
                }
        config['objects']['ratio_ct14nlo_xs_ptmaxexpys_to_ct14nlo_xs_ptmaxexpys'] = {
                'axis' : 'ax1',
                'color' : '_color1_',
                'style' : 'line',
                'step' : 'True',
                }

        config['objects']['ct14nlo_xs_ptavg'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_DEF_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                'color' : '_color0_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,avg}}$',
                }
        config['objects']['ct14nlo_xs_ptmaxexpys'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                'color' : '_color1_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,max}}\cdot e^{(0.3y^*)}$',
                }
        config['objects']['ct14nlo_xs_ptavgexpys'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVGEXPYS_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                'color' : '_color2_',
                'style' : 'line',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,avg}}\cdot e^{(0.3y^*)}$',
                }


        config["y_subplot_lims"] = [0.86, 1.14]
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
                              's=Ratio to $\mu=p_{\mathrm{T,max}}\cdot e^{(0.3y^*)}$?_bottomleft_?axis=ax1'] 

        config["output_path"] = 'nlo_xs_comp_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

