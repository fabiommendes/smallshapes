# -*- coding: utf8 -*-
from __future__ import division
from math import pi, sqrt
from smallvectors import dot, Vec
from smallvectors.core import FlatView
from smallshapes.base import Convex, Immutable, Mutable

SQRT_HALF = 1 / sqrt(2)

class CircleAny(Convex):

    '''Any class for Circle and mCircle classes'''

    __slots__ = ('_radius', '_x', '_y')

    def __init__(self, radius, pos=(0, 0)):
        self._radius = radius
        self._x, self._y = pos

    def __len__(self):
        return 2
    
    def __iter__(self):
        yield self._radius
        yield Vec(self._x, self._y)

    def __repr__(self):
        fmt = type(self).__name__, self.radius, tuple(self.pos)
        return '%s(%s, pos=%s)' % fmt
    
    def displaced_by_vector_to(self, vec):
        return type(self)(self.radius, vec)
    
    # Properties
    @property
    def radius(self):
        return self._radius

    @property
    def pos(self):
        return Vec(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    # Boundary boxes
    @property
    def aabb(self):
        r, x, y = self._radius, self._x, self._y
        return self.__aabb_t__(x -r, x + r, y - r, y + r)
    
    @property
    def xmin(self):
        return self._x - self._radius
    
    @property
    def xmax(self):
        return self._x + self._radius

    @property
    def ymin(self):
        return self._y - self._radius
    
    @property
    def ymax(self):
        return self._y + self._radius
    
    @property
    def cbb(self):
        return self.immutable()
    
    @property
    def cbb_radius(self):
        return self._radius

    # Flat iterator
    def __flatgetitem__(self, key):
        if key == 0:
            return self._radius
        elif key == 1:
            return self._x 
        elif key == 2:
            return self._y
        else:
            raise IndexError(key)

    def __flatlen__(self):
        return 3

    def __flatiter__(self):
        yield self._radius
        yield self.x
        yield self.y
        
    # Geometric properties
    def area(self):
        return pi * self._radius * self._radius

    def ROG_sqr(self):
        return self._radius * self._radius / 2

    def ROG(self):
        return self._radius * SQRT_HALF

    # SAT theorem
    def directions(self, n):
        return []

    def shadow(self, n):
        p0 = dot(self.pos, n)
        r = self._radius
        return (p0 - r, p0 + r)

    def distance_center(self, other):
        return self._pos.distance(other.pos)

    def distance_circle(self, other):
        distance = self._pos.distance(other.pos)
        sum_radius = self._radius + other.radius
        return max(distance - sum_radius, 0)

    # Containment functions
    def contains_circle(self, other):
        return (self.contains_point(other.pos) and
                (self.distance_center(other) + other.radius < self._radius))

    def contains_point(self, point):
        return self._pos.distance(point) <= self._radius


class Circle(CircleAny, Immutable):

    '''A circle of given radius and position `pos`''' 

    __slots__ = ()


class mCircle(CircleAny, Mutable):

    '''A mutable circle class'''

    __slots__ = ()

    def __flatsetitem__(self, key, value):
        if key == 0:
            self._radius = value
        elif key == 1:
            self._x = value 
        elif key == 2:
            self._y = value
        else:
            raise IndexError(key)
            
    @Circle.radius.setter
    def radius(self, value):
        self._radius = float(value)

    @Circle.pos.setter
    def pos(self, value):
        self._x, self._y = value
