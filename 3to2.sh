#!/bin/sh
3to2 py2src/ --no-diffs -j4 -w -f kwargs -f division -f metaclass -f unpacking -f super
addpyenconding.py  py2src
