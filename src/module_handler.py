import inspect
import fnmatch
import os
import imp

from modules.base_module import Module
from modules import base_module

import logging
log = logging.getLogger(__name__)


def get_all_modules():
    """Detect all modules in modules_dirs and add them to avalaible modules."""

    modules_dirs = ['src/modules']
    # Loop over all possible module files
    matches = []
    for module_dir in modules_dirs:
        for root, dirnames, filenames in os.walk(module_dir):
            for filename in fnmatch.filter(filenames, '*.py'):
                matches.append(os.path.join(root, filename))

    available_modules = {}
    for filename in matches:
        try:
            log.info("Try to import module from path {0}.".format(filename))
            module_name = os.path.splitext(os.path.basename(filename))[0]
            module = imp.load_source(module_name, filename)
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj):
                    if issubclass(obj, Module):
                        log.debug("Adding module {0}.".format(obj.label))
                        available_modules[obj.label()] = obj
        except ImportError as e:
            log.debug("Failed to import module {0} from {1}.".format(module_name, filename))
            log.debug("Error message: {0}.".format(e))

    return available_modules


#def register_modules_dir(self, module_dir):
#    """Add directory to list of searched directories for modules."""
#    # Expand environment variables
#    module_dir = os.path.expandvars(module_dir)
#    # absolute path
#    if os.path.isdir(module_dir):
#        self._modules_dirs.append(module_dir)
#    # relative path to current file
#    elif os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), module_dir)):
#        self._modules_dirs.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), module_dir))
#    else:
#        log.critical("Couldnt append %s to list of module directories!" % module_dir)
#
#def _print_available_modules(self):
#    """Prints all available modules to stdout."""
#    title_strings = ["Input modules:", "Analysis modules:", "Plot modules:"]
#    baseclasses = [InputBase, AnalysisBase, PlotBase]
#    for index, (title_string, baseclass) in enumerate(zip(title_strings, baseclasses)):
#        log.info(("\n" if index > 0 else "")+tools.get_colored_string(title_string, "yellow"))
#        self._print_module_list(sorted([module for module in self.available_processors if issubclass(self.available_processors[module], baseclass)]))
#
def _print_module_list(self, module_list):
   """Print a list of modules (name and docstring)"""
   for module in module_list:
       log.info("\t"+tools.get_colored_string("{}".format(module), "green"))
       if inspect.getdoc(self.available_processors[module]):
           log.info(tools.get_indented_text("\t\t", inspect.getdoc(self.available_processors[module])))

