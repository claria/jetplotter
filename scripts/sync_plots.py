#! /usr/bin/env python

import logging

log = logging.getLogger(__name__)

import tempfile
import glob
import subprocess
import stat
import os
import sys
import shutil
import shlex
from datetime import date
from datetime import datetime
import time
import random 

def scp(src, remote, destination, args=''):
    cmd = 'scp {0} {3} {1}:{2}'.format(src, remote, destination, args)
    log.debug('Executing command \'{0}\''.format(cmd))
    rc = subprocess.call(cmd.split())
    return rc

def ssh(remote, cmd, args=''):
    cmd = 'ssh -x {2} {0} {1}'.format(remote, cmd, args)
    log.debug('Executing command \'{0}\''.format(cmd))
    print cmd.split()
    rc = subprocess.call(shlex.split(cmd))
    return rc

def create_copy(filelist, suffix=None):
    tempdir = tempfile.mkdtemp()
    new_filelist = []
    for filename in filelist:
        new_filename = os.path.join(tempdir, '{0}{1}{2}'.format(os.path.splitext(os.path.basename(filename))[0], 
                                                                 '_' + suffix if suffix else '', 
                                                                 os.path.splitext(filename)[1]))
        shutil.copy(filename, new_filename)
        st = os.stat(new_filename)
        os.chmod(new_filename, st.st_mode | stat.S_IROTH)
        new_filelist.append(new_filename)
    return new_filelist


def main():
    remote_host = 'sieber@ekplx2.physik.uni-karlsruhe.de' 
    remote_basedir = '/ekpwww/web/sieber/public_html/private/plots/'
    remote_dir = os.path.join(remote_basedir, date.today().isoformat())
    current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

    if len(sys.argv) > 1:
        file_list = sys.argv[1:]
    else:
        file_list = glob.glob('plots/*.png')

    for filename in file_list[:]:
        print 'checking file', filename
        if os.path.isfile(filename.replace('.png', '.json')):
            file_list.append(filename.replace('.png', '.json'))
        if os.path.isfile(filename.replace('.png', '.pdf')):
            file_list.append(filename.replace('.png', '.pdf'))

    files_to_copy = create_copy(file_list, current_datetime)
    print 'create copies of all plots'
    files_to_copy += create_copy(['index.php'])

    time.sleep(random.uniform(1,10))
    rsync(files_to_copy, remote_host, remote_dir)


def rsync(filelist, remote_host, remote_dir):
    cmd = 'rsync -uavz --remove-source-files {0} {1}:{2}'.format(' '.join(filelist), remote_host, remote_dir)
    log.debug('Executing command \'{0}\''.format(cmd))
    rc = subprocess.call(cmd.split())
    return rc



if __name__ == '__main__':
    main()
