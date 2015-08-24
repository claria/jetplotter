import inspect
import fnmatch
import os
import imp
import logging

from modules.base_module import BaseModule

log = logging.getLogger(__name__)


def discover_modules():
    """Detect all modules in modules_dirs and add them to avalaible modules."""

    modules_dirs = [os.path.join(os.path.dirname(__file__), '../modules')]
    # Loop over all possible module files
    matches = []
    for module_dir in modules_dirs:
        for root, dirnames, filenames in os.walk(module_dir):
            for filename in fnmatch.filter(filenames, '*.py'):
                matches.append(os.path.join(root, filename))

    available_modules = {}
    for filename in matches:
        try:
            log.debug("Try to import modules from path {0}.".format(filename))
            module_name = os.path.splitext(os.path.basename(filename))[0]
            module = imp.load_source(module_name, filename)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    if issubclass(obj, BaseModule):
                        log.debug("Adding module {0}.".format(obj.label))
                        available_modules[obj.label()] = obj
        except ImportError as e:
            log.debug("Failed to import module {0} from {1}.".format(module_name, filename))
            log.debug("Error message: {0}.".format(e))

    return available_modules
