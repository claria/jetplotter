import logging
from modules.base_module import BaseModule

log = logging.getLogger(__name__)

import tempfile
import subprocess
import os
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
    tempdir = tempfile.gettempdir()
    new_filelist = []
    for filename in filelist:
        new_filename = os.path.join(tempdir, '{0}{1}{2}'.format(os.path.splitext(os.path.basename(filename))[0], 
                                                                 '_' + suffix if suffix else '', 
                                                                 os.path.splitext(filename)[1]))
        shutil.copy(filename, new_filename)
        new_filelist.append(new_filename)
    return new_filelist


class CopyToWebModule(BaseModule):
    def __init__(self):
        super(CopyToWebModule, self).__init__()
        self.arg_group.add_argument('--www', nargs='+', type='str2kvstr', action='setting', help='')

    def __call__(self, config):
        pass
        return
        remote_host = 'sieber@ekplx69.physik.uni-karlsruhe.de' 
        remote_basedir = '/autofs/ekpwww/web/sieber/public_html/private/plots/'
        remote_dir = os.path.join(remote_basedir, date.today().isoformat())
        current_datetime = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

        file_list = []
        file_list.append(os.path.join(config['output_prefix'], config['output_path']))
        file_list.append(os.path.join(config['output_prefix'], config['output_path'].replace('.png', '.json')))
        file_list.append(os.path.join(config['output_prefix'], config['output_path'].replace('.png', '.pdf')))

        files_to_copy = create_copy(file_list, current_datetime)
        files_to_copy += create_copy(['index.php'])

        time.sleep(random.uniform(1,10))
        rsync(files_to_copy, remote_host, remote_dir)
#
#
def rsync(filelist, remote_host, remote_dir):
    cmd = 'rsync -uavz --remove-source-files {0} {1}:{2}'.format(' '.join(filelist), remote_host, remote_dir)
    log.debug('Executing command \'{0}\''.format(cmd))
    rc = subprocess.call(cmd.split())
    return rc


