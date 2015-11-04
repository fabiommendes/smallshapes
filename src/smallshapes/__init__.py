'''
==================
Geometrical shapes
==================

The mathshapes.shape module define classes for various geometric primitives
such as points, lines, circles, polygons, etc. All these objects define some
common mathematical operations such as containment and distance FGAme_tests,
projections, and superposition calculations via SAT.


Mutable vs immutable
====================

Most objects have both an immutable and a mutable implementation with a
similar API. Mutable objects should be used when the geometric object
represents some fixed identity (e.g., a circle in a scene that can move and
change is geometric properties). All other sittuations should use immutable
types, (e.g.: check if to circles of given radius and positions intercept or
not).
'''

from .base import *
from .circle import *
from .aabb import *
from .line import *
from .poly import *
#from .SAT import *

#
# Late binding
#
Shape._circle = Circle
Shape._mcircle = mCircle
Shape._aabb = AABB
Shape._maabb = mAABB
