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

from smallvectors import dot, asvector, asdirection, Vec
from smallshapes.base import Shape, Mutable, Immutable

Inf = float('inf')


class SegmentAny(Shape):
    __slots__ = ('_start', '_end')

    def __init__(self, start, end):
        self._start = asvector(start)
        self._end = asvector(end)

    def __iter__(self):
        yield self._start
        yield self._end

    def __len__(self):
        return 2

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end
    
    @property
    def pos(self):
        return (self._start + self._end) / 2
    
    @property
    def xmin(self):
        return min(self._start.x, self._end.x)
    
    @property
    def xmax(self):
        return max(self._start.x, self._end.x)
    
    @property
    def ymin(self):
        return min(self._start.y, self._end.y)
    
    @property
    def ymax(self):
        return max(self._start.y, self._end.y)
    
    @property
    def direction(self):
        return self.end - self.start
    
    def displaced_by_vector_to(self, pos):
        u, v = self
        delta = pos - (u + v) / 2
        return type(self)(u + delta, v + delta)

class Segment(SegmentAny, Immutable):

    '''Represents a directed line segment from `start` point to `end` point.
    
    A segment is initialized from its end points:
    
    >>> obj = Segment((-1, 1), (1, 1))
    >>> obj.direction
    Vec(2, 0)
    '''


class mSegment(SegmentAny, Mutable):

    '''A mutable version of Segment'''

    @SegmentAny.start.setter
    def start(self, value):
        self._start = self._asvector(value)

    @SegmentAny.end.setter
    def end(self, value):
        self._end = self._asvector(value)

    @SegmentAny.direction.setter
    def direction(self, value):
        self.end = self.start + self._asvector(value)

    @SegmentAny.pos.setter
    def pos(self, value):
        start, end = self
        pos = (start + end) / 2
        delta = value - pos
        self._start += delta
        self._end += delta

class LineOrRayBase(Shape):
    '''Common functionality to Line and Ray objects'''
    
    __slots__ = ('pos', 'tangent')

    def __init__(self, start, direction):
        self.pos = asvector(start)
        self.tangent = asdirection(direction)
        
    def __iter__(self):
        yield self.start
        yield self.tangent
        
    def __flatiter__(self):
        yield from self.start
        yield from self.tangent

    def __len__(self):
        return 2

    @property
    def start(self):
        return self.pos
    
    @property
    def direction(self):
        return self.tangent

    def sat_directions(self, n):
        T = self.tangent
        return [T, T.perp()]

    def displaced_by_vector_to(self, pos):
        return type(self)(pos, self.direction)


class RayAny(LineOrRayBase):

    '''Any class for Ray and mRay'''

    __slots__ = ()
    

class Ray(RayAny, Immutable):

    '''A directed line that is infinite in one direction.
    
    Since a Ray is infinte and does not have a center point, the pos attribute
    is the same as `ray.start`.
    
    It only has an start point and the tangent vector in the ray's direction. 
    The tangent vector is always normalized.
    
    >>> ray = Ray((0, 0), (1, 1))
    >>> ray.tangent
    Direction(1, 1)
    '''
    
    __slots__ = ()

class mRay(RayAny, Mutable):

    '''A mutable Ray'''

    __slots__ = ()
    
###############################################################################
# Line -- an infinite line
###############################################################################
class LineAny(LineOrRayBase):

    '''Any class for Line and mLine'''

    __slots__ = ()

    def __contains__(self, pt):
        if self.tangent.cross(self.pos - pt) > 1:
            return False
        else:
            return True  

    def sat_shadow(self, n):
        if abs(dot(self.tangent(), n)) < 1e-6:
            p = dot(self.p1, n)
            return p, p
        else:
            return [-Inf, Inf]


class Line(LineAny, Immutable):

    '''A infinite line that passes in point p0 and has an unity direction;
    
    >>> line = Line((0, 0), (1, 1))
    >>> (-1, 1) in line
    True
    '''
    
    __slots__ = ()


class mLine(LineAny, Mutable):

    '''A mutable Line'''

    __slots__ = ()
    
    
###############################################################################
# Path -- a sequence of points
###############################################################################
class PathAny(Shape):

    '''Any class for Path and mPath'''

    def __init__(self, points):
        self._points = list(Vec(*pt) for pt in points)

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

    def displaced_by_vector_to(self, vec):
        return type(self)([pt + vec for pt in self]) 
        
    @property
    def pos(self):
        length = 0
        vector_part = Vec(0.0, 0.0)
        pt0 = self[-1]
        for pt in self:
            delta = asvector(pt - pt0).norm() #FIXME: Point subtraction --> Vec
            middle = asvector(pt.middle(pt0))
            vector_part += delta * middle
            length += delta
            pt0 = pt
        return vector_part / length 
        
    @property
    def points(self):
        return list(self.points)
    
    @property
    def points_closed(self):
        L = self.points
        L.append(L[0])
        return L

class Path(PathAny, Immutable):

    '''A path represented by a sequence of points
    
    >>> path = Path([(0, 0), (1, 1), (2, 0)])
    >>> path.pos
    Vec(1.0, 0.29289321881345254)
    '''
    

class mPath(PathAny, Mutable):

    '''A mutable Path'''
    
    def __setitem_simple__(self, key, value):
        self._points[key] = value

if __name__ == '__main__':
    import doctest
    doctest.testmod()

    mPath([])