from util.plot_tools import default_colors, default_colors_dark, paired_colors

"""
Dictionary containing lookup values which will be replaced in the 
settings.
"""
lookup_dict = {
    'x_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ / GeV',
        '_ptavgreco_': '$p_{\mathrm{T,avg}}^{\mathrm{reco}}$ / GeV',
        '_ptavgreconu_': '$p_{\mathrm{T,avg}}^{\mathrm{reco}}$',
        '_ptavgptcl_': '$p_{\mathrm{T,avg}}^{\mathrm{ptcl}}$ / GeV',
        '_ptavggen_': '$p_{\mathrm{T,avg}}^{\mathrm{ptcl}}$ / GeV ',
        '_ptavggennu_': '$p_{\mathrm{T,avg}}^{\mathrm{ptcl}}$',
        '_pt_': '$p_{\mathrm{T}}$ / GeV',
        '_y_boost_': '$y_\mathrm{b}$',
        '_y_star_': '$y*$',
        '_right_': '{"position" : [1.0,0.0], "va" : "top", "ha" : "right"}',
        '_center_': '{"position" : [0.5,0.0], "va" : "top", "ha" : "center"}'
    },
    'y_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ / GeV',
        '_ptavgreco_': '$p_{\mathrm{T,avg}}^{\mathrm{reco}}$ / GeV',
        '_ptavgreconu_': '$p_{\mathrm{T,avg}}^{\mathrm{reco}}$',
        '_ptavggen_': '$p_{\mathrm{T,avg}}^{\mathrm{ptcl}}$ / GeV',
        '_ptavggennu_': '$p_{\mathrm{T,avg}}^{\mathrm{ptcl}}$',
        '_y_star_': '$y^*$',
        '_top_': '{"position" : [0.0,1.0], "va" : "bottom", "ha" : "right"}',
        '_center_': '{"position" : [0.0,0.5], "va" : "bottom", "ha" : "center"}'

    },
    'label': {
        '_default_': 'nocut',
        '_yb0ys0_': '$0 \leq \, y_b < 1$  $0 \leq \, y^{*} < 1$',
        '_yb1ys0_': '$1 \leq \, y_b < 2$  $0 \leq \, y^{*} < 1$',
        '_yb2ys0_': '$2 \leq \, y_b < 3$  $0 \leq \, y^{*} < 1$',
        '_yb0ys1_': '$0 \leq \, y_b < 1$  $1 \leq \, y^{*} < 2$',
        '_yb0ys2_': '$0 \leq \, y_b < 1$  $2 \leq \, y^{*} < 3$',
        '_yb1ys1_': '$1 \leq \, y_b < 2$  $1 \leq \, y^{*} < 2$',
    },
    'color': {
        '_color0_': default_colors[0],
        '_color1_': default_colors[1],
        '_color2_': default_colors[2],
        '_color3_': default_colors[3],
        '_color4_': default_colors[4],
        '_color5_': default_colors[5],
        '_darkcolor0_': default_colors_dark[0],
        '_darkcolor1_': default_colors_dark[1],
        '_darkcolor2_': default_colors_dark[2],
        '_darkcolor3_': default_colors_dark[3],
        '_darkcolor4_': default_colors_dark[4],
        '_darkcolor5_': default_colors_dark[5],
        '_colorpair0a_': paired_colors[0],
        '_colorpair0b_': paired_colors[1],
        '_colorpair1a_': paired_colors[2],
        '_colorpair1b_': paired_colors[3],
        '_colorpair2a_': paired_colors[4],
        '_colorpair2b_': paired_colors[5],
        '_colorpair3a_': paired_colors[6],
        '_colorpair3b_': paired_colors[7],
        '_colorpair4a_': paired_colors[8],
        '_colorpair4b_': paired_colors[9],
    },
    'x_lims': {
        '_yb0ys0_xmin_' : 133.,
        '_yb0ys1_xmin_' : 133.,
        '_yb0ys2_xmin_' : 133.,
        '_yb1ys0_xmin_' : 133.,
        '_yb1ys1_xmin_' : 133.,
        '_yb2ys0_xmin_' : 133.,
        '_yb0ys0_xmax_' : 1784.,
        '_yb0ys1_xmax_' : 1248.,
        '_yb0ys2_xmax_' : 548.,
        '_yb1ys0_xmax_' : 1032.,
        '_yb1ys1_xmax_' : 686.,
        '_yb2ys0_xmax_' : 430.,
    },
    'y_lims': {
        '_yb0ys0_xmin_' : 133.,
        '_yb0ys1_xmin_' : 133.,
        '_yb0ys2_xmin_' : 133.,
        '_yb1ys0_xmin_' : 133.,
        '_yb1ys1_xmin_' : 133.,
        '_yb2ys0_xmin_' : 133.,
        '_yb0ys0_xmax_' : 1784.,
        '_yb0ys1_xmax_' : 1248.,
        '_yb0ys2_xmax_' : 548.,
        '_yb1ys0_xmax_' : 1032.,
        '_yb1ys1_xmax_' : 686.,
        '_yb2ys0_xmax_' : 430.,
    },

    'data_lims': {
        '_yb0ys0_xmin_' : 133.,
        '_yb0ys1_xmin_' : 133.,
        '_yb0ys2_xmin_' : 133.,
        '_yb1ys0_xmin_' : 133.,
        '_yb1ys1_xmin_' : 133.,
        '_yb2ys0_xmin_' : 133.,
        '_yb0ys0_xmax_' : 1784.,
        '_yb0ys1_xmax_' : 1248.,
        '_yb0ys2_xmax_' : 548.,
        '_yb1ys0_xmax_' : 1032.,
        '_yb1ys1_xmax_' : 686.,
        '_yb2ys0_xmax_' : 430.,
    },
    'global': {
        '_yb0ys0_xmin_' : 133.,
        '_yb0ys1_xmin_' : 133.,
        '_yb0ys2_xmin_' : 133.,
        '_yb1ys0_xmin_' : 133.,
        '_yb1ys1_xmin_' : 133.,
        '_yb2ys0_xmin_' : 133.,
        '_yb0ys0_xmax_' : 1784.,
        '_yb0ys1_xmax_' : 1248.,
        '_yb0ys2_xmax_' : 548.,
        '_yb1ys0_xmax_' : 1032.,
        '_yb1ys1_xmax_' : 686.,
        '_yb2ys0_xmax_' : 430.,
    },
    'ax_texts': {
        '_cms_': 's=CMS|x=0.0|y=1.01|va=bottom|ha=left',
        '_cmsp_': 's=CMS Preliminary|x=0.0|y=1.002|va=bottom|ha=left',
        '_cmss_': 's=CMS Simulation|x=0.0|y=1.002|va=bottom|ha=left',
        '_20fb_': 's=$19.\!7\\,\mathrm{fb}^{-1}$ (8 TeV)|x=1.0|y=1.002|va=bottom|ha=right',
        '_8tev_': 's=8 TeV|x=1.0|y=1.002|va=bottom|ha=right',
        '_default_': 's=',
        '_yb0ys0_': 's=$0 \leq \, y_b < 1$\n$0 \leq \, y^{*} < 1$',
        '_yb1ys0_': 's=$1 \leq \, y_b < 2$\n$0 \leq \, y^{*} < 1$',
        '_yb2ys0_': 's=$2 \leq \, y_b < 3$\n$0 \leq \, y^{*} < 1$',
        '_yb0ys1_': 's=$0 \leq \, y_b < 1$\n$1 \leq \, y^{*} < 2$',
        '_yb0ys2_': 's=$0 \leq \, y_b < 1$\n$2 \leq \, y^{*} < 3$',
        '_yb1ys1_': 's=$1 \leq \, y_b < 2$\n$1 \leq \, y^{*} < 2$',
        '_yb0ys0auto_': 's=$0.0 \leq y_b < 1.0$  $0.0 \leq y^* < 1.0$?0.03,0.85',
        '_topleft_':     'x=0.0|y=1.002|va=bottom|ha=left',
        '_topright_':    'x=1.0|y=1.002|va=bottom|ha=right',
        '_upperleft_':   'x=0.05|y=0.95|va=top|ha=left',
        '_upperleft2_':   'x=0.05|y=0.83|va=top|ha=left',
        '_upperright_':  'x=0.95|y=0.95|va=top|ha=right',
        '_bottomleft_':  'x=0.05|y=0.05|va=bottom|ha=left',
        '_bottomright_': 'x=0.95|y=0.05|va=bottom|ha=right',

    }

}


def get_lookup_val(key, s):
    """ Replaces all occurences of lookup keys in string with lookup dict values."""
    if key in lookup_dict:
        for lk, lv in lookup_dict[key].iteritems():
            if isinstance(s, basestring) and lk in s:
                s = s.replace(lk, str(lv))
    return s


def perform_lookup_replacement(node, parent=None):
    """Walks the dict recursively and replaces all strs with the lookups."""
    if parent is None:
        parent = []
    for k in node.keys():
        if isinstance(node[k], basestring):
            node[k] = get_lookup_val(k, node[k])
            for par in parent:
                node[k] = get_lookup_val(par, node[k])
        elif isinstance(node[k], list):
            for i in xrange(len(node[k])):
                if isinstance(node[k][i], basestring):
                    node[k][i] = get_lookup_val(k, node[k][i])
                    for par in parent:
                        node[k] = get_lookup_val(par, node[k])
                elif isinstance(node[k][i], dict):
                    parent.append(k)
                    perform_lookup_replacement(node[k][i], parent=parent)
        elif isinstance(node[k], dict):
            parent.append(k)
            perform_lookup_replacement(node[k], parent=parent)
