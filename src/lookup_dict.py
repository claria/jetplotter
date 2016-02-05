"""
Dictionary containing lookup values which will be replaced in the 
settings.
"""
lookup_dict = {
    'x_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ (GeV)',
        '_pt_': '$p_{\mathrm{T}}$ (GeV)',
        '_y_boost_': '$y_\mathrm{b}$',
        '_y_star_': '$y*$',
        '_right_': '{"position" : [1.0,0.0], "va" : "top", "ha" : "right"}',
        '_center_': '{"position" : [0.5,0.0], "va" : "top", "ha" : "center"}'
    },
    'y_label': {
        '_ptavg_': '$p_{\mathrm{T,avg}}$ (GeV)',
        '_y_star_': '$y^*$',
        '_top_': '{"position" : [0.0,1.0], "va" : "top", "ha" : "right"}',
        '_center_': '{"position" : [0.0,0.5], "va" : "center", "ha" : "right"}'

    },
    'label': {
        '_default_': 'nocut',
        '_yb0ys0_': '$0.0 \leq \, y_b < 1.0$  $0.0 \leq \, y^* < 1.0$',
        '_yb1ys0_': '$1.0 \leq \, y_b < 2.0$  $0.0 \leq \, y^* < 1.0$',
        '_yb2ys0_': '$2.0 \leq \, y_b < 3.0$  $0.0 \leq \, y^* < 1.0$',
        '_yb0ys1_': '$0.0 \leq \, y_b < 1.0$  $1.0 \leq \, y^* < 2.0$',
        '_yb0ys2_': '$0.0 \leq \, y_b < 1.0$  $2.0 \leq \, y^* < 3.0$',
        '_yb1ys1_': '$1.0 \leq \, y_b < 2.0$  $1.0 \leq \, y^* < 2.0$',
    },
    'color': {
        '_color0_': '#4C72B0',
        '_color1_': '#55A868',
        '_color2_': '#C44E52',
        '_color3_': '#8172B2',
        '_color4_': '#CCB974',
        '_color5_': '#64B5CD'
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
        '_cmsp_': 's=CMS Preliminary|x=0.0|y=1.01|va=bottom|ha=left',
        '_cmss_': 's=CMS Simulation|x=0.0|y=1.01|va=bottom|ha=left',
        '_20fb_': 's=$19.71\\,\mathrm{fb}^{-1}$ (8 TeV)|x=1.0|y=1.01|va=bottom|ha=right',
        '_8tev_': 's=8 TeV|x=1.0|y=1.01|va=bottom|ha=right',
        '_yb0ys0_': 's=$0.0 \leq \, y_b < 1.0$\n$0.0 \leq \, y^* < 1.0$',
        '_default_': 's=',
        '_yb1ys0_': 's=$1.0 \leq \, y_b < 2.0$\n$0.0 \leq \, y^* < 1.0$',
        '_yb2ys0_': 's=$2.0 \leq \, y_b < 3.0$\n$0.0 \leq \, y^* < 1.0$',
        '_yb0ys1_': 's=$0.0 \leq \, y_b < 1.0$\n$1.0 \leq \, y^* < 2.0$',
        '_yb0ys2_': 's=$0.0 \leq \, y_b < 1.0$\n$2.0 \leq \, y^* < 3.0$',
        '_yb1ys1_': 's=$1.0 \leq \, y_b < 2.0$\n$1.0 \leq \, y^* < 2.0$',
        '_yb0ys0auto_': 's=$0.0 \leq y_b < 1.0$  $0.0 \leq y^* < 1.0$?0.03,0.85',
        '_topleft_':     'x=0.0|y=1.01|va=bottom|ha=left',
        '_topright_':    'x=1.0|y=1.01|va=bottom|ha=right',
        '_upperleft_':   'x=0.05|y=0.95|va=top|ha=left',
        '_upperleft2_':   'x=0.05|y=0.85|va=top|ha=left',
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
