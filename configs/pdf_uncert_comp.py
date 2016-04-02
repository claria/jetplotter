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
        config['ana_modules'] = ['BuildTGraph', 'Ratio', 'DataLims', 'MinusOne']

        config['build_tgraph'] = [
                                ('ct14nlo_pdfunc', ('ct14nlo_xs', 'ct14nlo_pdfunc_l', 'ct14nlo_pdfunc_u')),
                                ('mmht2014_pdfunc', ('mmht2014_xs', 'mmht2014_pdfunc_l', 'mmht2014_pdfunc_u')),
                                ('nnpdf30_pdfunc', ('nnpdf30_xs', 'nnpdf30_pdfunc_l', 'nnpdf30_pdfunc_u')),
                                ]
        config['plot_id'] = [
                             '^ct14nlo_pdfunc$', 
                             '^mmht2014_pdfunc$', 
                             '^nnpdf30_pdfunc$', 
                            ]
        config['minusone'] = ['ct14nlo_pdfunc', 'mmht2014_pdfunc', 'nnpdf30_pdfunc']

        config['ratio'] = [
                           ('ct14nlo_pdfunc', 'ct14nlo_pdfunc'),
                           ('mmht2014_pdfunc', 'mmht2014_pdfunc'),
                           ('nnpdf30_pdfunc', 'nnpdf30_pdfunc'),
                          ]

        config['objects']['ct14nlo_xs'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_xs'.format(rap_bin),
                }
        config['objects']['ct14nlo_pdfunc_l'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_pdfunc_l'.format(rap_bin),
                }
        config['objects']['ct14nlo_pdfunc_u'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/CT14nlo_pdfunc_u'.format(rap_bin),
                }
        config['objects']['mmht2014_xs'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/MMHT2014_xs'.format(rap_bin),
                }
        config['objects']['mmht2014_pdfunc_l'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/MMHT2014_pdfunc_l'.format(rap_bin),
                }
        config['objects']['mmht2014_pdfunc_u'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/MMHT2014_pdfunc_u'.format(rap_bin),
                }
        config['objects']['nnpdf30_xs'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/NNPDF30_xs'.format(rap_bin),
                }
        config['objects']['nnpdf30_pdfunc_l'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/NNPDF30_pdfunc_l'.format(rap_bin),
                }
        config['objects']['nnpdf30_pdfunc_u'] = {
                'input' : '/nfs/dust/cms/user/gsieber/dijetana/ana/CMSSW_7_2_3/PTMAXEXPYS_YBYS_NLO.root?{0}/NNPDF30_pdfunc_u'.format(rap_bin),
                }

        config['objects']['ct14nlo_pdfunc'] = {
                'color' : '_color0_',
                'style' : 'errorlines',
                'step' : 'True',
                'label' : 'CT14 (NLO)',
                }
        config['objects']['mmht2014_pdfunc'] = {
                'color' : '_color1_',
                'style' : 'errorlines',
                'dashes': [8,4],
                'step' : 'True',
                'label' : 'MMHT 2014 (NLO)',
                }
        config['objects']['nnpdf30_pdfunc'] = {
                'color' : '_color2_',
                'style' : 'errorlines',
                'dashes': [16,4],
                'step' : 'True',
                'label' : 'NNPDF 3.0 (NLO)',
                }


        config["y_lims"] = ["0.7", "1.3"]
        config['legend_loc'] = 'upper right'
        config["x_lims"] = ["_{0}_xmin_".format(rap_bin),"_{0}_xmax_".format(rap_bin)]
        config['margin'] = 0.05
        config["x_log"] =  True
        config["data_lims"] = [('all', { 'min' : '_{0}_xmin_'.format(rap_bin), 'max' : '_{0}_xmax_'.format(rap_bin)}),
                                ]
        config["x_label"] = "_ptavg_"
        config["y_label"] = "Relative uncertainty?_center_"
        config["ax_hlines"] = [
                {'y' : 1.0, 'color' : 'black', 'linewidth' : 1.0, 'linestyle' : '--'}
                ]
        config["ax_texts"] = ["_{0}_?_upperleft_".format(rap_bin)] 

        config["output_path"] = 'pdf_uncert_comp_{0}.png'.format(rap_bin)
        configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['legend.fontsize'] = 20
    # kwargs['mpl'].rcParams['font.size'] = 20
