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
        7 : { 1.9 : 0.6, 10000 : 0.6,100000 : 0.6, 1000000 : 0.6},
        8 : { 1.9 : 1.0, 10000 : 1.0, 100000 : 1.0, 1000000 : 1.0},
        }


def get_config():
    configs = []
    partons = [0, 7, 8, 9]
    names = ['gluon', 'd valence quark', 'u valence quark', 'sea quarks']
    y_labels = ['$xg(x,Q^2\!)$', '$xd_{\mathrm{v}}(x,Q^2\!)$', '$xu_{\mathrm{v}}(x,Q^2\!)$', '$x\Sigma(x,Q^2\!)$',]
    q2s = [1.9, 4.0, 10000, 100000, 1000000]
    pdfset1 = "NNPDF30_nlo_as_0118"
    pdfset3 = "INCJETS_8TEV_EIG"
    pdfset2 = "HFTD_HERACMSTDJETS_V111K_EIG"
    pdfset4 = "CT14nlo"

    pdf_label1 = "NNPDF30"
    pdf_label3 = "HERA + CMS INC JETS"
    pdf_label2 = "HERA + CMS Dijets"
    pdf_label4 = "CT14nlo"


   
    for k, q2 in enumerate(q2s):
        for i, parton in enumerate(partons):
            config = get_base_config()
            config['ana_modules'] = ["PDFModule", 'Ratio', 'Copy', 'MinusOne']
            config['copy_id'] = []
            config['combine_legend_entries'] = []

            config['copy_id'].append(("_{0}_totunc".format(pdfset1),"_{0}_totunc_line".format(pdfset1)))
            config['copy_id'].append(("_{0}_totunc".format(pdfset2),"_{0}_totunc_line".format(pdfset2)))
            config['copy_id'].append(("_{0}_totunc".format(pdfset3),"_{0}_totunc_line".format(pdfset3)))
            config['copy_id'].append(("_{0}_totunc".format(pdfset4),"_{0}_totunc_line".format(pdfset4)))
            config['minusone'] = ['ratio__{0}_totunc_to__{0}_totunc'.format(pdfset1), 
                                  'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset2),
                                  'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset3),
                                  'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset4)
                                  ]

            config["plot_id"] =  [
                                    '_{0}_totunc'.format(pdfset1),'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset1),
                                    '_{0}_totunc_line'.format(pdfset1),
                                    '_{0}_totunc'.format(pdfset2),'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset2),
                                    '_{0}_totunc_line'.format(pdfset2),
                                    '_{0}_totunc'.format(pdfset3),'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset3),
                                    '_{0}_totunc_line'.format(pdfset3),
                                    '_{0}_totunc'.format(pdfset4),'ratio__{0}_totunc_to__{0}_totunc'.format(pdfset4),
                                    '_{0}_totunc_line'.format(pdfset4),

                                 ] 
            config['plot_order'] = ['_{0}_totunc'.format(pdfset1), '_{0}_totunc'.format(pdfset2)]
            config["combine_legend_entries"].append(("_{0}_totunc_line".format(pdfset1), "_{0}_totunc".format(pdfset1)))
            config["combine_legend_entries"].append(("_{0}_totunc_line".format(pdfset2), "_{0}_totunc".format(pdfset2)))
            config["combine_legend_entries"].append(("_{0}_totunc_line".format(pdfset3), "_{0}_totunc".format(pdfset3)))
            config["combine_legend_entries"].append(("_{0}_totunc_line".format(pdfset4), "_{0}_totunc".format(pdfset4)))

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
                    ("{0}".format(pdfset3), {
                            "flavour": partons[i], 
                            "q2": q2s[k], 
                            "pdfset": pdfset3
                            }
                    ),
                    ("{0}".format(pdfset4), {
                            "flavour": partons[i], 
                            "q2": q2s[k], 
                            "pdfset": pdfset4
                            }
                    ),

            ]
            config['ratio_copy'] = [
                                    ('_{0}_totunc'.format(pdfset1), '_{0}_totunc'.format(pdfset1)),
                                    ('_{0}_totunc'.format(pdfset2), '_{0}_totunc'.format(pdfset2)),
                                    ('_{0}_totunc'.format(pdfset3), '_{0}_totunc'.format(pdfset3)),
                                    ('_{0}_totunc'.format(pdfset4), '_{0}_totunc'.format(pdfset4)),
                                    ]

            config["objects"]["_{0}_totunc".format(pdfset1)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "_color0_",
                "linestyle": "",
                "label": "{0}".format(pdf_label1),
                "step": False,
                "cmap": "viridis",
                "zorder": 1.0,
                "obj": "null",
                "marker": ".", 
                "alpha": 0.5, 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }
            config["objects"]["_{0}_totunc_line".format(pdfset1)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "_color0_",
                "linewidth": 1.0,
                "linestyle": "--",
                "label": "{0}".format(pdf_label1),
                "step": False,
                "cmap": "viridis",
                "zorder": 1.0,
                "obj": "null",
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
                "rasterized": False, 
                "capsize": 0, 
                "x_err": True, 
                "color": "_color0_", 
                "linestyle": "", 
                "step": False, 
                "cmap": "viridis", 
                "zorder": 1.0, 
                "obj": "null", 
                "marker": ".", 
                "alpha": 0.5, 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax1"
            }

            config["objects"]["_{0}_totunc".format(pdfset2)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "_darkcolor2_", 
                "edgecolor": "_darkcolor2_", 
                "linestyle": "",
                "linewidth": "2.0",
                "label": "{0}".format(pdf_label2),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": '//', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 0.2, 
                "fill": False, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }
            config["objects"]["_{0}_totunc_line".format(pdfset2)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "color": "_darkcolor2_", 
                "linestyle": "--",
                "linewidth": "1.0",
                "label": "{0}".format(pdf_label2),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": '//', 
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
                "rasterized": False, 
                "capsize": 0, 
                "x_err": True, 
                "edgecolor": "_darkcolor2_", 
                "color": "_darkcolor2_", 
                "linestyle": "", 
                "step": False, 
                "cmap": "viridis", 
                "zorder": 2.0, 
                "linewidth": "2.0",
                "obj": "null", 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 0.2, 
                "hatch": '//', 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax1"
            }

            config["objects"]["_{0}_totunc".format(pdfset3)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "_darkcolor3_", 
                "edgecolor": "_darkcolor3_", 
                "linestyle": "",
                "linewidth": "2.0",
                "label": "{0}".format(pdf_label3),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": '//', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 0.2, 
                "fill": False, 
                "y_err": True, 
                "axis": "ax"
            }
            config["objects"]["_{0}_totunc_line".format(pdfset3)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "color": "_darkcolor3_", 
                "linestyle": "--",
                "linewidth": "1.0",
                "label": "{0}".format(pdf_label3),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": '//', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": False, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }

            config["objects"]["ratio__{0}_totunc_to__{0}_totunc".format(pdfset3)] = {
                "edgealpha": 1.0, 
                "style": "band", 
                "rasterized": False, 
                "capsize": 0, 
                "x_err": True, 
                "edgecolor": "_darkcolor3_", 
                "color": "_darkcolor3_", 
                "linestyle": "", 
                "step": False, 
                "cmap": "viridis", 
                "zorder": 2.0, 
                "linewidth": "2.0",
                "obj": "null", 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 0.2, 
                "hatch": '//', 
                "fill": True, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax1"
            }

            config["objects"]["_{0}_totunc".format(pdfset4)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "band",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "_darkcolor4_", 
                "edgecolor": "_darkcolor4_", 
                "linestyle": "",
                "linewidth": "2.0",
                "label": "{0}".format(pdf_label4),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": '//', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 0.2, 
                "fill": False, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }
            config["objects"]["_{0}_totunc_line".format(pdfset4)] = {
                "edgealpha": 1.0,
                "edgecolor": "auto",
                "style": "line",
                "rasterized": False,
                "capsize": 0, 
                "x_err": True, 
                "color": "none", 
                "color": "_darkcolor4_", 
                "linestyle": "--",
                "linewidth": "1.0",
                "label": "{0}".format(pdf_label4),
                "step": False,
                "cmap": "viridis",
                "zorder": 2.0,
                "obj": "null",
                "hatch": '//', 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 1.0, 
                "fill": False, 
                "y_err": True, 
                "id": "_nnpdf30_totunc", 
                "axis": "ax"
            }

            config["objects"]["ratio__{0}_totunc_to__{0}_totunc".format(pdfset4)] = {
                "edgealpha": 1.0, 
                "style": "band", 
                "rasterized": False, 
                "capsize": 0, 
                "x_err": True, 
                "edgecolor": "_darkcolor4_", 
                "color": "_darkcolor4_", 
                "linestyle": "", 
                "step": False, 
                "cmap": "viridis", 
                "zorder": 2.0, 
                "linewidth": "2.0",
                "obj": "null", 
                "plot_datavals": False, 
                "marker": ".", 
                "alpha": 0.2, 
                "hatch": '//', 
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
            config["y_subplot_lims"] = ["-0.5", "0.5"]
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
                                  's=$Q^2\!={0}\,\mathrm{{GeV}}^2$?_topright_'.format(get_q2label(q2)),
                                  ] 
            config["output_path"] = 'pdfcomp_direct_{0}_{1}_ext.png'.format(partons[i], q2)
            configs.append(config)

    return configs

@callbacks.register('before_plot')
def final_plot(**kwargs):
    kwargs['mpl'].rcParams['hatch.linewidth'] = 1.5
#   kwargs['mpl'].rcParams['legend.fontsize'] = 20
#   kwargs['mpl'].rcParams['font.size'] = 20
