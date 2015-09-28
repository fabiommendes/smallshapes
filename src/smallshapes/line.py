# -*- coding: utf8 -*-
'''
====================
Line-like primitives
====================

A module for all line-like primitives::

    - **Segment:** a finite directed line segment defined by a starting and an
      ending point
    - **Ray:** a semi-finite line segment defined by a point and a direction.
    - **Line:** an infinite line defined by two points
'''

# TODO
from smallvectors import dot, asvector, aspoint, Point, Vec
#from smallvectors.util import pt_print, tp_print
from smallshapes.base import Curve

Inf = float('inf')


###############################################################################
# Segment -- a finite line segment
###############################################################################
class SegmentBase(Curve):

    '''Base class for Segment and mSegment'''

    __slots__ = ['_start', '_end']

    def __init__(self, start, end):
        self._start = asvector(start)
        self._end = asvector(end)

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def direction(self):
        return self.end - self.start

    def __iter__(self):
        yield self._start
        yield self._end


class Segment(SegmentBase):

    '''Represents a directed line segment from `start` point to `end` point'''


class mSegment(SegmentBase):

    '''A mutable version of Segment'''

    @SegmentBase.start.setter
    def start(self, value):
        self._start = self._asvector(value)

    @SegmentBase.end.setter
    def end(self, value):
        self._end = self._asvector(value)

    @SegmentBase.direction.setter
    def direction(self, value):
        self.end = self.start + self._asvector(value)

###############################################################################
# Ray -- semi-infinite line
###############################################################################


class RayBase(Curve):

    '''Base class for Ray and mRay'''

    def __init__(self, point, direction):
        self.point = Vec(point)
        self.direction = Vec(direction).normalize()


class Ray(RayBase):

    '''A directed line that is infinite in one direction'''


class mRay(RayBase):

    '''A mutable Ray'''


###############################################################################
# Line -- an infinite line
###############################################################################
class LineBase(Curve):

    '''Base class for Line and mLine'''

    def __init__(self, *args):
        raise NotImplementedError

    def directions(self, n):
        return [self.tangent(), self.normal()]

    def shadow(self, n):
        if abs(dot(self.tangent(), n)) < 1e-6:
            p = dot(self.p1, n)
            return p, p
        else:
            return [-Inf, Inf]


class Line(LineBase):

    '''A infinite line that passes in point p0 and has an unity direction u'''


class mLine(LineBase):

    '''A mutable Line'''


###############################################################################
# Path -- a sequence of points
###############################################################################
class PathBase(Curve):

    '''Base class for Path and mPath'''

    def __init__(self, points):
        self._points = list(Point(*pt) for pt in points)

    def __iter__(self):
        return iter(self._points)

    def __getitem__(self, idx):
        return self._points[idx]

    def __len__(self):
        return len(self._points)

    def __repr__(self):
        data = [str(tuple(pt)) for pt in self._points]
        data = ', '.join(data)
        return '%s([%s])' % (type(self).__name__, data)


class Path(PathBase):

    '''A path represented by a sequence of points'''


class mPath(PathBase):

    '''A mutable Path'''
if __name__ == '__main__':
    import doctest
    doctest.testmod()
