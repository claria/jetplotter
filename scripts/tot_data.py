#!/usr/bin/env python2
import os
import sys
import numpy as np
import collections

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from util.root_tools import get_np_object, get_root_object
from util.root2np import R2npObject1D
import ROOT


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

    f = ROOT.TFile('data_summary.root', 'RECREATE')

    for i, ybys_bin in enumerate(ybys_bins):
        # unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root = get_root_object('~/dust/dijetana/ana/CMSSW_7_2_3/unf_DATA_NLO.root?{0}/h_ptavg'.format(ybys_bin))
        unf_data_root.Scale(1.0, 'width')
        unf_data = R2npObject1D(unf_data_root)
        np_factor = get_np_object('~/dust/dijetana/plot/plots/np_factors_calc_{0}.root?res_np_factor'.format(ybys_bin))

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
        data['uncor'] = np.array([1.0] * len(unf_data.xl))
        data['stat'] = unf_data.yerr/unf_data.y * 100.
        data['jer_up'] = jer_data.yerru/jer_data.y * 100.
        data['jer_dn'] = jer_data.yerrl/jer_data.y * 100.
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

        jec_default = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}/h_genptavg'.format(ybys_bin))
        for jec_source in jec_sources:
            jec_up = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_{1}_up/h_genptavg'.format(ybys_bin, jec_source))
            jec_dn = get_np_object('~/dust/dijetana/ana/CMSSW_7_2_3/JEC_GEN.root?{0}_{1}_dn/h_genptavg'.format(ybys_bin, jec_source))
            # data['{0}_up'.format(jec_source)] = jec_up.y/jec_default.y -1.
            # data['{0}_dn'.format(jec_source)] = 1. - jec_dn.y/jec_default.y
            # data['{0}'.format(jec_source)] = np.abs((jec_up.y - jec_dn.y)/2.0)/jec_default.y * 100.
            data['{0}'.format(jec_source)] = np.maximum(np.abs(1. - jec_up.y/jec_default.y), np.abs(1. - jec_dn.y/jec_default.y)) * 100.
            data['{0}'.format(jec_source)] = 0.5 *( (jec_up.y -jec_dn.y)/jec_default.y) * 100.
            # data['{0}'.format(jec_source)] = np.abs(1 - jec_up.y/jec_default.y) * 100.

        for k,v in data.iteritems():
            v[np.isnan(v)] = 0.
            v[np.isinf(v)] = 0.

        #sums
        stat_error_u = data['sigma'] * (data['stat']/100.)
        stat_error_l = data['sigma'] * (data['stat']/100.)
        syst_error_u = np.zeros((len(data['sigma'])))
        syst_error_l = np.zeros((len(data['sigma'])))

        jec_error_u = np.zeros((len(data['sigma'])))
        jec_error_l = np.zeros((len(data['sigma'])))

        jer_error_u = np.zeros((len(data['sigma'])))
        jer_error_l = np.zeros((len(data['sigma'])))

        unc_error_u = np.zeros((len(data['sigma'])))
        unc_error_l = np.zeros((len(data['sigma'])))

        lumi_error_u = np.zeros((len(data['sigma'])))
        lumi_error_l = np.zeros((len(data['sigma'])))

        lumi_error_u = data['lumi']/100. * data['sigma']
        lumi_error_l = data['lumi']/100. * data['sigma']

        unc_error_u = data['uncor']/100. * data['sigma']
        unc_error_l = data['uncor']/100. * data['sigma']

        jer_error_u = data['jer_up']/100. * data['sigma']
        jer_error_l = data['jer_dn']/100. * data['sigma']

        syst_error_u += (data['uncor']/100. * data['sigma'])**2
        syst_error_l += (data['uncor']/100. * data['sigma'])**2

        syst_error_u += (data['lumi']/100. * data['sigma'])**2
        syst_error_l += (data['lumi']/100. * data['sigma'])**2

        for jec_source in jec_sources:
            syst_error_u += (data[jec_source]/100. * data['sigma'])**2
            syst_error_l += (data[jec_source]/100. * data['sigma'])**2

            jec_error_u += (data[jec_source]/100. * data['sigma'])**2
            jec_error_l += (data[jec_source]/100. * data['sigma'])**2

        jec_error_u = np.sqrt(jec_error_u)
        jec_error_l = np.sqrt(jec_error_l)

        syst_error_u = np.sqrt(syst_error_u)
        syst_error_l = np.sqrt(syst_error_l)

        f.cd()
        f.mkdir(ybys_bin)
        f.Cd("/" + ybys_bin)

        data_tot = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_stat = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_syst = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_lumi = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_unc = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_jec = ROOT.TGraphAsymmErrors(len(data['sigma'])) 
        data_jer = ROOT.TGraphAsymmErrors(len(data['sigma'])) 

        for i in range(len(data['sigma'])):
            data_tot.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_tot.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], np.sqrt(stat_error_l[i]**2+syst_error_l[i]**2), np.sqrt(stat_error_u[i]**2+syst_error_u[i]**2))

            data_stat.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_stat.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], stat_error_l[i], stat_error_u[i])

            data_syst.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_syst.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], syst_error_l[i], syst_error_u[i])

            data_lumi.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_lumi.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], lumi_error_l[i], lumi_error_u[i])

            data_unc.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_unc.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], unc_error_l[i], unc_error_u[i])

            data_jec.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_jec.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], jec_error_l[i], jec_error_u[i])

            data_jer.SetPoint(i, unf_data.x[i], data['sigma'][i])
            data_jer.SetPointError(i, unf_data.xerrl[i], unf_data.xerru[i], jer_error_l[i], jer_error_u[i])



        data_tot.Write('data_tot')
        data_stat.Write('data_stat')
        data_syst.Write('data_syst')
        data_lumi.Write('data_lumi')
        data_unc.Write('data_unc')
        data_jec.Write('data_jec')
        data_jer.Write('data_jer')


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
