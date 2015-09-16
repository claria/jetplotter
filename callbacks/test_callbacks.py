""" Demonstrates the callback mechanism. This function will be called
    after the building of the config.
"""

import util.callbacks as callbacks

print "hallo"

@callbacks.register('after_config_build')
def after_config(*args, **kwargs):
    print 'Config was build'
