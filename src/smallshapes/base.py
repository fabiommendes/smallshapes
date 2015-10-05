'''
Base classes for smallshapes objects
'''

import functools
from abc import abstractmethod, abstractproperty, ABCMeta
from smallvectors import Vec, asvector, aspoint, asdirection
from smallvectors.core import Flat, mFlat, FlatView

def args_or_vec_method(func):
    '''Decorator that transforms a method that only accept vector inputs to
    a function that accepts both coordinates or vectors'''
    
    @functools.wraps(func)
    def decorated(self, *args):
        if len(args) == 1:
            return func(self, asvector(args[0]))
        else:
            return func(self, asvector(args))
        
    return decorated
    
class SerializableAny(metaclass=ABCMeta):
    '''Serializable objects exihibit a `flat` iterable object that can traverse
    the scalar contents of the object in a serial fashion.
    
    Seriable objects can be linearized to a flat list or initialized from it.
    
    Mutable serializable objets can also be modified directly by this list.
    '''
    
    __slots__ = ()

    _newflat = None
    
    def __init__(self, *args):
        self.flat = self._newflat(self._flat_from_args(args))

    def __getitem__(self, key):
        N = len(self)
        if isinstance(key, int):
            if key > N:
                raise IndexError(key)
            elif key >= 0:
                for i, x in zip(self, range(N)):
                    pass
                if i == key:
                    return x
                raise IndexError(key)
            elif key < 0:
                return self[N - key]
        
        elif isinstance(key, slice):
            return [self[i] for i in range(*slice)]
        
        else:
            raise TypeError('invalid index: %r' % key)

    def __len__(self):
        return len(self.flat)
    
    def __iter__(self):
        return iter(self.flat)

    def __repr__(self):
        args = ', '.join(map(str, self))
        return '%s(%s)' % (type(self).__name__, args)
    
    def __eq__(self, other):
        if (isinstance(other, type(self)) or 
                isinstance(self, type(other)) or
                not isinstance(other, Locatable)):
            return all(x == y for (x, y) in zip(self, other))
        else:
            return False

    @classmethod
    def from_flat(cls, data, copy=True):
        cls.__getflat__(data)
        new = object.__new__(cls)
        new.flat = new._newflat(data, copy)
        return new
        
    @classmethod
    def from_seq(cls, seq):
        return cls(*seq)
    
    @classmethod
    def __getflat__(cls, args):
        return args
        
    @classmethod
    def __getargs__(cls, flat):
        return tuple(flat)
    
    @property
    def flat(self):
        '''Represents object as flattened scalar data'''
        
        return FlatView(self)

class Serializable(SerializableAny):
    '''An immutable serializable object'''
    
    _newflat = Flat


class mSerializable(SerializableAny):
    '''A mutable serializable object'''
    
    _newflat = mFlat
        
        
        
class SmallShapeBase(Serializable):
    '''Base class for all gemetric objects in the smallshapes package.
    
    Similarly to classes in the smallvectors package, `smallshapes` objects must
    implement a Serializable/mSerializable interface.
    '''

    __slots__ = ()
    

    
#
# Locatable base classes
#
class LocatableAny(SmallShapeBase):
    '''
    Base class for all geometric objects that have a location in space.
    
    Subclasses must define a `pos` attribute as a vector with the center point
    coordinates and a few methods that implement space translations.
    
    displaced_by_vector_to (abstract):
        Return a copy of with the center point displaced to the given position
        vector. This method can assume that the input is a Vec[n, float] object
        and may perform any optimizations based in this assumption. Users should
        generally use the locatable.displaced_to() method.
    displaced_by_vector:
        Similar to `displaced_by_vector_to`, but uses relative displacements.
    '''
    
    __slots__ = ()
    
    def moved(self, *args):
        '''Alias to obj.displaced()'''
        
        return self.displaced(*args)
    
    @args_or_vec_method
    def displaced(self, vec):
        '''Return a copy of itself displaced by the given vector or 
        coordinates'''
    
        return self.displaced_by_vector(vec)
        
    def displaced_by_vector(self, vector):
        '''Like obj.displaced(vec), but expects a vector input'''

        self.displaced_by_vector_to(vector + self.pos)

    @args_or_vec_method
    def displaced_to(self, vec):
        '''Return a copy of itself displaced to reach the given final 
        position'''
    
        return self.displaced_by_vector(vec)
    
    @abstractmethod
    def displaced_by_vector_to(self, vector):
        '''Like obj.displaced_to(vec), but expects a vector input'''

        raise NotImplementedError

    @abstractproperty
    def pos(self):
        '''Vector to object's center position.
        
        Note: obj.pos is a Vec instance and obj.center is a Point.'''
        
        raise NotImplementedError
        
    @property
    def center(self):
        '''Object's center position.
        
        Note: obj.pos is a Vec instance and obj.center is a Point.'''
        
        return aspoint(self.pos)
    

class Locatable(LocatableAny):
    '''Base class for immutable geometric types'''
    
    __slots__ = ()
    
    def __hash__(self):
        return hash(tuple(self))

    def copy(self):
        '''Return a copy of itself'''
        
        return self
    
