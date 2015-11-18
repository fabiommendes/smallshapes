#-*- coding: utf8 -*-
import os
import sys
import setuptools
from setuptools import setup

#
# Read VERSION from file and write it in the appropriate places
#
AUTHOR = 'Fábio Macêdo Mendes'
BASE, _ = os.path.split(__file__)
with open(os.path.join(BASE, 'VERSION')) as F:
    VERSION = F.read().strip()
path = os.path.join(BASE, 'src', 'smallshapes', 'meta.py')
with open(path, 'w') as F:
    F.write(
        '# Auto-generated file. Please do not edit\n'
        '__version__ = %r\n' % VERSION +
        '__author__ = %r\n' % AUTHOR)
VERSION_BIG = VERSION.rpartition('.')[0]

#
# Choose the default Python3 branch or the code converted by 3to2
#
PYSRC = 'src' if sys.version.startswith('3') else 'py2src'

#
# Cython stuff (for the future)
#
setup_kwds = {}
if 'PyPy' not in sys.version:
    try:
        from Cython.Build import cythonize
        from Cython.Distutils import build_ext
    except ImportError:
        import warnings
        warnings.warn('Please install Cython to compile faster versions of FGAme modules')
    else:
        try:
            setup_kwds.update(
                ext_modules=cythonize('src/generic/*.pyx'),
                cmdclass={'build_ext': build_ext})
        except ValueError:
            pass

#
# Main configuration script
#
setup(
    name='smallshapes',
    version=VERSION,
    description='A simple engine that implements mathematical shapes of '
                'small dimensionality',
    author='Fábio Macêdo Mendes',
    author_email='fabiomacedomendes@gmail.com',
    url='https://github.com/fabiommendes/smallshapes',
    long_description=open(os.path.join(BASE, 'README.rst')).read(),

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
    ],

    package_dir={'': PYSRC},
    packages=setuptools.find_packages(PYSRC),
    license='GPL',
    install_requires=['smallvectors>=%s' % VERSION_BIG, 'six'],
    zip_safe=False,
    **setup_kwds
)
