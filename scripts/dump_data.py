#!/usr/bin/env python2
import os
import sys
import numpy as np
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.root_tools import get_np_object


def main():
    pass
    ybys_bins = ['yb0ys0', 'yb0ys1', 'yb0ys2', 'yb1ys0', 'yb1ys1', 'yb2ys0']


    for ybys_bin in ybys_bins:
        unf_data = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA.root?{0}/h_ptavg'.format(ybys_bin))

        data = collections.OrderedDict()
        data['yb_low'] = np.array([float(ybys_bin[2])] * len(unf_data.xl))
        data['yb_high'] = np.array([float(ybys_bin[2]) + 1.0] * len(unf_data.xl))
        data['ys_low'] = np.array([float(ybys_bin[5])] * len(unf_data.xl))
        data['ys_high'] = np.array([float(ybys_bin[5]) + 1.0] * len(unf_data.xl))
        data['pt_low'] = unf_data.xl
        data['pt_high'] = unf_data.xu
        data['sigma'] = unf_data.y
        # lumi
        lumi_unc = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/lumi_unc_relative.root?{0}/lumi_unc_up'.format(ybys_bin))
        data['lumi'] = (lumi_unc.y - 1.) * 100.

        jec_sources  = [
                       'AbsoluteScale','AbsoluteStat','AbsoluteMPFBias',
                       'Fragmentation',
                       'SinglePionECAL',
                       'SinglePionHCAL',
                       'FlavorQCD',
                       'TimeEta',
                       'TimePt',
                       'RelativeJEREC1','RelativeJEREC2','RelativeJERHF',
                       'RelativePtBB','RelativePtEC1','RelativePtEC2','RelativePtHF',
                       'RelativeFSR',
                       'RelativeStatEC2', 'RelativeStatHF', 'RelativeStatFSR',
                       'PileUpDataMC',
                       'PileUpPtRef',
                       'PileUpPtBB','PileUpPtEC1','PileUpPtEC2','PileUpPtHF',
                       'PileUpEnvelope',
                       ]

        jec_default = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?{0}/h_ptavg'.format(ybys_bin))
        for jec_source in jec_sources:
            jec_up = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?{0}_{1}_up/h_ptavg'.format(ybys_bin, jec_source))
            jec_dn = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_DATA.root?{0}_{1}_dn/h_ptavg'.format(ybys_bin, jec_source))
            # data['{0}_up'.format(jec_source)] = jec_up.y/jec_default.y -1.
            # data['{0}_dn'.format(jec_source)] = 1. - jec_dn.y/jec_default.y
            data['{0}'.format(jec_source)] = np.abs((jec_up.y - jec_dn.y)/2.0)/jec_default.y

        for k,v in data.iteritems():
            v[np.isnan(v)] = 0.

        if 'yb0ys0' == ybys_bin:
            labels = data.keys()
            print ' '.join(['{0:<15}'.format(label) for label in labels])
        print_data(data, labels=labels)

def print_data(data, labels):
    # labels = data.keys()
    # labels.sort()
    nbins = len(data[labels[0]])
    for i in xrange(nbins):
        vals = ['{0:<15.4e}'.format(data[label][i]) for label in labels]
        print ' '.join(vals)

# unfolded data
# stat unc
# correlations
# jec
# systematic unfolding





if __name__ == '__main__':
    main()
