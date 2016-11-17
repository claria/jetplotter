#!/usr/bin/env python2
import os
import sys
import numpy as np
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.root_tools import get_np_object, get_root_object
from util.root2np import R2npObject1D


nongaussian_unc = {
'yb0ys0': np.array([ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.11,  0.08,  0.07,  0.22,  0.06,  0.0 ,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.0 ,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.0 ,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.  ]),
'yb0ys1': np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.37,   0.32,   0.1 ,   0.0 ,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,  00.00,   0.  ,
         0.  ,   0.  ,   0.  ]),
'yb0ys2' : np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   1.46,   1.19,   1.62,   1.38,   1.68,   0.31,   0.00,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,  00.00,  00.00,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ]),
'yb1ys0' :np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.43,   0.4 ,   0.33,   0.34,   0.29,   0.13,   0.0 ,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.0 ,
         0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,   0.00,
         0.00,   0.00,   0.00,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ]),
'yb1ys1' : np.array([ 0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        1.19,  1.18,  1.01,  1.42,  1.11,  0.97,  0.5 ,  0.00,  0.00,
        0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,  0.00,
        0.00,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,
        0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ,  0.  ]),
'yb2ys0' : np.array([  0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   1.8 ,   1.69,   1.17,   1.81,   1.78,   2.38,   1.08,
         0.64,   0.  ,   0.  ,   0.  ,   0.  ,   0.00,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,   0.  ,
         0.  ,   0.  ,   0.  ])
}




