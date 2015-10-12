#!/usr/bin/python

import os
import sys
import glob
import itertools
import dateutil.parser


def main():

    cwd = os.path.dirname(os.path.realpath(__file__))

    plot_dirs = [x[0] for x in os.walk(cwd) if x[0] != cwd]

    for plot_dir in plot_dirs:
        plots = glob.glob(os.path.join(plot_dir, '*.png'))
        sort_func = lambda x: os.path.basename(x).rsplit('_', 1)[0]
        plots.sort(key=sort_func)

        data = dict()
        for i, j in itertools.groupby(plots, key=sort_func):
            files = list(j)
            # sort files after date
            files.sort(key=lambda x: dateutil.parser.parse(os.path.splitext(os.path.basename(x))[0].rsplit('_',1)[1]), reverse=True)
            data[i] = files

        html_content = get_plot_page(data)

        filename = os.path.join(plot_dir, 'index.html')
        with open(filename, 'w') as f:
            f.write(html_content)



def get_plot_page(data):

    html_page = ''
    html_page += header

    for id, plots in sorted(data.iteritems()):
        sub = ''
        if len(plots) > 1:
            for i, plot in enumerate(plots[:10]):
                sub += '[<a href="{1}">{0}</a>] '.format(i, os.path.basename(plot))
        template = '<div class="plot"><div style="margin-left:30px"><h3>{0}</h3>{2}<a href="{1}"></div><img src="{1}" height="400" alt="plot missing"></a></div>\n'.format(id, os.path.basename(plots[0]),sub)
        html_page += template

    html_page += footer

    return html_page



header = """
<!DOCTYPE html>
<html>
<head>
<title>Plot Overview</title>
<style type="text/css">
.plot {float:left }
h3 {
    margin-bottom:5px;
}
</style>
</head>
<body>
<h1>Plot overview</h1>
"""
footer = """
</body>
</html>
"""

if __name__ == '__main__':
    main()