class mLocatable(LocatableAny):
    '''Base class for mutable geometric types'''
    
    __slots__ = ()
    
    def __setitem__(self, key, value):
        N = len(self)
        if isinstance(key, int):
            if key > N:
                raise IndexError(key)
            elif key >= 0:
                self.__setitem_simple__(key, value)
            elif key < 0:
                self.__setitem_simple__(N - key, value)
        elif isinstance(key, slice):
            indexes = range(*slice)
            if indexes[-1] > len(self):
                raise IndexError
            else:
                setindex = self.__setitem_simple__
                values = [value[i] for i in indexes]
                for i,v in zip(indexes, values):
                    setindex(i, v)
        else:
            raise TypeError('invalid index: %r' % key)
        
    def __setitem_simple__(self, key, value):
        raise NotImplementedError
    
    def move(self, *args):
        '''Alias to obj.displace(*args)'''
        
        self.displace(*args)
        
    @args_or_vec_method
    def setpos(self, vec):
        '''Set the center of object position *INPLACE*'''
        
        self.setpos_vector(vec)
        
    def setpos_vector(self, vec):
        '''Like obj.setpos(vec), but expects vector inputs'''
        
        self.pos = vec
        
    @args_or_vec_method
    def displace(self, vec):
        '''Change object position *INPLACE*'''
        
        self.setpos_vector(self.pos + vec)
        
    def copy(self):
        '''Return a copy of itself''' 
        
        return type(self)(*iter(self))
#
# Curves
#
class ShapeAny(LocatableAny):

    '''Base class for all objects that have a definite shape.
    
    The shape does not have to be solid, e.g., a line can be a shape.'''

    __slots__ = ()

    # These must be fixed after the proper subclasses are defined using late
    # binding
    _Circle = None
    _Segment = None
    _asvector = staticmethod(asvector)
    _aspoint = staticmethod(aspoint)
    _asdirection = staticmethod(asdirection)

    def rotated(self, rotation):
        '''Return a copy of rotated by the given rotation'''
        
        if rotation:
            tname = type(self).__name__
            raise TypeError('%r objects do not implement rotations' % tname)
        return self.copy()
    
    def rotated_at(self, rotation, axis):
        '''Return a copy of rotated by the given rotation'''
        
        rotated = self.rotated(rotation)
        delta = (axis - self.pos).rotated(rotation)
        return rotated.displaced_by_vector(delta)

    def rescaled(self, scale):
        '''Return a copy rescaled around the center point by the given scale 
        factor'''
        
        tname = type(self).__name__
        raise TypeError('%r objects cannot be rescaled' % tname)

    def rescaled_at(self, scale, point):
        '''Return a copy rescaled by the given scale factor using the 
        reference point as the center of the scaling operation.'''
        
        # Try to rescale at the center
        self.rescaled(scale)
        
        tname = type(self).__name__
        msg = '%r objects can only be rescaled at their centers' % tname
        raise TypeError(msg)


    def distance_to_point(self, point):
        '''Return the distance of object to the given point. Return 0.0 if
        they intercept'''

        raise NotImplementedError

    def distance_to_circle(self, circle):
        '''Return the distance to the given circle. Return 0.0 if both shapes
        intercept'''

        raise NotImplementedError

    def distance_to(self, other):
        '''Return the distance between two objects. Return 0.0 if they
        intercept'''

        if isinstance(other, (Vec, tuple)):
            return self.distance_point(other)
        elif isinstance(other, self._Circle):
            return self.distance_circle(other)
        else:
            t1 = type(self).__name__
            t2 = type(other).__name__
            raise TypeError('invalid distance test: %s vs %s' % (t1, t2))

class Shape(ShapeAny, Locatable):
    '''Immutable shape object'''
    
    __slots__ = ()
    
class mShape(ShapeAny, mLocatable):
    '''A muttable shape object'''

    __slots__ = ()

#
# Solid shapes
#
class SolidAny(ShapeAny):

    '''Base class for all closed shape objects'''

    __slots__ = ()

    def contains_point(self, point):
        '''Tests if the given point is completely contained by object'''

        raise NotImplementedError

    def contains_circle(self, circle):
        '''Tests if the given circle is completely contained by object'''

        raise NotImplementedError

    def contains_segment(self, segment):
        '''Tests if the given line segment is completely contained by object'''

        raise NotImplementedError

    def __contains__(self, other):
        if isinstance(other, (Vec, tuple)):
            return self.contains_point(other)
        elif isinstance(other, self._Circle):
            return self.contains_circle(other)
        else:
            t1 = type(self).__name__
            t2 = type(other).__name__
            raise TypeError('invalid containement test: %s vs %s' % (t1, t2))

class Solid(SolidAny, Shape):
    '''Immutable solid shapes'''
    
    __slots__ = ()

class mSolid(SolidAny, mShape):
    '''Muttable solid shapes'''

    __slots__ = ()
    
    
#
# Convex shapes
#
class ConvexAny(SolidAny):

    '''Base class for all convex shapes'''
    
    __slots__ = ()

    # Generic containement FGAme_tests implementations that are valid for all
    # convex shapes
    def contains_segment(self, segment):
        pt_test = self.contains_point
        pt1, pt2 = segment
        return pt_test(pt1) and pt_test(pt2)

class Convex(ConvexAny, Solid):
    '''Immutable convex shapes'''
    
    __slots__ = ()
    
class mConvex(ConvexAny, mSolid):
    '''Mutable convex shapes''' 
    
    __slots__ = ()

if __name__ == '__main__':
    import doctest
    doctest.testmod()
