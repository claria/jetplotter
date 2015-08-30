#!/usr/bin/env python2

import sys
import shutil
import tempfile
import os


def main():

    filename = sys.argv[1]

    clone_list = ['yb0ys0', 'yb1ys0', 'yb2ys0', 'yb1ys1', 'yb0ys1', 'yb0ys2']

    identifier = ''
    for item in clone_list:
        if item in filename:
            identifier = item
            break

    if not identifier: 
        print 'No identifier in filename.Exit.'
        sys.exit(1)

    clone_list.remove(identifier)

    for item in clone_list:
        # copy the original
        target_filename = filename.replace(identifier, item)
        print 'Copy {0} to {1}'.format(filename, target_filename)
        shutil.copyfile(filename, target_filename)
        replace_dict = { identifier : item }
        print 'Replace stuff in {0} using {1}'.format(target_filename, replace_dict)
        replace(target_filename, replace_dict)

def replace(source_file_path, replace_dict):
    """ Replace all occurences of keys in replace_dict with the related
        value in the file source_file_path.
    """

    fh, target_file_path = tempfile.mkstemp()
    with open(target_file_path, 'w') as target_file:
        with open(source_file_path, 'r') as source_file:
            for line in source_file:
                for pattern in replace_dict:
                    line = line.replace('{0}'.format(pattern), replace_dict[pattern])
                target_file.write(line)
    os.remove(source_file_path)
    shutil.move(target_file_path, source_file_path)



if __name__ == '__main__':
    main()
