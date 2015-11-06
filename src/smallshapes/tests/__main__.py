'''
Loads all tests in package and run
'''

import doctest
import sys
from smallshapes.tests import *  # @UnusedWildImport
import smallshapes as mod_current
from pytest import main

if __name__ == '__main__':
    main('. -q')
