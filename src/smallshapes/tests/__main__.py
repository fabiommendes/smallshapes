'''
Loads all tests in package and run
'''

import doctest
import sys
from smallshapes.tests import *  # @UnusedWildImport
import smallshapes as mod_current

try:
    from unittest2 import main
except ImportError:
    from unittest import main


def load_tests(loader, tests, ignore):
    prefix = mod_current.__name__

    # Find doctests
    for modname, mod in sys.modules.items():
        if modname.startswith(prefix + '.') or modname == prefix:
            try:
                tests.addTests(doctest.DocTestSuite(mod))
            except ValueError:  # no docstring
                pass

    return tests

main()
