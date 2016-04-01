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
        config['ana_modules'] = ['BuildTGraph', 'Ratio', 'DataLims']

        config['build_tgraph'] = [
                                ('ct14nlo_ptavg_scaleunc', ('ct14nlo_xs_ptavg', 'ct14nlo_scunc_l_ptavg', 'ct14nlo_scunc_u_ptavg')),
                                ('ct14nlo_ptmaxexpystar_scaleunc', ('ct14nlo_xs_ptmaxexpystar', 'ct14nlo_scunc_l_ptmaxexpystar', 'ct14nlo_scunc_u_ptmaxexpystar')),
                                ('ct14nlo_ptavgexpystar_scaleunc', ('ct14nlo_xs_ptavgexpystar', 'ct14nlo_scunc_l_ptavgexpystar', 'ct14nlo_scunc_u_ptavgexpystar')),
                                ]

        config['plot_id']= ['ct14nlo_ptavg_scaleunc', 'ct14nlo_ptavgexpystar_scaleunc','ct14nlo_ptmaxexpystar_scaleunc']

        config['ratio'] = [
                           ('ct14nlo_ptmaxexpystar_scaleunc', 'ct14nlo_ptmaxexpystar_scaleunc'),
                           ('ct14nlo_ptavgexpystar_scaleunc', 'ct14nlo_ptavgexpystar_scaleunc'),
                           ('ct14nlo_ptavg_scaleunc', 'ct14nlo_ptavg_scaleunc'),
                          ]
        config['objects']['ct14nlo_xs_ptavg'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_DEF_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                }
        config['objects']['ct14nlo_xs_ptmaxexpystar'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                }
        config['objects']['ct14nlo_xs_ptavgexpystar'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVGEXPYS_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                }

        config['objects']['ct14nlo_scunc_l_ptavg'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_DEF_YBYS_NLO.root?{0}/CT14nlo_scunc_l'.format(rap_bin),
                }
        config['objects']['ct14nlo_scunc_l_ptmaxexpystar'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_scunc_l'.format(rap_bin),
                }
        config['objects']['ct14nlo_scunc_l_ptavgexpystar'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVGEXPYS_YBYS_NLO.root?{0}/CT14nlo_scunc_l'.format(rap_bin),
                }
        config['objects']['ct14nlo_scunc_u_ptavg'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVG_DEF_YBYS_NLO.root?{0}/CT14nlo_scunc_u'.format(rap_bin),
                }
        config['objects']['ct14nlo_scunc_u_ptmaxexpystar'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_scunc_u'.format(rap_bin),
                }
        config['objects']['ct14nlo_scunc_u_ptavgexpystar'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTAVGEXPYS_YBYS_NLO.root?{0}/CT14nlo_scunc_u'.format(rap_bin),
                }
        config['objects']['ct14nlo_ptavg_scaleunc'] = {
                'color' : '_color0_',
                'style' : 'errorlines',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,avg}}$',
                }
        config['objects']['ct14nlo_ptmaxexpystar_scaleunc'] = {
                'color' : '_color1_',
                'style' : 'errorlines',
                'dashes': [10,4],
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,max}}e^{(0.3y^{*})}$',
                }
        config['objects']['ct14nlo_ptavgexpystar_scaleunc'] = {
                'color' : '_color2_',
                'style' : 'errorlines',
                'step' : 'True',
                'label' : 'CT14 (NLO) - $\mu=p_{\mathrm{T,avg}}e^{(0.3y^{*})}$',
                }


        config["y_lims"] = ["0.6", "1.2"]
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config['margin'] = 0.05
        config["x_log"] =  True
        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Fractional Uncertainty?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = ["_{0}_?_upperleft_".format(rap_bin)] 

        config["output_path"] = 'scale_uncert_comp_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    # kwargs['mpl'].rcParams['font.size'] = 20
