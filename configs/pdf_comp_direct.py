import util.callbacks as callbacks

def get_base_config():
    config = {}
    config['objects'] = {}
    config['store_json'] = False
    return config

def get_q2label(q2):
    q2_str = r'{:.2G}'.format(q2)
    if "E" in q2_str:
        base, exponent = q2_str.split('E')
        if base == '1':
            return r"10^{{{1}}}".format(base, int(exponent))
        else:
            return r"{0}\times 10^{{{1}}}".format(base, int(exponent))
    else:
        return q2_str

ymax_lim = { 
        0 : { 1.9 : 4.0},
        7 : { 1.9 : 0.6, 10000 : 0.6},
        8 : { 1.9 : 1.0, 10000 : 1.0},
        }


def get_config():
    configs = []
    partons = [0, 7, 8, 9]
    names = ['gluon', 'd valence quark', 'u valence quark', 'sea quarks']
    y_labels = ['$xg(x,Q^2\!)$', '$xd_{\mathrm{v}}(x,Q^2\!)$', '$xu_{\mathrm{v}}(x,Q^2\!)$', '$x\Sigma(x,Q^2\!)$',]
    q2s = [1.9, 10000]
    pdfset1 = "HFTD_HERA_V101_EIG"
    pdfset2 = "HFTD_HERACMSTDJETS_V101_EIG"

    pdf_label1 = "HERA DIS"
    pdf_label2 = "HERA DIS + CMS jets"


   
    for k, q2 in enumerate(q2s):
        for i, parton in enumerate(partons):
            config = get_base_config()
            config['ana_modules'] = ["PDFModule", 'Ratio', 'Copy']
            config['copy_id'] = []
            config['combine_legend_entries'] = []

            config['copy_id'].append(("_{0}_totunc".format(pdfset1),"_{0}_totunc_line".format(pdfset1)))
            config['copy_id'].append(("_{0}_totunc".format(pdfset2),"_{0}_totunc_line".format(pdfset2)))

            config["plot_id"] =  [
                                    '_{0}_totunc'.format(pdfset1),'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset1),
                                    '_{0}_totunc_line'.format(pdfset1),
                                    '_{0}_totunc'.format(pdfset2),'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset2),
                                    '_{0}_totunc_line'.format(pdfset2),
                                 ] 
            config['plot_order'] = ['_{0}_totunc'.format(pdfset1), '_{0}_totunc'.format(pdfset2)]
            config["combine_legend_entries"].append(("_{0}_totunc_line".format(pdfset1), "_{0}_totunc".format(pdfset1)))
            config["combine_legend_entries"].append(("_{0}_totunc_line".format(pdfset2), "_{0}_totunc".format(pdfset2)))

            config["input_pdfsets"] = [
                    ("{0}".format(pdfset1), {
                            "flavour": partons[i], 
                            "q2": q2s[k], 
                            "pdfset": pdfset1
                            }
                    ),
                    ("{0}".format(pdfset2), {
                            "flavour": partons[i], 
                            "q2": q2s[k], 
                            "pdfset": pdfset2
                            }
                    ),

            ]
            config['ratio_copy'] = [
                                    ('_{0}_totunc'.format(pdfset1), '_{0}_totunc'.format(pdfset1)),
                                    ('_{0}_totunc'.format(pdfset2), '_{0}_totunc'.format(pdfset2)),
                                    ]

            config["objects"]["_{0}_totunc".format(pdfset1)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "_color0_",
                "linestyle": "",
                "label": "{0}".format(pdf_label1),
                "step": False,
                "cmap": "viridis",
                "zorder": 1.0,
                "obj": "null",
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }
            config["objects"]["_{0}_totunc_line".format(pdfset1)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "black",
                "linewidth": 1.0,
                "linestyle": "--",
                "label": "{0}".format(pdf_label1),
                "step": False,
                "cmap": "viridis",
                "zorder": 1.0,
                "obj": "null",
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }

            config["objects"]["ratio__{0}_totunc_to__{0}_totunc".format(pdfset1)] = {
                "edgealpha": 1.0, 
                "edgecolor": "auto", 
                "style": "band", 
                "rasterized": True, 
                "capsize": 0, 
                "x_err": True, 
                "color": "_color0_", 
                "linestyle": "", 
                "step": False, 
                "cmap": "viridis", 
                "zorder": 1.0, 
                "obj": "null", 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax1"
            }

            config["objects"]["_{0}_totunc".format(pdfset2)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "edgecolor": "_color2_", 
                "linestyle": "",
                "linewidth": "2.0",
                "label": "{0}".format(pdf_label2),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": 'sllll', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": False, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }
            config["objects"]["_{0}_totunc_line".format(pdfset2)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": True,
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "color": "_color2_", 
                "linestyle": "--",
                "linewidth": "1.0",
                "label": "{0}".format(pdf_label2),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": 'sllll', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": False, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }

            config["objects"]["ratio__{0}_totunc_to__{0}_totunc".format(pdfset2)] = {
                "edgealpha": 1.0, 
                "style": "band", 
                "rasterized": True, 
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "edgecolor": "_color2_", 
                "linestyle": "", 
                "step": False, 
                "cmap": "viridis", 
                "zorder": 2.0, 
                "obj": "null", 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "hatch": 'sllll', 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax1"
            }


            if parton in ymax_lim and q2 in ymax_lim[parton]:
                ymaxval = ymax_lim[parton][q2]
            else:
                ymaxval = 'none'

            config["y_lims"] = ["0.0", ymaxval]
            config["y_subplot_lims"] = ["0.5", "1.5"]
            config["y_subplot_label"] = 'Rel. Uncert.'
            config["x_lims"] = [1E-4, 0.9]
            config['x_axis_formatter'] = 'scientific'
            config["x_log"] =  True
            config["add_subplot"] =  True
            config["legend_loc"] = 'best'
            config["x_label"] = "$x$"
            config["y_label"] = y_labels[i]
            config["ax_texts"] = [
                                  # 's={0}?_topleft_'.format(pdf_labels[j]),
                                  's=$Q^2\!={0}\mathrm{{GeV}}^2$?_topright_'.format(get_q2label(q2)),
                                  ] 
            config["output_path"] = 'pdfcomp_direct_{0}_{1}.png'.format(partons[i], q2)
            configs.append(config)

    return configs

# @callbacks.register('before_plot')
# def final_plot(**kwargs):
#     kwargs['mpl'].rcParams['legend.fontsize'] = 20
#     # kwargs['mpl'].rcParams['font.size'] = 20
