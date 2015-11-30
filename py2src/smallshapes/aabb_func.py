'''
Created on 30/06/2015

@author: chips
'''

from __future__ import division
from mathtools.shapes import *
from Fatou import generic
inf = float('inf')

#
# Declaration of generic functions
#


@generic
def aabb(obj):
    '''Return an AABB object corresponding to the minimum axis-aligned
    bounding box that surrounds the given object'''

    try:
        return obj.aabb()
    except AttributeError:
        try:
            xmin, xmax = shadow(obj, ux2D)
            ymin, ymax = shadow(obj, uy2D)
            return AABB(xmin, xmax, ymin, ymax)
        except TypeError:
            raise TypeError('cannot extract AABB from %s object' % tname(obj))


@generic
def cbb(obj):
    '''Return a Circle object corresponding to the minimum circular bounding
    box that surrounds the given object'''

    try:
        return obj.cbb()
    except AttributeError:
        try:
            return cbb(aabb(obj))
        except TypeError:
            raise TypeError('cannot extract CBB from %s object' % tname(obj))


#
# AABB implementations
#
@aabb.overload
def aabb(obj: AABB):
    return obj


@aabb.overload
def aabb(obj: Circle):
    r, x, y = obj
    return AABB(x - r, x + r, y - r, y + r)


@aabb.overload
def aabb(obj: (Poly, Segment)):
    X = [v.x for v in obj]
    Y = [v.y for v in obj]
    return AABB(min(X), max(X), min(Y), max(Y))


@aabb.overload
def aabb(obj: Line):
    if obj.tangent.y == 0:
        y = obj.point.y
        return AABB(-inf, inf, y, y)
    elif obj.tangent.x == 0:
        x = obj.point.x
        return AABB(x, x, -inf, inf)
    else:
        return AABB(-inf, inf, -inf, inf)


#
# CBB implementations
#
@cbb.overload
def cbb(obj: Circle):
    return obj


@cbb.overload
def cbb(obj: AABB):
    u = obj.point_se
    v = obj.point_nw
    return Circle((v - u).norm(), middle(u, v))


@cbb.overload
def cbb(obj: Segment):
    u, v = obj
    return Circle((v - u).norm(), middle(u, v))


@cbb.overload
def cbb(obj: Poly):
    pos = obj.center()
    r2 = max((u - pos).norm_sqr() for u in obj)
    return Circle(sqrt(r2), pos)


@cbb.overload
def cbb(obj: Line):
    return Circle(inf, obj.point)


@generic
def middle(u: Vec, v: Vec):
    '''Return the middle point between two smallvectors or two points'''

    return (u + v) / 2


@middle.overload
def middle(u: Point, v: Point):
    return ((u.to_vector() + v.to_vector()) / 2).to_vector()
