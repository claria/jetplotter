import os

import ROOT

from util.root_tools import get_root_object, get_tgraphasymm_from_histos, get_root_file

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(True)

from modules.base_module import BaseModule

import logging

log = logging.getLogger('__name__')


class RootModule(BaseModule):
    """ Input module to load histograms and graphs from a root file.

        This modules runs at the beginning to load objects from root files and puts these objects into the config dict.
        Therefore you always have to give the id in which the object will be stored. The --input-graph options has a few
        more options to construct a TGraphAsymmErrors from multiple histograms.
    """

    def __init__(self):
        super(RootModule, self).__init__()
        self.arg_group.add_argument('-i', '--input', nargs='+', type='str2kvstr', action='setting',
                                    help='Path to root file or objects in root files with syntax '
                                         'id:rootfile?path/to/object.')
        self.arg_group.add_argument('--input_tgraph', nargs='+', type='str2kvstr', action='setting',
                                    help='Path to root file or objects in root files with '
                                         'syntax id:rootfile?path/to/object.')

    def __call__(self, config):
        for id, item in config['objects'].iteritems():
            if 'input' in item:
                item['obj'] = get_root_object(item['input'])
            elif 'input_tgraph' in item:
                if '&' in item['input_tgraph']:
                    item['obj'] = get_tgraphasymm_from_histos(
                        *[get_root_object(input) for input in item['input_tgraph'].split('&')])
                else:
                    item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input_tgraph']))
            elif 'input_asymmerrgraph' in item:
                item['obj'] = ROOT.TGraphAsymmErrors(get_root_object(item['input']))


class RootOutputModule(BaseModule):
    def __init__(self):
        super(RootOutputModule, self).__init__()
        self.arg_group.add_argument('--root-output', default=None, nargs='+', type=str,
                                    help='List of ids, which objects will be written out to a root file.')

    def __call__(self, config):
        if config.get('root-output', []):
            ids = config['root-output']
        else:
            ids = config['objects'].keys()

        root_output_filename = os.path.splitext(os.path.join(config['output_prefix'], config['output_path']))[
                                   0] + '.root'

        f = get_root_file(root_output_filename, "RECREATE")
        f.cd('/')

        for id in ids:
            if id not in config['objects']:
                raise ValueError('Id {0} not found within objects. Check your supplied ids.'.format(id))
            if 'obj' in config['objects'][id]:
                log.info('Writing id {0} to file {1}'.format(id, root_output_filename))
                config['objects'][id]['obj'].Write(id)
            else:
                log.debug('Omitting id {0} since no root object found.'.format(id))
                continue

        f.Close()


class BuildTGraph(BaseModule):
    def __init__(self):
        super(BuildTGraph, self).__init__()
        self.arg_group.add_argument('--build-tgraph', default=[], nargs='+', type='str2kvdict',
                                    help='List of ids, which objects will be written out to a root file.')

    def __call__(self, config):
        if config['build_tgraph']:
            print config['build_tgraph']
            for id, input_ids in config['build_tgraph']:
                if len(input_ids) == 1:
                    # Basically only copies th TGraph
                    new_graph = ROOT.TGraphErrors(config['objects'][input_ids[0]]['obj'])
                elif len(input_ids) == 2:
                    # The both inputs define the minimum maximum and the center is set by the mean of both.
                    tmp_tgraph1 = config['objects'][input_ids[0]]['obj']
                    tmp_tgraph2 = config['objects'][input_ids[1]]['obj']
                    if not (tmp_tgraph1.GetN() == tmp_tgraph2.GetN()):
                        raise ValueError('The both objects must have the same number of points.')
                    print type(tmp_tgraph1)
                    new_graph = ROOT.TGraphAsymmErrors(tmp_tgraph1)
                    for i in xrange(new_graph.GetN()):
                        tmp_tgraph1x, tmp_tgraph1y = ROOT.Double(0), ROOT.Double(0)
                        tmp_tgraph1.GetPoint(i, tmp_tgraph1x, tmp_tgraph1y)

                        tmp_tgraph2x, tmp_tgraph2y = ROOT.Double(0), ROOT.Double(0)
                        tmp_tgraph2.GetPoint(i, tmp_tgraph2x, tmp_tgraph2y)

                        center = 0.5 * (tmp_tgraph1y + tmp_tgraph2y)

                        new_graph.SetPoint(i, tmp_tgraph1x, 0.5 * (tmp_tgraph1y + tmp_tgraph2y))
                        new_graph.SetPointEYlow(i, abs(tmp_tgraph1y - tmp_tgraph2y) / 2.)
                        new_graph.SetPointEYhigh(i, abs(tmp_tgraph1y - tmp_tgraph2y) / 2.)

                        new_graph.SetPointEXlow(i, tmp_tgraph1.GetErrorX(i))
                        new_graph.SetPointEXhigh(i, tmp_tgraph1.GetErrorX(i))

                elif len(input_ids) == 3:
                    # The both inputs define the minimum maximum and the center is set by the mean of both.
                    tmp_tgraph1 = config['objects'][input_ids[0]]['obj']
                    tmp_tgraph2 = config['objects'][input_ids[1]]['obj']
                    tmp_tgraph3 = config['objects'][input_ids[2]]['obj']
                    if not (tmp_tgraph1.GetN() == tmp_tgraph2.GetN() == tmp_tgraph3.GetN()):
                        raise ValueError('The input objects must have the same number of points.')

                    new_graph = ROOT.TGraphAsymmErrors(tmp_tgraph1)

                    for i in xrange(tmp_tgraph1.GetN()):
                        tmp_tgraph1x, tmp_tgraph1y = ROOT.Double(0), ROOT.Double(0)
                        tmp_tgraph1.GetPoint(i, tmp_tgraph1x, tmp_tgraph1y)

                        tmp_tgraph2x, tmp_tgraph2y = ROOT.Double(0), ROOT.Double(0)
                        tmp_tgraph2.GetPoint(i, tmp_tgraph2x, tmp_tgraph2y)

                        tmp_tgraph3x, tmp_tgraph3y = ROOT.Double(0), ROOT.Double(0)
                        tmp_tgraph3.GetPoint(i, tmp_tgraph3x, tmp_tgraph3y)

                        new_graph.SetPoint(i, tmp_tgraph1x, tmp_tgraph1y)
                        new_graph.SetPointEYlow(i, tmp_tgraph1y - tmp_tgraph2y)
                        new_graph.SetPointEYhigh(i, tmp_tgraph3y - tmp_tgraph1y)

                        new_graph.SetPointEXlow(i, tmp_tgraph1.GetErrorX(i))
                        new_graph.SetPointEXhigh(i, tmp_tgraph1.GetErrorX(i))

                config['objects'].setdefault(id, {})['obj'] = new_graph
