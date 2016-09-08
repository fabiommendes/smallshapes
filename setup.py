# -*- coding: utf8 -*-
#
# This file were created by Python Boilerplate. Use boilerplate to start simple
# usable and best-practices compliant Python projects.
#
# Learn more about it at: http://github.com/fabiommendes/python-boilerplate/
#

import os

import sys
from setuptools import setup, find_packages


# Meta information
name = 'smallshapes'
project = 'smallshapes'
author = 'Fábio Macêdo Mendes'
version = open('VERSION').read().strip()
dirname = os.path.dirname(__file__)


# Save version and author to __meta__.py
with open(os.path.join(dirname, 'src', project, '__meta__.py'), 'w') as F:
    F.write('__version__ = %r\n__author__ = %r\n' % (version, author))


# Cython support
setup_kwds = {}
if 'PyPy' not in sys.version:
    try:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext
    except ImportError:
        import warnings
        warnings.warn('Please install Cython to compile faster versions of '
                      'smallshapes modules')
    else:
        try:
            setup_kwds.update(
                ext_modules=cythonize('src/generic/*.pyx'),
                cmdclass={'build_ext': build_ext})
        except ValueError:
            pass


setup(
    # Basic info
    name=name,
    version=version,
    author=author,
    author_email='fabiomacedomendes@gmail.com',
    url='',
    description='A simple engine that implements mathematical shapes of '
                'small dimensionality',
    long_description=open('README.rst').read(),

    # Classifiers (see https://pypi.python.org/pypi?%3Aaction=list_classifiers)
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries',
    ],

    # Packages and depencies
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=[
        'smallvectors>=0.6',
    ],
    extras_require={
        'dev': [
            'invoke',
            'manuel',
            'pytest',
            'python-boilerplate',
        ],
    },

    # Other configurations
    zip_safe=False,
    platforms='any',
)