#!/usr/bin/env python2
import os
import sys
import numpy as np
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.root_tools import get_np_object, get_root_object
from util.root2np import R2npObject1D


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
        unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root.Scale(1.0, 'width')
        unf_data = R2npObject1D(unf_data_root)
        np_factor = get_np_object('~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor'.format(ybys_bin))

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
        # lumi
        lumi_unc = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/lumi_unc_relative.root?{0}/lumi_unc_up'.format(ybys_bin))
        data['lumi'] = (lumi_unc.y - 1.) * 100.

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

        jec_default = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?{0}/h_ptavg'.format(ybys_bin))
        for jec_source in jec_sources:
            jec_up = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?{0}_{1}_up/h_ptavg'.format(ybys_bin, jec_source))
            jec_dn = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?{0}_{1}_dn/h_ptavg'.format(ybys_bin, jec_source))
            # data['{0}_up'.format(jec_source)] = jec_up.y/jec_default.y -1.
            # data['{0}_dn'.format(jec_source)] = 1. - jec_dn.y/jec_default.y
            # data['{0}'.format(jec_source)] = np.abs((jec_up.y - jec_dn.y)/2.0)/jec_default.y * 100.
            data['{0}'.format(jec_source)] = np.maximum(np.abs(1. - jec_up.y/jec_default.y), np.abs(1. - jec_dn.y/jec_default.y)) * 100.
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
            'yb0ys0' : (74.,1784.),
            'yb0ys1' : (74.,1248.),
            'yb0ys2' : (74.,548.),
            'yb1ys0' : (74.,1032.),
            'yb1ys1' : (74.,686),
            'yb2ys0' : (74.,430.),
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
            vals = ['{0:<15.4g}'.format(data[label][i]) for label in labels]
            print ' '.join(vals)

# unfolded data
# stat unc
# correlations
# jec
# systematic unfolding

if __name__ == '__main__':
    main()