def main():
    pass
    ybys_bins = ['yb0ys0', 'yb0ys1', 'yb0ys2', 'yb1ys0', 'yb1ys1', 'yb2ys0']
    def get_coltype(s):
        if s in ['yb_low', 'yb_high', 'ys_low', 'ys_high',  'pt_low', 'pt_high', 'NPCorr', 'nbin']:
            return 'Bin'
        elif s in ['sigma']:
            return 'Sigma'
        else:
            return 'Error'


    for i, ybys_bin in enumerate(ybys_bins):
        # unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO_WITHFAKES.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root.Scale(1.0, 'width')
        unf_data = R2npObject1D(unf_data_root)
        # np_factor = get_np_object('~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor'.format(ybys_bin))

        # hack for full range
        np_factor = get_np_object('~/dust/dijetana/plot/plots/np_factors_nlo_final_{0}.root?res_np_factor'.format(ybys_bin))
        np_factor.x = np.concatenate((unf_data.x[0:9],np_factor.x))
        np_factor.x = np.concatenate((np_factor.x,unf_data.x[np_factor.x.size:]))
        np_factor.y = np.concatenate((np.zeros((9,)),np_factor.y))
        np_factor.y = np.concatenate((np_factor.y,np.zeros((unf_data.y.size - np_factor.y.size,))))

        np_factor.yerrl = np.concatenate((np.zeros((9,)),np_factor.yerrl))
        np_factor.yerrl = np.concatenate((np_factor.yerrl,np.zeros((unf_data.y.size - np_factor.yerrl.size,))))

        np_factor.yerru = np.concatenate((np.zeros((9,)),np_factor.yerru))
        np_factor.yerru = np.concatenate((np_factor.yerru,np.zeros((unf_data.y.size - np_factor.yerru.size,))))

        # hack for full range ewk
        ewk_factor = get_np_object('~/dust/dijetana/ewk/ewk_dijet.root?{0}/ewk_corr'.format(ybys_bin))
        ewk_factor.x = np.concatenate((unf_data.x[0:9],ewk_factor.x))
        ewk_factor.x = np.concatenate((ewk_factor.x,unf_data.x[ewk_factor.x.size:]))
        ewk_factor.y = np.concatenate((np.zeros((9,)),ewk_factor.y))
        ewk_factor.y = np.concatenate((ewk_factor.y,np.zeros((unf_data.y.size - ewk_factor.y.size,))))

        ewk_factor.yerrl = np.concatenate((np.zeros((9,)),ewk_factor.yerrl))
        ewk_factor.yerrl = np.concatenate((ewk_factor.yerrl,np.zeros((unf_data.y.size - ewk_factor.yerrl.size,))))

        ewk_factor.yerru = np.concatenate((np.zeros((9,)),ewk_factor.yerru))
        ewk_factor.yerru = np.concatenate((ewk_factor.yerru,np.zeros((unf_data.y.size - ewk_factor.yerru.size,))))

        # just multiply with np _factors for now
        np_factor.y = np_factor.y * ewk_factor.y


        jer_data = get_np_object('~/dust/dijetana/plot/plots/jer_uncert_{0}.root?jer_uncert'.format(ybys_bin))

        data = collections.OrderedDict()
        data['nbin'] = np.array([i] * len(unf_data.xl))
        data['yb_low'] = np.array([float(ybys_bin[2])] * len(unf_data.xl))
        data['yb_high'] = np.array([float(ybys_bin[2]) + 1.0] * len(unf_data.xl))
        data['ys_low'] = np.array([float(ybys_bin[5])] * len(unf_data.xl))
        data['ys_high'] = np.array([float(ybys_bin[5]) + 1.0] * len(unf_data.xl))
        data['pt_low'] = unf_data.xl
        data['pt_high'] = unf_data.xu
        data['sigma'] = unf_data.y
        data['NPCorr'] = np_factor.y
        data['nperr'] = 0.5 * (np_factor.yu - np_factor.yl)/np_factor.y * 100.
        data['uncor'] = np.array([1.0] * len(unf_data.xl))
        data['stat'] = unf_data.yerr/unf_data.y * 100.

        data['jererr'] = (jer_data.yu - jer_data.yl)/jer_data.y * 100.

        # lumi
        lumi_unc = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/lumi_unc_relative.root?{0}/lumi_unc_up'.format(ybys_bin))
        data['lumi'] = (lumi_unc.y - 1.) * 100.

        # non-gaussian tails
        # unf_smeared = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/SMEARED_NEW2_QCDMGP6.root?{0}/h_ptavg'.format(ybys_bin))
        # unf_scaled = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/SMEARED_OLD_QCDMGP6.root?{0}/h_ptavg'.format(ybys_bin))
        # data['nongaussiantails'] = np.abs(unf_smeared.y - unf_scaled.y)/unf_smeared.y / 2.0 * 100.
        data['nongaussiantails'] = nongaussian_unc[ybys_bin] 
        # data['nongaussiantails'] = smooth(data['nongaussiantails'], 3)
        # np.set_printoptions(precision=2)
        # np.set_printoptions(suppress=True)
        # print ybys_bin, np.array_repr(np.nan_to_num(data['nongaussiantails']))


        jec_sources  = [
                       'AbsoluteScale','AbsoluteStat','AbsoluteMPFBias',
                       'Fragmentation',
                       'SinglePionECAL',
                       'SinglePionHCAL',
                       'FlavorQCD',
                       'RelativeJEREC1','RelativeJEREC2','RelativeJERHF',
                       'RelativePtBB','RelativePtEC1','RelativePtEC2','RelativePtHF',
                       'RelativeFSR',
                       'RelativeStatEC2', 'RelativeStatHF', 'RelativeStatFSR',
                       'PileUpDataMC',
                       'PileUpPtRef',
                       'PileUpPtBB','PileUpPtEC1','PileUpPtEC2','PileUpPtHF',
                       ]

        jec_default = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}/h_genptavg'.format(ybys_bin))
        for jec_source in jec_sources:
            jec_up = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_{1}_up/h_genptavg'.format(ybys_bin, jec_source))
            jec_dn = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_{1}_dn/h_genptavg'.format(ybys_bin, jec_source))
            # data['{0}_up'.format(jec_source)] = jec_up.y/jec_default.y -1.
            # data['{0}_dn'.format(jec_source)] = 1. - jec_dn.y/jec_default.y
            # data['{0}'.format(jec_source)] = np.abs((jec_up.y - jec_dn.y)/2.0)/jec_default.y * 100.
            # data['{0}'.format(jec_source)] = np.maximum(np.abs(1. - jec_up.y/jec_default.y), np.abs(1. - jec_dn.y/jec_default.y)) * 100.
            data['{0}'.format(jec_source)] = 0.5 *np.abs((jec_up.y -jec_dn.y))/jec_default.y * 100.
            data['{0}'.format(jec_source)][np.abs(data['{0}'.format(jec_source)]) < 0.05 ] = 0.0
            # data['{0}'.format(jec_source)] = np.abs(1 - jec_up.y/jec_default.y) * 100.

        for k,v in data.iteritems():
            v[np.isnan(v)] = 0.
            v[np.isinf(v)] = 0.

        if 'yb0ys0' == ybys_bin:
            labels = data.keys()
            print ', '.join(['\'{0}\''.format(label) for label in labels])
            print ', '.join(['\'{0}\''.format(get_coltype(label)) for label in labels])
            print 'NColumn', len(labels)
        print_data(data, labels=labels, ybys_bin=ybys_bin)

def infinalrange(pt_low, ybys_bin):
    cuts = {
            'yb0ys0' : (133.,1784.),
            'yb0ys1' : (133.,1248.),
            'yb0ys2' : (133.,548.),
            'yb1ys0' : (133.,1032.),
            'yb1ys1' : (133.,686),
            'yb2ys0' : (133.,430.),
            }
    if pt_low >= cuts[ybys_bin][0] and pt_low < cuts[ybys_bin][1]:
        return True
    return False

def print_data(data, labels, ybys_bin):
    # labels = data.keys()
    # labels.sort()
    nbins = len(data[labels[0]])
    for i in xrange(nbins):
        if infinalrange(data['pt_low'][i], ybys_bin):
            vals = ['{0:<15.4G}'.format(data[label][i]) for label in labels]
            print ' '.join(vals)

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth

if __name__ == '__main__':
    main()
